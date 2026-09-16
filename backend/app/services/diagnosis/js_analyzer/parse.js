'use strict';
// Parses submitted JavaScript into a real ESTree AST (via espree, the same
// parser ESLint itself uses) and prints it as JSON on stdout -- the tree
// walking to extract diagnosis features happens on the Python side
// (features_js.py) so the feature logic lives in one place, not duplicated
// across languages.
const espree = require('espree');

let raw = '';
process.stdin.setEncoding('utf-8');
process.stdin.on('data', (chunk) => { raw += chunk; });
process.stdin.on('end', () => {
  const code = JSON.parse(raw);
  try {
    const ast = espree.parse(code, { ecmaVersion: 2022, sourceType: 'script', loc: false, range: false });
    process.stdout.write(JSON.stringify({ ok: true, ast }));
  } catch (e) {
    process.stdout.write(JSON.stringify({ ok: false, message: String((e && e.message) || e) }));
  }
});
