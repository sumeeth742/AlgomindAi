import type { FlowEdge, FlowNode, FlowStep } from "@/components/visualizers/FlowDiagram";

export interface NetworkVisualization {
  nodes: FlowNode[];
  edges: FlowEdge[];
  steps: FlowStep[];
}

// One diagram per Networks lesson, keyed by lesson slug -- same shape and
// intent as SD_VISUALIZATIONS (sdVisualizations.ts): a real, technically
// accurate step-by-step walkthrough of how the protocol/mechanism actually
// behaves, not a decorative illustration. Every message and field named here
// (sequence numbers, cwnd growth, NAT port rewriting, MAC learning, etc.) is
// real protocol behavior, not invented for effect.
export const NETWORK_VISUALIZATIONS: Record<string, NetworkVisualization> = {
  "tcp-handshake-lifecycle": {
    nodes: [
      { id: "client", label: "Client", col: 0, row: 0, color: "#0284c7" },
      { id: "server", label: "Server", col: 1, row: 0, color: "#059669" },
    ],
    edges: [
      { from: "client", to: "server", label: "SYN (seq=x)" },
      { from: "server", to: "client", label: "SYN-ACK (seq=y, ack=x+1)" },
      { from: "client", to: "server", label: "ACK (ack=y+1)" },
      { from: "client", to: "server", label: "data flows both ways", dashed: true },
      { from: "client", to: "server", label: "FIN (client done sending)" },
      { from: "server", to: "client", label: "ACK" },
      { from: "server", to: "client", label: "FIN (server done sending)" },
      { from: "client", to: "server", label: "ACK -- connection closed" },
    ],
    steps: [
      { activeNodes: ["client"], activeEdges: [], note: "Client wants to open a reliable connection to the server." },
      { activeEdges: [0], note: "Client sends SYN with an initial sequence number x -- \"I want to connect, starting at seq x.\"" },
      { activeEdges: [1], note: "Server replies SYN-ACK: its own sequence number y, and ack=x+1 acknowledging the client's SYN." },
      { activeEdges: [2], note: "Client sends ACK with ack=y+1 -- both sides have confirmed the connection. This is the \"three-way\" handshake." },
      { activeEdges: [3], note: "The connection is established -- application data now flows in both directions." },
      { activeEdges: [4], note: "When the client is done sending, it sends FIN." },
      { activeEdges: [5], note: "Server ACKs the FIN, but may still have data left to send -- TCP close is half-duplex first." },
      { activeEdges: [6], note: "Once the server is also done sending, it sends its own FIN." },
      { activeEdges: [7], note: "Client ACKs the server's FIN -- the connection is now fully closed on both sides." },
    ],
  },

  "tcp-vs-udp": {
    nodes: [
      { id: "sender", label: "Sender", col: 0, row: 0, color: "#0284c7" },
      { id: "receiver", label: "Receiver", col: 1, row: 0, color: "#059669" },
    ],
    edges: [
      { from: "sender", to: "receiver", label: "TCP: handshake first" },
      { from: "sender", to: "receiver", label: "TCP: data + seq numbers" },
      { from: "receiver", to: "sender", label: "TCP: ACK (or resend on loss)" },
      { from: "sender", to: "receiver", label: "UDP: datagram, no handshake" },
      { from: "sender", to: "receiver", label: "UDP: if lost, nobody resends it" },
    ],
    steps: [
      { activeNodes: ["sender", "receiver"], activeEdges: [], note: "Same two hosts, two very different transport choices." },
      { activeEdges: [0], note: "TCP first performs a handshake to establish a reliable, ordered connection before any data is sent." },
      { activeEdges: [1], note: "TCP then sends data carrying sequence numbers, so the receiver can detect loss and reorder if needed." },
      { activeEdges: [2], note: "The receiver ACKs; if an ACK doesn't arrive in time, TCP retransmits -- reliable, but with handshake and retransmission overhead." },
      { activeEdges: [3], note: "UDP skips all of that -- it just sends a datagram directly, no handshake, no connection state to maintain." },
      { activeEdges: [4], note: "If a UDP datagram is lost, nothing resends it automatically -- the application has to handle that itself, if it even cares (e.g. live video can just skip a frame)." },
    ],
  },

  "tcp-congestion-control": {
    nodes: [
      { id: "sender", label: "Sender", col: 0, row: 0, color: "#0284c7" },
      { id: "receiver", label: "Receiver", col: 1, row: 0, color: "#059669" },
    ],
    edges: [
      { from: "sender", to: "receiver", label: "cwnd = 1 segment" },
      { from: "sender", to: "receiver", label: "cwnd = 2 (doubled)" },
      { from: "sender", to: "receiver", label: "cwnd = 4 (doubled again)" },
      { from: "sender", to: "receiver", label: "packet lost!" },
      { from: "sender", to: "receiver", label: "cwnd halved, linear growth resumes" },
    ],
    steps: [
      { activeNodes: ["sender", "receiver"], activeEdges: [], note: "TCP doesn't know the network's real capacity upfront -- it has to probe for it." },
      { activeEdges: [0], note: "Slow start: begins with a small congestion window (cwnd), e.g. 1 segment in flight." },
      { activeEdges: [1], note: "Each round-trip with no loss, cwnd roughly doubles -- exponential growth." },
      { activeEdges: [2], note: "Growth continues until a threshold is crossed (switching to slower linear growth) or a packet is lost." },
      { activeEdges: [3], note: "A lost packet is treated as a real congestion signal -- something on the path is overwhelmed." },
      { activeEdges: [4], note: "TCP reacts with a sharp multiplicative decrease, then grows linearly again -- this repeating saw-tooth IS TCP congestion control." },
    ],
  },

  "tls-ssl-https": {
    nodes: [
      { id: "client", label: "Client", col: 0, row: 0, color: "#0284c7" },
      { id: "server", label: "Server", col: 1, row: 0, color: "#059669" },
    ],
    edges: [
      { from: "client", to: "server", label: "ClientHello (supported ciphers)" },
      { from: "server", to: "client", label: "ServerHello + certificate" },
      { from: "client", to: "server", label: "verify cert, send key material" },
      { from: "server", to: "client", label: "session key derived" },
      { from: "client", to: "server", label: "encrypted application data" },
    ],
    steps: [
      { activeNodes: ["client", "server"], activeEdges: [], note: "Client wants to talk to the server securely -- this is what happens before HTTPS shows the padlock." },
      { activeEdges: [0], note: "ClientHello: client proposes a TLS version and the ciphers it supports." },
      { activeEdges: [1], note: "ServerHello: server picks a cipher and sends back its certificate -- its identity plus a public key." },
      { activeEdges: [2], note: "Client verifies the certificate against a trusted Certificate Authority, then helps establish a shared secret." },
      { activeEdges: [3], note: "Both sides now derive the same symmetric session key -- the slower asymmetric crypto was only used to set this up." },
      { activeEdges: [4], note: "From here on, everything is encrypted with the fast symmetric session key -- this is the padlock icon's actual guarantee." },
    ],
  },

  "nat-firewalls": {
    nodes: [
      { id: "host", label: "Host", sublabel: "192.168.1.5:5000", col: 0, row: 0, color: "#0284c7" },
      { id: "nat", label: "NAT Router", col: 1, row: 0, color: "#d97706" },
      { id: "server", label: "Internet Server", col: 2, row: 0, color: "#059669" },
    ],
    edges: [
      { from: "host", to: "nat", label: "src 192.168.1.5:5000" },
      { from: "nat", to: "server", label: "src rewritten to 8.2.4.6:40001" },
      { from: "server", to: "nat", label: "reply to 8.2.4.6:40001" },
      { from: "nat", to: "host", label: "dst rewritten back to 192.168.1.5:5000" },
    ],
    steps: [
      { activeNodes: ["host"], activeEdges: [], note: "A host on a private network (192.168.1.5) wants to reach a server on the public internet." },
      { activeEdges: [0], note: "The host sends a packet from its private IP:port straight to the NAT router -- its default gateway." },
      { activeEdges: [1], note: "NAT rewrites the source to its own public IP and a new port, and remembers this mapping in a translation table." },
      { activeEdges: [2], note: "The server only ever sees the NAT's public address -- it has no idea the private host exists -- and replies there." },
      { activeEdges: [3], note: "NAT looks up the mapping for that port, rewrites the destination back to the private IP:port, and forwards it home." },
    ],
  },

  "routers-routing-algorithms": {
    nodes: [
      { id: "source", label: "Source", col: 0, row: 0, color: "#0284c7" },
      { id: "routerA", label: "Router A", col: 1, row: 0, color: "#d97706" },
      { id: "routerB", label: "Router B", col: 2, row: 0, color: "#d97706" },
      { id: "dest", label: "Destination", col: 3, row: 0, color: "#059669" },
    ],
    edges: [
      { from: "source", to: "routerA" },
      { from: "routerA", to: "routerB" },
      { from: "routerB", to: "dest" },
    ],
    steps: [
      { activeNodes: ["source"], activeEdges: [], note: "A packet needs to reach a destination on a different network entirely." },
      { activeEdges: [0], note: "Source sends the packet to its default gateway -- Router A." },
      { activeEdges: [1], note: "Router A reads the destination IP, checks its own routing table for the best next hop, and forwards to Router B -- just the next hop, not the whole path." },
      { activeEdges: [2], note: "Router B does the same lookup and forwards directly to the destination, now one hop away." },
      { activeNodes: ["source", "routerA", "routerB", "dest"], activeEdges: [0, 1, 2], note: "No router ever knew the full path -- the route emerged hop by hop, and TTL decrements at each one to prevent infinite loops." },
    ],
  },

  "socket-programming": {
    nodes: [
      { id: "client", label: "Client App", col: 0, row: 0, color: "#0284c7" },
      { id: "socket", label: "Server Socket", sublabel: "bind + listen", col: 1, row: 0, color: "#d97706" },
      { id: "server", label: "Server App", col: 2, row: 0, color: "#059669" },
    ],
    edges: [
      { from: "server", to: "socket", label: "bind(port) + listen()" },
      { from: "client", to: "socket", label: "connect()" },
      { from: "socket", to: "server", label: "accept() -> new connected socket" },
      { from: "client", to: "server", label: "read()/write() data" },
      { from: "client", to: "server", label: "close()" },
    ],
    steps: [
      { activeNodes: ["server"], activeEdges: [], note: "The server process creates a socket, calls bind() to claim a port, and listen() to start accepting connections." },
      { activeEdges: [0], note: "The socket is now in a \"listening\" state, passively waiting for someone to connect." },
      { activeEdges: [1], note: "The client creates its own socket and calls connect() to the server's IP:port -- under the hood this triggers a real TCP three-way handshake." },
      { activeEdges: [2], note: "The server's accept() returns a brand-new connected socket dedicated to this one client -- the original listening socket goes right back to waiting for the next connection." },
      { activeEdges: [3], note: "From here, both sides just read()/write() bytes through their own socket -- to the application it feels like a simple file-like stream." },
      { activeEdges: [4], note: "Either side calls close() when done, tearing the connection down." },
    ],
  },

  "mac-ethernet-switches": {
    nodes: [
      { id: "hostA", label: "Host A", col: 0, row: 0, color: "#0284c7" },
      { id: "switch", label: "Switch", col: 1, row: 0, color: "#d97706" },
      { id: "hostB", label: "Host B", col: 2, row: 0, color: "#059669" },
      { id: "hostC", label: "Host C", col: 2, row: 1, color: "#059669" },
    ],
    edges: [
      { from: "hostA", to: "switch", label: "frame, dst = MAC(B)" },
      { from: "switch", to: "hostB", label: "flooded copy" },
      { from: "switch", to: "hostC", label: "flooded copy (wasted)" },
      { from: "switch", to: "hostB", label: "forwarded directly (learned)" },
    ],
    steps: [
      { activeNodes: ["hostA"], activeEdges: [], note: "Host A sends a frame addressed to Host B's MAC address -- but the switch doesn't yet know which port Host B is on." },
      { activeEdges: [0], note: "The frame arrives at the switch. It checks its MAC address table for Host B's address -- not found yet." },
      { activeEdges: [1, 2], note: "Unknown destination -> the switch floods the frame out every port except the one it arrived on, so Host B (and, wastefully, Host C) both receive it." },
      { activeNodes: ["hostA", "switch"], activeEdges: [], note: "At the same time, the switch learns Host A's MAC from the frame's source address, and remembers which port it arrived on." },
      { activeEdges: [3], note: "Once Host B's MAC is learned too, the next frame addressed to it is forwarded directly to just the right port -- no more flooding needed for that address." },
    ],
  },
};
