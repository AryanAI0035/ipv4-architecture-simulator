from typing import Tuple, Optional, List
from core.packet import IPPacket

def process_ip_packet(packet: IPPacket, routing_table: List[Tuple[str, int, str, str]], local_ip: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Module 2: Processing & Routing Module
    Validates checksum, decrements TTL, and performs longest-prefix match routing.
    Returns: (next_hop_ip, interface_name) or ("DELIVER", None) if destined for local host.
    """
    print(f"\n[2] PROCESSING: Packet reached node {local_ip}")
    h = packet.header
    
    # 1. Checksum Verification
    original_checksum = h.checksum
    h.checksum = 0
    if h.calculate_checksum() != original_checksum:
        print("    -> ERROR: Checksum mismatch. Packet dropped.")
        return None, None
    h.checksum = original_checksum
        
    # 2. Check if destined for us
    if h.dest_ip == local_ip:
        print(f"    -> Packet reached final destination ({local_ip})!")
        return "DELIVER", None
        
    # 3. Decrement TTL
    h.ttl -= 1
    if h.ttl == 0:
        print("    -> ERROR: TTL expired. Packet dropped (ICMP Time Exceeded).")
        return None, None
        
    # 4. Longest Prefix Match Routing
    print(f"    -> Routing lookup for {h.dest_ip}...")
    best_match = None
    best_mask = -1
    
    def ip_to_bin(ip):
        return ''.join([bin(int(x))[2:].zfill(8) for x in ip.split('.')])
        
    dest_bin = ip_to_bin(h.dest_ip)
    
    for prefix, mask, next_hop, interface in routing_table:
        pref_bin = ip_to_bin(prefix)[:mask]
        if dest_bin.startswith(pref_bin) and mask > best_mask:
            best_mask = mask
            best_match = (next_hop, interface)
                
    if best_match is None:
        print("    -> ERROR: No route to host. Packet dropped.")
        return None, None
        
    # Recompute checksum after TTL modification
    h.checksum = 0
    h.checksum = h.calculate_checksum()
    
    next_hop, interface = best_match
    print(f"    -> Route found: Next Hop = {next_hop}, Interface = {interface}")
    
    return next_hop, interface
