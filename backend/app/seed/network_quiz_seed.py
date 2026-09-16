"""
Real, deterministically-graded quiz questions for the Computer Networks
curriculum -- the practice/assessment layer this feature otherwise lacks (no
coding problems the way DSA has, no case studies the way System Design has).
Keyed by NetworkLesson slug, mirroring quiz_seed.py's shape exactly.
"""

NETWORK_QUIZZES = {
    "intro-to-networks": [
        {
            "question": "Why do almost all modern offices wire devices in a star topology instead of a bus?",
            "options": [
                "Star topology is cheaper to cable",
                "A star topology isolates failures -- one device or cable failing doesn't take down the whole network",
                "Bus topology cannot carry HTTP traffic",
                "Star topology doesn't need a central switch",
            ],
            "correct_index": 1,
            "explanation": "Bus topology shares one cable across every device, so a single break takes the whole segment offline; a star topology's central switch isolates each device's failure from the rest.",
        },
        {
            "question": "What's the main downside of a star topology?",
            "options": [
                "It cannot support more than a few devices",
                "The central hub/switch becomes a single point of failure",
                "Only one device can transmit at a time",
                "It requires wireless hardware",
            ],
            "correct_index": 1,
            "explanation": "Every device depends on the central switch -- if it fails, the whole star loses connectivity, unlike a mesh's redundant links.",
        },
    ],
    "osi-model": [
        {
            "question": "Which OSI layer is responsible for delivery between devices on the SAME local network (using MAC addresses)?",
            "options": ["Network (Layer 3)", "Data Link (Layer 2)", "Transport (Layer 4)", "Session (Layer 5)"],
            "correct_index": 1,
            "explanation": "The Data Link layer handles local delivery via MAC addresses; the Network layer (Layer 3) handles routing between different networks via IP.",
        },
        {
            "question": "A user can ping a server by IP address but the website won't load. What does the successful ping tell you?",
            "options": [
                "Nothing useful",
                "Layer 3 (Network) connectivity works, so the issue is likely higher up the stack",
                "The web server's code has a bug",
                "The DNS server is down",
            ],
            "correct_index": 1,
            "explanation": "A successful ping confirms routing/connectivity (Layer 3) is fine, narrowing the problem to something higher up -- like the web server not listening on the expected port, or an application misconfiguration.",
        },
    ],
    "tcp-ip-model": [
        {
            "question": "The TCP/IP model's 'Application' layer corresponds to which OSI layers combined?",
            "options": ["Physical + Data Link", "Network + Transport", "Application + Presentation + Session", "Only Application"],
            "correct_index": 2,
            "explanation": "TCP/IP collapses OSI's top three layers (Application, Presentation, Session) into one practical Application layer, since real protocols like HTTP handle all of that themselves.",
        },
        {
            "question": "Why is the TCP/IP model preferred over OSI for actually configuring real infrastructure?",
            "options": [
                "It's older and more established",
                "It maps directly onto real, configurable technology (IP addresses, TCP ports, Ethernet)",
                "It has more layers, so it's more precise",
                "OSI doesn't include a Transport layer",
            ],
            "correct_index": 1,
            "explanation": "TCP/IP's 4 layers reflect what's actually implemented and configured in real systems, unlike OSI's more abstract, finer-grained reference framework.",
        },
    ],
    "mac-ethernet-switches": [
        {
            "question": "What does ARP do?",
            "options": [
                "Encrypts traffic between two hosts",
                "Discovers which MAC address corresponds to a given IP address on the local network",
                "Routes packets between different networks",
                "Assigns IP addresses to new devices",
            ],
            "correct_index": 1,
            "explanation": "ARP (Address Resolution Protocol) lets a device find the MAC address behind an IP address it already knows, by broadcasting a request on the local network.",
        },
        {
            "question": "Why can't a switch route traffic between two different networks the way a router does?",
            "options": [
                "Switches are too slow",
                "A switch operates at Layer 2 using MAC addresses and has no concept of separate networks",
                "Switches only work with WiFi",
                "Switches require a firewall to function",
            ],
            "correct_index": 1,
            "explanation": "A switch's MAC-address-table forwarding is purely local-network (Layer 2); crossing between different networks is a Layer 3 (IP-based) job, which is what a router does.",
        },
    ],
    "ip-addressing-subnetting": [
        {
            "question": "In the address 192.168.1.42/24, what does the /24 tell you?",
            "options": [
                "The device is on port 24",
                "The first 24 bits identify the network; the remaining 8 bits identify the host",
                "There are 24 devices on this network",
                "The address is reserved for private use",
            ],
            "correct_index": 1,
            "explanation": "CIDR notation like /24 marks the boundary between the network portion and host portion of the address -- here, 24 bits for network, 8 bits (up to 254 usable) for hosts.",
        },
        {
            "question": "Why can't a device with a private IP address like 192.168.1.10 be reached directly from the public internet?",
            "options": [
                "Private IP ranges are reserved for use inside private networks and are never routed on the public internet directly",
                "Private IPs are always behind a firewall",
                "Private IPs only work over WiFi",
                "Private IPs expire after 24 hours",
            ],
            "correct_index": 0,
            "explanation": "Ranges like 192.168.0.0/16 are reserved specifically for private, internal use -- reaching them from outside requires NAT or a VPN, covered in later lessons.",
        },
    ],
    "routers-routing-algorithms": [
        {
            "question": "Does a single router along a packet's path typically know the packet's entire end-to-end route?",
            "options": [
                "Yes, every router computes the full path in advance",
                "No, each router only decides the single best next hop",
                "Only the source router knows the full path",
                "Only routers running BGP know the full path",
            ],
            "correct_index": 1,
            "explanation": "Routing is a series of independent, local decisions -- each router just picks the next hop that's closer to the destination, not the entire path.",
        },
        {
            "question": "Why might traffic take a longer-than-necessary path across the real internet?",
            "options": [
                "The internet always uses the shortest path",
                "BGP's routing decisions are policy-driven (business agreements between network operators), not purely distance-based",
                "Routers cannot calculate distance",
                "This never actually happens",
            ],
            "correct_index": 1,
            "explanation": "BGP connects independent networks based on real business/peering agreements, which can result in a technically longer but contractually preferred path being used.",
        },
    ],
    "nat-firewalls": [
        {
            "question": "What problem does NAT solve?",
            "options": [
                "It encrypts traffic between a device and the internet",
                "It lets many private devices share one public IP address",
                "It blocks unauthorized inbound connections",
                "It speeds up DNS lookups",
            ],
            "correct_index": 1,
            "explanation": "NAT rewrites each private device's outgoing traffic to share one public IP, directly addressing IPv4 address exhaustion -- access control is a separate job, handled by a firewall.",
        },
        {
            "question": "Is NAT alone a substitute for a real firewall?",
            "options": [
                "Yes, NAT fully secures a network",
                "No -- NAT happens to hide devices as a side effect, but a device with an explicit port-forward rule is just as reachable as one without NAT",
                "Yes, but only for UDP traffic",
                "No, NAT and firewalls are the exact same thing",
            ],
            "correct_index": 1,
            "explanation": "NAT's 'hiding' effect is a side effect of address sharing, not a deliberate access-control policy -- that's specifically what a firewall provides.",
        },
    ],
    "tcp-vs-udp": [
        {
            "question": "Why does a live video call typically use UDP instead of TCP?",
            "options": [
                "UDP is more secure",
                "Retransmitting a lost, late video frame (TCP's behavior) would arrive too late to be useful, so briefly glitching and moving on is preferable",
                "TCP cannot carry video data",
                "UDP guarantees delivery, unlike TCP",
            ],
            "correct_index": 1,
            "explanation": "UDP has no delivery guarantee, which is exactly right here: a resent, late frame would already be stale by the time it arrived.",
        },
        {
            "question": "Which of these is a real guarantee TCP provides that UDP does not?",
            "options": [
                "Lower latency",
                "Guaranteed, ordered delivery of data, with lost data automatically retransmitted",
                "Smaller packet headers",
                "No connection setup required",
            ],
            "correct_index": 1,
            "explanation": "TCP establishes a connection and guarantees complete, ordered delivery; UDP sends best-effort datagrams with no such guarantee.",
        },
    ],
    "tcp-handshake-lifecycle": [
        {
            "question": "What is confirmed once the TCP three-way handshake (SYN, SYN-ACK, ACK) completes?",
            "options": [
                "The data has already been fully transferred",
                "Both sides have confirmed they can send AND receive, and the connection is established",
                "The connection is encrypted",
                "The server has authenticated the client",
            ],
            "correct_index": 1,
            "explanation": "The handshake's job is purely to establish a reliable, two-way-confirmed connection before any actual application data flows.",
        },
        {
            "question": "Why does reusing an existing TCP connection (instead of opening a new one per request) improve performance?",
            "options": [
                "It avoids paying the handshake's round-trip cost again for every request",
                "It automatically compresses data",
                "It bypasses congestion control entirely",
                "It uses UDP instead of TCP",
            ],
            "correct_index": 0,
            "explanation": "Each new TCP connection pays a real round-trip cost for its handshake -- reusing one already-established connection amortizes that cost across multiple requests.",
        },
    ],
    "tcp-congestion-control": [
        {
            "question": "During TCP 'slow start,' how does the congestion window grow?",
            "options": [
                "It stays constant",
                "It roughly doubles every round trip, until a threshold or packet loss",
                "It grows by exactly 1 segment per second",
                "It shrinks gradually",
            ],
            "correct_index": 1,
            "explanation": "Slow start grows the congestion window exponentially (doubling each round trip) until either a threshold is reached or loss is detected -- at which point growth becomes much more cautious.",
        },
        {
            "question": "What does TCP typically do when it detects packet loss?",
            "options": [
                "Ignores it and keeps sending at the same rate",
                "Sharply cuts the congestion window (often by half), then resumes cautious growth",
                "Immediately closes the connection",
                "Switches to UDP",
            ],
            "correct_index": 1,
            "explanation": "TCP treats loss as a strong congestion signal and reacts with a sharp pullback (multiplicative decrease), then grows back cautiously -- the 'AIMD' pattern.",
        },
    ],
    "tls-ssl-https": [
        {
            "question": "Why does TLS use asymmetric encryption only briefly, during the handshake, rather than for all the actual data?",
            "options": [
                "Asymmetric encryption is illegal for bulk data",
                "Asymmetric encryption is computationally far more expensive, so it's used only to safely bootstrap a shared symmetric session key",
                "Symmetric encryption is less secure",
                "Browsers don't support asymmetric encryption for data transfer",
            ],
            "correct_index": 1,
            "explanation": "Asymmetric crypto's real job is safely establishing a shared secret; the much faster symmetric encryption then handles the actual bulk data transfer.",
        },
        {
            "question": "Besides encrypting data, what else does a TLS certificate provide?",
            "options": [
                "Faster page load times",
                "Authentication -- proof the server genuinely controls the domain it claims to be",
                "Automatic virus scanning",
                "Free hosting",
            ],
            "correct_index": 1,
            "explanation": "A certificate, signed by a trusted Certificate Authority, is what prevents a network attacker from impersonating a legitimate site -- encryption alone wouldn't stop that.",
        },
    ],
    "vpns-tunneling": [
        {
            "question": "What does a VPN hide from a user's local network/ISP that plain HTTPS does not?",
            "options": [
                "Nothing -- they provide identical protection",
                "Which destinations/sites are being reached at all, not just the content of one connection",
                "The user's password",
                "The device's MAC address",
            ],
            "correct_index": 1,
            "explanation": "HTTPS encrypts one connection's content but a local observer can still see which sites are being reached; a VPN tunnels all traffic to one server, hiding the actual destinations from the local network.",
        },
        {
            "question": "Can the VPN provider itself see a user's real, unencrypted traffic?",
            "options": [
                "Never -- VPNs are fully anonymous to everyone including the provider",
                "Yes, in principle -- since it's the VPN server that decrypts the tunnel to forward traffic onward",
                "Only if the user is on WiFi",
                "Only for UDP traffic",
            ],
            "correct_index": 1,
            "explanation": "The VPN provider decrypts the tunnel to forward traffic to its real destination, so genuine privacy depends heavily on trusting that specific provider.",
        },
    ],
    "socket-programming": [
        {
            "question": "What does a server's accept() call actually return?",
            "options": [
                "A copy of the entire listening socket",
                "A new, dedicated socket for that specific client connection, while the original listening socket keeps listening",
                "The client's IP address only",
                "Nothing -- accept() just logs the connection",
            ],
            "correct_index": 1,
            "explanation": "accept() hands off each new client to its own dedicated socket, freeing the original listening socket to keep accepting further new connections.",
        },
        {
            "question": "Why can't a single send() call on one side be assumed to match exactly one recv() call on the other?",
            "options": [
                "TCP sockets are stream-oriented, not message-oriented -- data can be combined or split across calls",
                "Sockets always drop half of every message",
                "send() and recv() must always be called the same number of times",
                "This is only true for UDP, not TCP",
            ],
            "correct_index": 0,
            "explanation": "TCP delivers a continuous byte stream, not discrete messages -- a receiver might get two sends combined in one recv(), or one send split across multiple recv() calls.",
        },
    ],
    "wireless-networking": [
        {
            "question": "Why does WiFi use CSMA/CA (Collision Avoidance) instead of wired Ethernet's CSMA/CD (Collision Detection)?",
            "options": [
                "WiFi doesn't support collision handling at all",
                "A wireless device generally can't reliably detect a collision while simultaneously transmitting over radio",
                "CSMA/CA is faster in every case",
                "CSMA/CD requires a cable, which WiFi doesn't have",
            ],
            "correct_index": 1,
            "explanation": "Since a radio transmitter can't easily listen for a collision while it's transmitting, WiFi instead waits a random backoff period beforehand to reduce the odds of colliding in the first place.",
        },
        {
            "question": "What is 'handoff' in a cellular network?",
            "options": [
                "A device switching from WiFi to cellular data",
                "Transferring an active connection from one cell tower to the next as a device moves, ideally without interruption",
                "A dropped call being redialed automatically",
                "Encrypting cellular traffic",
            ],
            "correct_index": 1,
            "explanation": "As a device moves between coverage areas, handoff transfers its active connection to the next tower, ideally seamlessly enough that the user never notices.",
        },
    ],
}
