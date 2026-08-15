from typing import Optional
from core.packet import IPPacket

def forward_ip_packet(packet: IPPacket, next_hop: str, interface: dict) -> Optional[str]:
    """
    Module 3: Forwarding Module
    Checks interface status and resolves the effective next hop MAC/IP.
    Returns the effective next hop IP, or None if dropped.
    """
    print(f"\n[3] FORWARDING: Preparing to send out {interface['name']}")
    
    if interface['status'] != 'UP':
        print("    -> ERROR: Interface is DOWN. Packet dropped.")
        return None
        
    eff_next_hop = packet.header.dest_ip if next_hop == "0.0.0.0" else next_hop
    print(f"    -> Effective Next Hop MAC resolution for IP: {eff_next_hop}")
    
    return eff_next_hop
