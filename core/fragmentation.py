from typing import List
from core.packet import IPHeader, IPPacket

def fragment_ip_packet(packet: IPPacket, interface: dict) -> List[IPPacket]:
    """
    Module 4: Fragmentation Module
    Fragments an oversized IP datagram based on the outgoing interface's MTU.
    Returns a list of IP fragments.
    """
    mtu = interface['mtu']
    h = packet.header
    print(f"\n[4] FRAGMENTATION: Checking MTU ({mtu} bytes) vs Packet Length ({h.total_length} bytes)")
    
    if h.total_length <= mtu:
        print("    -> No fragmentation needed.")
        return [packet]
        
    if h.df == 1:
        print("    -> ERROR: Packet too big but DF bit set. Dropped.")
        return []
        
    print("    -> Fragmentation required!")
    fragments = []
    
    # Payload bytes per fragment must be a multiple of 8
    data_per_frag = ((mtu - 20) // 8) * 8
    
    remaining_data = packet.payload
    offset = 0
    
    while len(remaining_data) > 0:
        chunk = remaining_data[:data_per_frag]
        remaining_data = remaining_data[data_per_frag:]
        mf = 1 if len(remaining_data) > 0 else 0
        
        frag_header = IPHeader(
            dest_ip=h.dest_ip, 
            src_ip=h.src_ip, 
            protocol=h.protocol,
            payload_len=len(chunk), 
            identification=h.identification,
            df=0, 
            mf=mf, 
            offset=offset // 8, 
            ttl=h.ttl
        )
        
        fragments.append(IPPacket(frag_header, chunk))
        print(f"    -> Created Fragment: Offset={offset}, PayloadLen={len(chunk)}, MF={mf}")
        offset += len(chunk)
        
    return fragments
