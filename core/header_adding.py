from core.packet import IPHeader, IPPacket

def encapsulate_ip_header(payload: bytes, dest_ip: str, src_ip: str, protocol: int, packet_id: int) -> IPPacket:
    """
    Module 1: Header Adding Module
    Takes a payload from the upper layer and prepends an IPv4 header.
    """
    print(f"\n[1] HEADER ADDING: Encapsulating payload of size {len(payload)} bytes")
    
    header = IPHeader(
        dest_ip=dest_ip,
        src_ip=src_ip,
        protocol=protocol,
        payload_len=len(payload),
        identification=packet_id
    )
    
    return IPPacket(header, payload)
