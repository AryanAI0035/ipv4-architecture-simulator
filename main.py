import random
from core.header_adding import encapsulate_ip_header
from core.processing import process_ip_packet
from core.forwarding import forward_ip_packet
from core.fragmentation import fragment_ip_packet
from core.reassembly import reassemble_ip_fragment

def main():
    print("=== IPv4 ARCHITECTURE MODULE DEMONSTRATION ===")
    
    # ---------------------------------------------------------
    # 0. Setup Network Environment
    # ---------------------------------------------------------
    local_host = "192.168.1.10"
    dest_host = "10.0.0.5"
    
    # Routing Table: (Prefix, Mask, Next_Hop, Interface_Name)
    routing_table = [
        ("10.0.0.0", 8, "192.168.1.1", "eth0"),      # Default route to gateway
        ("192.168.1.0", 24, "0.0.0.0", "eth1"),      # Directly connected
    ]
    
    # Interfaces dictionary
    interfaces = {
        "eth0": {"name": "eth0", "status": "UP", "mtu": 500}, # Small MTU to force fragmentation
        "eth1": {"name": "eth1", "status": "UP", "mtu": 1500}
    }
    
    # Payload of 1200 bytes (will need fragmentation on eth0's 500 MTU)
    original_payload = b"Hello IPv4" * 120
    
    # ---------------------------------------------------------
    # 1. Module 1: Header Adding
    # ---------------------------------------------------------
    packet = encapsulate_ip_header(original_payload, dest_host, local_host, protocol=6, packet_id=9999)
    
    # ---------------------------------------------------------
    # 2. Module 2: Processing (at sender/router)
    # ---------------------------------------------------------
    next_hop, iface_name = process_ip_packet(packet, routing_table, local_host)
    
    if next_hop and next_hop != "DELIVER":
        iface = interfaces[iface_name]
        
        # ---------------------------------------------------------
        # 3. Module 3: Forwarding
        # ---------------------------------------------------------
        eff_next_hop = forward_ip_packet(packet, next_hop, iface)
        
        if eff_next_hop:
            # ---------------------------------------------------------
            # 4. Module 4: Fragmentation
            # ---------------------------------------------------------
            fragments = fragment_ip_packet(packet, iface)
            
            print(f"\n--- SIMULATING NETWORK TRANSMISSION OF {len(fragments)} FRAGMENTS ---")
            
            # Shuffle fragments to prove reassembly handles out-of-order delivery gracefully
            random.seed(42) # Deterministic shuffle for repeatable output
            random.shuffle(fragments)
            
            reassembled_data = None
            
            for i, frag in enumerate(fragments):
                print(f"\n>> Receiving fragment {i+1}/{len(fragments)} out of order")
                
                # Processing at destination
                res, _ = process_ip_packet(frag, routing_table, dest_host)
                
                if res == "DELIVER":
                    # ---------------------------------------------------------
                    # 5. Module 5: Reassembly
                    # ---------------------------------------------------------
                    out = reassemble_ip_fragment(frag)
                    if out:
                        reassembled_data = out
                        
            # ---------------------------------------------------------
            # Final Verification
            # ---------------------------------------------------------
            print("\n=== FINAL VERIFICATION ===")
            if reassembled_data == original_payload:
                print("All modules executed correctly! Reassembled payload exactly matches the original 1200-byte payload.")
            else:
                print("Error: Reassembled payload does NOT match original.")

if __name__ == "__main__":
    main()
