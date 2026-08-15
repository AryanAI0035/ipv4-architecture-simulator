# IPv4 Architecture Simulator

A modular, educational Python simulation of the five core modules of the Internet Protocol (IPv4) architecture. This project serves as a practical demonstration for university-level networking courses.

## Architecture

The project strictly follows the structural decomposition of the IPv4 protocol, separated into distinct algorithmic modules:

- **Module 1: Header Adding** (`core/header_adding.py`) - Encapsulates Transport layer payloads with a simulated 20-byte IPv4 header and computes the 1's complement checksum.
- **Module 2: Processing & Routing** (`core/processing.py`) - Verifies packet integrity (checksum), manages the Time-To-Live (TTL) lifecycle, and executes longest-prefix match (LPM) routing table lookups.
- **Module 3: Forwarding** (`core/forwarding.py`) - Resolves whether the packet's next hop is a gateway router or a directly connected host.
- **Module 4: Fragmentation** (`core/fragmentation.py`) - Iteratively slices oversized IP datagrams into 8-byte aligned fragments to respect the Maximum Transmission Unit (MTU) of the outgoing interface.
- **Module 5: Reassembly** (`core/reassembly.py`) - A stateful receiver mechanism that buffers incoming, out-of-order fragments and mathematically reconstructs the original datagram.

## Project Structure

```
ipv4-architecture-simulator/
├── main.py                  # Demonstration script tying all modules together
├── core/                    # Core IPv4 modules
│   ├── packet.py            # Data structures (IPHeader, IPPacket)
│   ├── header_adding.py     
│   ├── processing.py        
│   ├── forwarding.py        
│   ├── fragmentation.py     
│   └── reassembly.py        
└── docs/                    # Mathematical formulation and academic documentation
    ├── IP_Algorithms.tex
    └── IP_Algorithms_Research_Paper.tex
```

## How to Run

Simply execute the main demonstration script:

```bash
python main.py
```

### What happens during the demonstration?
1. A large 1200-byte payload is encapsulated into an IP packet.
2. The packet is processed and routed to `eth0`.
3. Because `eth0` has a simulated MTU of 500 bytes, the Fragmentation Module splits the packet into 3 independent fragments.
4. The simulation transmits the 3 fragments **out-of-order** to the destination.
5. The Reassembly Module buffers the fragments and perfectly reconstructs the original payload upon receiving the final missing piece.
