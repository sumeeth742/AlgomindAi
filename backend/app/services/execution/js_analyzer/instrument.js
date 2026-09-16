'use strict';
// Instruments a JS function's source by splicing a real trace-recording call
// before every statement, using espree's real AST (range/loc info) -- not a
// regex or a guess at statement boundaries. A scope stack tracks exactly
// which variable names have actually been declared by each point in
// execution order, so the generated snapshot expression only ever
// references names that are truly in scope there (referencing a `let`/
// `const` before its declaration would throw in real JS -- this walker
// exists specifically to never do that).
//
// Deliberately scoped: only var/let/const with plain identifier targets (no
// destructuring), if/for/for-of/for-in/while/do-while/block statements are
// instrumented; a nested function/arrow function is left untouched (opaque),
// matching the Python tracer's "only the target function's own lines" scope.
const espree = require('espree');

function parseAndFind(code, functionName) {
  const ast = espree.parse(code, { ecmaVersion: 2022, sourceType: 'script', range: true, loc: true });
  let target = null;
  (function walk(node) {
    if (target || !node || typeof node !== 'object') return;
    if (node.type === 'FunctionDeclaration' && node.id && node.id.name === functionName) {
      target = node;
      return;
    }
    if (node.type === 'VariableDeclarator' && node.id && node.id.name === functionName && node.init
        && (node.init.type === 'ArrowFunctionExpression' || node.init.type === 'FunctionExpression')) {
      target = node.init;
      return;
    }
    for (const key of Object.keys(node)) {
      if (key === 'type' || key === 'loc' || key === 'range') continue;
      const value = node[key];
      if (Array.isArray(value)) value.forEach(walk);
      else if (value && typeof value.type === 'string') walk(value);
    }
  })(ast);
  return target;
}

function declaredNames(idNode) {
  // Only plain identifiers are supported (see module docstring) -- anything
  // else (destructuring) is skipped rather than mis-instrumented.
  return idNode.type === 'Identifier' ? [idNode.name] : [];
}

function instrumentFunction(code, functionName, maxSteps) {
  const target = parseAndFind(code, functionName);
  if (!target) return { ok: false, message: `Function ${functionName} not found` };
  if (target.body.type !== 'BlockStatement') return { ok: false, message: 'Only a block-bodied function can be traced' };

  const edits = []; // {pos, text}, applied end-to-start so earlier positions aren't shifted
  const paramNames = target.params.filter((p) => p.type === 'Identifier').map((p) => p.name);

  function traceCall(line, scopeStack) {
    const names = [].concat(...scopeStack);
    const props = names.map((n) => `${JSON.stringify(n)}:${n}`).join(',');
    return `__trace(${line},__d,{${props}});`;
  }

  function instrumentBody(bodyArray, scopeStack) {
    scopeStack.push([]);
    for (const stmt of bodyArray) {
      edits.push({ pos: stmt.range[0], text: traceCall(stmt.loc.start.line, scopeStack) });
      visitStatement(stmt, scopeStack);
    }
    scopeStack.pop();
  }

  function instrumentSingle(stmt, scopeStack) {
    // A non-block single statement body, e.g. `if (x) return y;`. This MUST
    // be wrapped in a real `{ }` block, not just have a trace call inserted
    // in front of it as plain text -- confirmed as a real, serious bug: `if
    // (n<=1) return n;` with only a trace call spliced before `return n;`
    // becomes `if (n<=1) __trace(...);return n;`, and since a brace-less
    // `if` only governs the single statement immediately after it, the
    // ORIGINAL `return n;` silently became unconditional (always runs),
    // corrupting the actual behavior of a base-case check -- not just the
    // trace data, the program's real result was wrong (fibonacci(6)
    // returned 6 instead of 8). Wrapping both the trace call and the
    // original statement in `{ }` keeps them together under the same
    // condition, exactly preserving the original semantics.
    scopeStack.push([]);
    edits.push({ pos: stmt.range[0], text: '{' + traceCall(stmt.loc.start.line, scopeStack) });
    visitStatement(stmt, scopeStack);
    edits.push({ pos: stmt.range[1], text: '}' });
    scopeStack.pop();
  }

  function instrumentBlockOrSingle(node, scopeStack) {
    if (!node) return;
    if (node.type === 'BlockStatement') instrumentBody(node.body, scopeStack);
    else instrumentSingle(node, scopeStack);
  }

  function visitStatement(stmt, scopeStack) {
    const top = scopeStack[scopeStack.length - 1];
    switch (stmt.type) {
      case 'VariableDeclaration':
        for (const decl of stmt.declarations) top.push(...declaredNames(decl.id));
        break;
      case 'IfStatement':
        instrumentBlockOrSingle(stmt.consequent, scopeStack);
        if (stmt.alternate) instrumentBlockOrSingle(stmt.alternate, scopeStack);
        break;
      case 'ForStatement': {
        scopeStack.push([]);
        if (stmt.init && stmt.init.type === 'VariableDeclaration') {
          for (const decl of stmt.init.declarations) scopeStack[scopeStack.length - 1].push(...declaredNames(decl.id));
        }
        instrumentBlockOrSingle(stmt.body, scopeStack);
        scopeStack.pop();
        break;
      }
      case 'ForOfStatement':
      case 'ForInStatement': {
        scopeStack.push([]);
        if (stmt.left.type === 'VariableDeclaration') {
          for (const decl of stmt.left.declarations) scopeStack[scopeStack.length - 1].push(...declaredNames(decl.id));
        }
        instrumentBlockOrSingle(stmt.body, scopeStack);
        scopeStack.pop();
        break;
      }
      case 'WhileStatement':
      case 'DoWhileStatement':
        instrumentBlockOrSingle(stmt.body, scopeStack);
        break;
      case 'BlockStatement':
        instrumentBody(stmt.body, scopeStack);
        break;
      case 'TryStatement':
        instrumentBlockOrSingle(stmt.block, scopeStack);
        if (stmt.handler) {
          scopeStack.push([]);
          if (stmt.handler.param) scopeStack[scopeStack.length - 1].push(...declaredNames(stmt.handler.param));
          instrumentBody(stmt.handler.body.body, scopeStack);
          scopeStack.pop();
        }
        if (stmt.finalizer) instrumentBlockOrSingle(stmt.finalizer, scopeStack);
        break;
      default:
        break; // Return/Expression/Break/Continue/etc. -- no declarations, nothing to recurse into
    }
  }

  const rootScope = [paramNames];
  instrumentBody(target.body.body, rootScope);

  // Recursion depth: `__d` is captured once per invocation (a fresh `let`
  // per call, via closure) from a shared global counter -- so every trace
  // call made during THIS invocation reports the depth it was actually
  // called at, even while a nested recursive call is busy incrementing the
  // counter further for its own invocation.
  edits.push({ pos: target.body.range[0] + 1, text: 'let __d=++globalThis.__algomindDepth;try{' });
  edits.push({ pos: target.body.range[1] - 1, text: '}finally{globalThis.__algomindDepth--;}' });

  edits.sort((a, b) => b.pos - a.pos); // end-to-start, so positions stay valid as we splice
  let spliced = code;
  for (const edit of edits) {
    spliced = spliced.slice(0, edit.pos) + edit.text + spliced.slice(edit.pos);
  }
  return { ok: true, instrumented: spliced };
}

let raw = '';
process.stdin.setEncoding('utf-8');
process.stdin.on('data', (chunk) => { raw += chunk; });
process.stdin.on('end', () => {
  const { code, functionName } = JSON.parse(raw);
  try {
    const result = instrumentFunction(code, functionName);
    process.stdout.write(JSON.stringify(result));
  } catch (e) {
    process.stdout.write(JSON.stringify({ ok: false, message: String((e && e.message) || e) }));
  }
});
