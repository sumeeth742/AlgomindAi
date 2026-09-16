import com.sun.jdi.*;
import com.sun.jdi.connect.*;
import com.sun.jdi.event.*;
import com.sun.jdi.request.*;
import java.io.*;
import java.util.*;

/**
 * Steps through Solution.<methodName> in a launched, debugged JVM, using the
 * real JDI (Java Debug Interface) -- the same mechanism real Java debuggers
 * (jdb, IntelliJ, VS Code's Java debugger) are built on. Every line number
 * and every variable value reported here is read directly out of the
 * debuggee's actual running state via the JDWP wire protocol, not
 * re-derived, approximated, or guessed.
 *
 * Compiled once (its own source never depends on the submission being
 * traced) and reused across requests -- see trace_probe.py's
 * trace_java_execution for how it's invoked: `workDir` must already contain
 * compiled Main.class/Solution.class (Main built the same way java_sandbox.py
 * builds it for a normal run, calling the target method exactly once with
 * the one input being traced).
 *
 * Usage: java TraceDriver <workDir> <methodName> <maxSteps>
 * Prints one line of JSON: {"steps":[...], "truncated":bool,
 * "mainOutput":<Main's own last JSON line, or null>, "driverError":string|null}
 */
public class TraceDriver {
    static final StringBuilder stepsJson = new StringBuilder("[");
    static boolean firstStep = true;
    static int maxSteps;
    static int baseDepth = -1;

    public static void main(String[] args) throws Exception {
        String workDir = args[0];
        String methodName = args[1];
        maxSteps = Integer.parseInt(args[2]);

        LaunchingConnector connector = null;
        for (Connector c : Bootstrap.virtualMachineManager().allConnectors()) {
            if (c.name().equals("com.sun.jdi.CommandLineLaunch")) { connector = (LaunchingConnector) c; break; }
        }
        if (connector == null) {
            System.out.println("{\"steps\":[],\"truncated\":false,\"mainOutput\":null,\"driverError\":\"No launching connector available\"}");
            return;
        }

        Map<String, Connector.Argument> arguments = connector.defaultArguments();
        arguments.get("main").setValue("Main");
        arguments.get("options").setValue("-cp " + workDir);
        VirtualMachine vm = connector.launch(arguments);

        ByteArrayOutputStream stdoutBuf = new ByteArrayOutputStream();
        ByteArrayOutputStream stderrBuf = new ByteArrayOutputStream();
        pump(vm.process().getInputStream(), stdoutBuf);
        pump(vm.process().getErrorStream(), stderrBuf);

        EventRequestManager erm = vm.eventRequestManager();
        ClassPrepareRequest cpr = erm.createClassPrepareRequest();
        cpr.addClassFilter("Solution");
        cpr.enable();

        int stepCount = 0;
        boolean done = false;
        String driverError = null;

        EventQueue queue = vm.eventQueue();
        try {
            while (!done) {
                EventSet eventSet = queue.remove(15000);
                if (eventSet == null) { driverError = "Timed out waiting for the debuggee JVM"; break; }
                for (Event event : eventSet) {
                    if (event instanceof ClassPrepareEvent) {
                        ReferenceType refType = ((ClassPrepareEvent) event).referenceType();
                        List<Method> methods = refType.methodsByName(methodName);
                        if (methods.isEmpty()) {
                            driverError = "Method " + methodName + " not found on Solution";
                            done = true;
                            break;
                        }
                        List<Location> lines = methods.get(0).allLineLocations();
                        if (!lines.isEmpty()) {
                            BreakpointRequest bpr = erm.createBreakpointRequest(lines.get(0));
                            bpr.enable();
                        }
                    } else if (event instanceof BreakpointEvent) {
                        ThreadReference thread = ((BreakpointEvent) event).thread();
                        baseDepth = thread.frameCount();
                        stepCount = recordStep(thread, stepCount);
                        event.request().disable();
                        if (stepCount < maxSteps) armNextStep(erm, thread);
                    } else if (event instanceof StepEvent) {
                        ThreadReference thread = ((StepEvent) event).thread();
                        ((StepRequest) event.request()).disable();
                        stepCount = recordStep(thread, stepCount);
                        if (stepCount < maxSteps) armNextStep(erm, thread);
                    } else if (event instanceof VMDeathEvent || event instanceof VMDisconnectEvent) {
                        done = true;
                    }
                }
                if (!done) eventSet.resume();
            }
        } catch (VMDisconnectedException e) {
            // Debuggee ran to completion on its own -- not an error.
        }
        try { vm.process().waitFor(); } catch (InterruptedException ignored) { }

        stepsJson.append("]");
        String stdout = stdoutBuf.toString("UTF-8");
        String mainOutputLine = null;
        for (String line : stdout.split("\n")) {
            String trimmed = line.trim();
            if (trimmed.startsWith("{")) mainOutputLine = trimmed;
        }
        if (mainOutputLine == null && driverError == null) {
            String stderrText = stderrBuf.toString("UTF-8").trim();
            if (!stderrText.isEmpty()) driverError = "Debuggee crashed before producing output: " + stderrText;
        }

        StringBuilder out = new StringBuilder();
        out.append("{\"steps\":").append(stepsJson)
           .append(",\"truncated\":").append(stepCount >= maxSteps)
           .append(",\"mainOutput\":").append(mainOutputLine == null ? "null" : mainOutputLine)
           .append(",\"driverError\":").append(driverError == null ? "null" : jsonString(driverError))
           .append("}");
        System.out.println(out);
    }

    static void armNextStep(EventRequestManager erm, ThreadReference thread) {
        StepRequest sr = erm.createStepRequest(thread, StepRequest.STEP_LINE, StepRequest.STEP_INTO);
        sr.addClassFilter("Solution");
        sr.enable();
    }

    static int recordStep(ThreadReference thread, int stepCount) throws Exception {
        if (stepCount >= maxSteps) return stepCount;
        StackFrame frame = thread.frame(0);
        Location loc = frame.location();
        List<LocalVariable> vars;
        Map<LocalVariable, Value> rawValues;
        try {
            vars = frame.visibleVariables();
            rawValues = frame.getValues(vars);
        } catch (AbsentInformationException e) {
            vars = Collections.emptyList();
            rawValues = Collections.emptyMap();
        }
        int depth = baseDepth < 0 ? 1 : Math.max(1, thread.frameCount() - baseDepth + 1);

        if (!firstStep) stepsJson.append(",");
        firstStep = false;
        stepsJson.append("{\"line\":").append(loc.lineNumber())
                  .append(",\"depth\":").append(depth)
                  .append(",\"locals\":{");
        boolean first = true;
        for (LocalVariable lv : vars) {
            if (!first) stepsJson.append(",");
            first = false;
            stepsJson.append(jsonString(lv.name())).append(":").append(describeValue(thread, rawValues.get(lv)));
        }
        stepsJson.append("}}");
        return stepCount + 1;
    }

    static String describeValue(ThreadReference thread, Value v) throws Exception {
        if (v == null) return "null";
        if (v instanceof StringReference) return jsonString(((StringReference) v).value());
        if (v instanceof CharValue) return jsonString(String.valueOf(((CharValue) v).value()));
        if (v instanceof BooleanValue) return String.valueOf(((BooleanValue) v).value());
        if (v instanceof PrimitiveValue) return v.toString();
        if (v instanceof ArrayReference) {
            ArrayReference ar = (ArrayReference) v;
            StringBuilder sb = new StringBuilder("[");
            List<Value> vals = ar.getValues();
            for (int i = 0; i < vals.size(); i++) {
                if (i > 0) sb.append(",");
                sb.append(describeValue(thread, vals.get(i)));
            }
            return sb.append("]").toString();
        }
        if (v instanceof ObjectReference) {
            ObjectReference or = (ObjectReference) v;
            String typeName = or.referenceType().name();
            if (typeName.equals("ListNode")) return describeLinkedList(or);
            if (typeName.equals("TreeNode")) return describeTree(or);
            // Any other object (HashMap, ArrayList, a helper class the learner
            // wrote, ...): invoke its real toString() in the debuggee -- a
            // genuine computed value, not a fabricated summary. This is the
            // same category of representation a real debugger's "Variables"
            // pane falls back to for objects without special handling.
            Method toStringMethod = findNoArgMethod(or.referenceType(), "toString");
            if (toStringMethod != null) {
                Value result = or.invokeMethod(thread, toStringMethod, Collections.emptyList(), ObjectReference.INVOKE_SINGLE_THREADED);
                return jsonString(result == null ? "null" : ((StringReference) result).value());
            }
            return jsonString("<" + typeName + ">");
        }
        return jsonString(String.valueOf(v));
    }

    static String describeLinkedList(ObjectReference head) throws Exception {
        List<String> values = new ArrayList<>();
        Set<Long> seen = new HashSet<>();
        ObjectReference cur = head;
        while (cur != null && seen.add(cur.uniqueID())) {
            Field valField = cur.referenceType().fieldByName("val");
            values.add(valField == null ? "null" : String.valueOf(cur.getValue(valField)));
            Field nextField = cur.referenceType().fieldByName("next");
            Value nextVal = nextField == null ? null : cur.getValue(nextField);
            cur = (nextVal instanceof ObjectReference) ? (ObjectReference) nextVal : null;
        }
        return "{\"__type__\":\"linked_list\",\"values\":[" + String.join(",", values) + "]}";
    }

    static String describeTree(ObjectReference root) throws Exception {
        List<String> values = new ArrayList<>();
        Deque<ObjectReference> queue = new ArrayDeque<>();
        if (root != null) queue.add(root);
        while (!queue.isEmpty()) {
            ObjectReference node = queue.poll();
            if (node == null) {
                values.add("null");
            } else {
                Field valField = node.referenceType().fieldByName("val");
                values.add(String.valueOf(node.getValue(valField)));
                Field leftField = node.referenceType().fieldByName("left");
                Field rightField = node.referenceType().fieldByName("right");
                Value leftVal = node.getValue(leftField);
                Value rightVal = node.getValue(rightField);
                queue.add(leftVal instanceof ObjectReference ? (ObjectReference) leftVal : null);
                queue.add(rightVal instanceof ObjectReference ? (ObjectReference) rightVal : null);
            }
        }
        while (!values.isEmpty() && values.get(values.size() - 1).equals("null")) values.remove(values.size() - 1);
        return "{\"__type__\":\"binary_tree\",\"values\":[" + String.join(",", values) + "]}";
    }

    static Method findNoArgMethod(ReferenceType rt, String name) {
        for (Method m : rt.allMethods()) {
            if (m.name().equals(name) && m.argumentTypeNames().isEmpty()) return m;
        }
        return null;
    }

    static String jsonString(String s) {
        StringBuilder b = new StringBuilder("\"");
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            switch (c) {
                case '"': b.append("\\\""); break;
                case '\\': b.append("\\\\"); break;
                case '\n': b.append("\\n"); break;
                case '\r': b.append("\\r"); break;
                case '\t': b.append("\\t"); break;
                default:
                    if (c < 0x20) b.append(String.format("\\u%04x", (int) c));
                    else b.append(c);
            }
        }
        return b.append("\"").toString();
    }

    static void pump(InputStream in, ByteArrayOutputStream out) {
        Thread t = new Thread(() -> {
            byte[] buf = new byte[4096];
            int n;
            try {
                while ((n = in.read(buf)) != -1) out.write(buf, 0, n);
            } catch (IOException ignored) { }
        });
        t.setDaemon(true);
        t.start();
    }
}
