import type { FlowEdge, FlowNode, FlowStep } from "@/components/visualizers/FlowDiagram";

export interface SdVisualization {
  nodes: FlowNode[];
  edges: FlowEdge[];
  steps: FlowStep[];
}

// One diagram per system design lesson, keyed by lesson slug. Every diagram
// mirrors the ASCII sketch or example already described in that lesson's text.
export const SD_VISUALIZATIONS: Record<string, SdVisualization> = {
  "what-is-a-system": {
    nodes: [
      { id: "user", label: "User", col: 0, row: 0, color: "#6b7280" },
      { id: "frontend", label: "Frontend", col: 1, row: 0, color: "#0284c7" },
      { id: "backend", label: "Backend", col: 2, row: 0, color: "#059669" },
      { id: "db", label: "Database", col: 3, row: 0, color: "#9333ea" },
    ],
    edges: [{ from: "user", to: "frontend" }, { from: "frontend", to: "backend" }, { from: "backend", to: "db" }],
    steps: [
      { activeNodes: ["user"], activeEdges: [], note: "A user opens a website in their browser." },
      { activeNodes: ["user", "frontend"], activeEdges: [0], note: "The browser (client) sends a request to the frontend." },
      { activeNodes: ["frontend", "backend"], activeEdges: [1], note: "The frontend forwards the request to the backend server." },
      { activeNodes: ["backend", "db"], activeEdges: [2], note: "The backend reads/writes the database to fulfill the request." },
      { activeNodes: ["user", "frontend", "backend", "db"], activeEdges: [0, 1, 2], note: "The response flows back: Database → Backend → Frontend → User." },
    ],
  },

  "client-server-http": {
    nodes: [
      { id: "client", label: "Client", col: 0, row: 0, color: "#0284c7" },
      { id: "server", label: "Server", col: 1, row: 0, color: "#059669" },
    ],
    edges: [{ from: "client", to: "server", label: "GET /users/42" }, { from: "server", to: "client", label: "200 OK + JSON" }],
    steps: [
      { activeNodes: ["client"], activeEdges: [], note: "Client wants user 42's data." },
      { activeNodes: ["client", "server"], activeEdges: [0], note: "Sends an HTTP GET request to /users/42." },
      { activeNodes: ["server"], activeEdges: [], note: "Server looks up the data and prepares a response." },
      { activeNodes: ["client", "server"], activeEdges: [1], note: "Server replies 200 OK with the user's data as JSON." },
    ],
  },

  "sql-vs-nosql": {
    nodes: [
      { id: "data", label: "Your Data", col: 0, row: 0, color: "#6b7280" },
      { id: "sql", label: "SQL", sublabel: "Postgres, MySQL", col: 1, row: 0, color: "#0284c7" },
      { id: "nosql", label: "NoSQL", sublabel: "Mongo, DynamoDB", col: 1, row: 1, color: "#9333ea" },
    ],
    edges: [{ from: "data", to: "sql" }, { from: "data", to: "nosql" }],
    steps: [
      { activeNodes: ["data", "sql"], activeEdges: [0], note: "Clear relationships, need transactions? → SQL." },
      { activeNodes: ["data", "nosql"], activeEdges: [1], note: "Flexible schema, need to scale writes across machines? → NoSQL." },
    ],
  },

  "horizontal-vs-vertical-scaling": {
    nodes: [
      { id: "lb", label: "Load Balancer", col: 1, row: 0, color: "#d97706" },
      { id: "s1", label: "Server 1", col: 0, row: 1, color: "#059669" },
      { id: "s2", label: "Server 2", col: 1, row: 1, color: "#059669" },
      { id: "s3", label: "Server 3", col: 2, row: 1, color: "#059669" },
      { id: "db", label: "Database", col: 1, row: 2, color: "#9333ea" },
    ],
    edges: [
      { from: "lb", to: "s1" }, { from: "lb", to: "s2" }, { from: "lb", to: "s3" },
      { from: "s1", to: "db" }, { from: "s2", to: "db" }, { from: "s3", to: "db" },
    ],
    steps: [
      { activeNodes: ["lb"], activeEdges: [], note: "A load balancer sits in front of multiple stateless servers." },
      { activeNodes: ["lb", "s1", "s2", "s3"], activeEdges: [0, 1, 2], note: "Incoming requests are distributed across all three servers." },
      { activeNodes: ["s1", "s2", "s3", "db"], activeEdges: [3, 4, 5], note: "Any server can handle any request -- none holds request-specific state; they share the same database." },
      { activeNodes: ["s2"], activeEdges: [], note: "If one server fails, the load balancer stops sending it traffic -- the others keep serving." },
    ],
  },

  "caching-fundamentals": {
    nodes: [
      { id: "app", label: "App Server", col: 0, row: 0, color: "#059669" },
      { id: "cache", label: "Cache", col: 1, row: 0, color: "#d97706" },
      { id: "db", label: "Database", col: 1, row: 1, color: "#9333ea" },
    ],
    edges: [
      { from: "app", to: "cache", label: "1. check" }, { from: "cache", to: "app", label: "2a. hit!" },
      { from: "app", to: "db", label: "2b. miss → query" }, { from: "db", to: "app", label: "3. data" },
      { from: "app", to: "cache", label: "4. populate" },
    ],
    steps: [
      { activeNodes: ["app", "cache"], activeEdges: [0], note: "Request comes in. App checks the cache first." },
      { activeNodes: ["app", "cache"], activeEdges: [1], note: "Cache hit! Return the cached value immediately -- fast, database untouched." },
      { activeNodes: ["app", "db"], activeEdges: [2], note: "On a cache miss instead: app queries the database." },
      { activeNodes: ["app", "db"], activeEdges: [3], note: "Database returns the data." },
      { activeNodes: ["app", "cache"], activeEdges: [4], note: "App populates the cache with this value, so the next request for it is a hit." },
    ],
  },

  "message-queues": {
    nodes: [
      { id: "producer", label: "Producer", col: 0, row: 0, color: "#0284c7" },
      { id: "queue", label: "Message Queue", col: 1, row: 0, color: "#d97706" },
      { id: "c1", label: "Consumer 1", col: 2, row: 0, color: "#059669" },
      { id: "c2", label: "Consumer 2", col: 2, row: 1, color: "#059669" },
    ],
    edges: [{ from: "producer", to: "queue" }, { from: "queue", to: "c1" }, { from: "queue", to: "c2" }],
    steps: [
      { activeNodes: ["producer"], activeEdges: [], note: "Producer has a message to send -- e.g. 'send welcome email'." },
      { activeNodes: ["producer", "queue"], activeEdges: [0], note: "Producer drops the message on the queue and moves on immediately -- it doesn't wait." },
      { activeNodes: ["queue", "c1"], activeEdges: [1], note: "Consumer 1 picks up the message whenever it's ready and processes it." },
      { activeNodes: ["queue", "c2"], activeEdges: [2], note: "Multiple consumers can pull from the same queue, spreading out the work." },
    ],
  },

  "cap-theorem": {
    nodes: [
      { id: "c", label: "Consistency", col: 0, row: 0, color: "#0284c7" },
      { id: "a", label: "Availability", col: 2, row: 0, color: "#059669" },
      { id: "p", label: "Partition Tol.", col: 1, row: 1, color: "#d97706" },
    ],
    edges: [{ from: "c", to: "a" }, { from: "a", to: "p" }, { from: "p", to: "c" }],
    steps: [
      { activeNodes: ["c", "a", "p"], activeEdges: [], note: "Three properties: Consistency, Availability, Partition tolerance." },
      { activeNodes: ["p"], activeEdges: [], note: "In a distributed system, network partitions WILL happen -- P isn't optional." },
      { activeNodes: ["c"], activeEdges: [], note: "Choosing Consistency during a partition: every read is correct, but some requests may be rejected or delayed." },
      { activeNodes: ["a"], activeEdges: [], note: "Choosing Availability during a partition: every request gets a response, but it might be stale." },
    ],
  },

  "rate-limiting": {
    nodes: [
      { id: "request", label: "Request", col: 0, row: 0, color: "#0284c7" },
      { id: "bucket", label: "Token Bucket", col: 1, row: 0, color: "#d97706" },
      { id: "server", label: "Server", col: 2, row: 0, color: "#059669" },
    ],
    edges: [{ from: "request", to: "bucket", label: "costs 1 token" }, { from: "bucket", to: "server", label: "allowed" }],
    steps: [
      { activeNodes: ["bucket"], activeEdges: [], note: "A bucket holds tokens, refilling at a fixed rate (e.g. 10/sec)." },
      { activeNodes: ["request", "bucket"], activeEdges: [0], note: "A request arrives -- it costs 1 token from the bucket." },
      { activeNodes: ["bucket", "server"], activeEdges: [1], note: "The bucket had tokens available -- request is allowed through." },
      { activeNodes: ["request", "bucket"], activeEdges: [0], note: "If the bucket is empty, the next request is rejected (HTTP 429) until it refills." },
    ],
  },

  "oop-fundamentals-solid": {
    nodes: [
      { id: "caller", label: "Caller", col: 0, row: 0, color: "#0284c7" },
      { id: "obj", label: "Object", sublabel: "public methods", col: 1, row: 0, color: "#059669" },
      { id: "data", label: "Private Data", col: 1, row: 1, color: "#9333ea" },
    ],
    edges: [{ from: "caller", to: "obj", label: "calls method()" }, { from: "obj", to: "data", label: "reads/writes" }],
    steps: [
      { activeNodes: ["caller", "obj"], activeEdges: [0], note: "Callers only interact through public methods -- they can't reach in directly." },
      { activeNodes: ["obj", "data"], activeEdges: [1], note: "The object manages its own private data internally -- this is encapsulation." },
      { activeNodes: ["caller", "obj", "data"], activeEdges: [0, 1], note: "The internal representation can change later without breaking any caller, as long as the public methods behave the same." },
    ],
  },

  "essential-design-patterns": {
    nodes: [
      { id: "client", label: "Client", col: 0, row: 0, color: "#0284c7" },
      { id: "factory", label: "Factory", col: 1, row: 0, color: "#d97706" },
      { id: "circle", label: "Circle", col: 2, row: 0, color: "#059669" },
      { id: "square", label: "Square", col: 2, row: 1, color: "#9333ea" },
    ],
    edges: [{ from: "client", to: "factory", label: "create('circle')" }, { from: "factory", to: "circle" }, { from: "factory", to: "square" }],
    steps: [
      { activeNodes: ["client", "factory"], activeEdges: [0], note: "Client asks the factory for a shape, without knowing which concrete class it'll get." },
      { activeNodes: ["factory", "circle"], activeEdges: [1], note: "Factory decides: type is 'circle' -> create and return a Circle." },
      { activeNodes: ["factory", "square"], activeEdges: [2], note: "If instead type was 'square', the factory would return a Square -- the client's code doesn't change either way." },
    ],
  },
};
