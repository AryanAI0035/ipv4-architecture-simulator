from typing import Optional
from core.packet import IPPacket

# Global state for reassembly buffer across packets
reassembly_table = {}

def reassemble_ip_fragment(fragment: IPPacket) -> Optional[bytes]:
    """
    Module 5: Reassembly Module
    Reconstructs an IP datagram from its fragments.
    Returns the fully reassembled payload if complete, else None.
    """
    print(f"\n[5] REASSEMBLY: Processing fragment...")
    h = fragment.header
    key = (h.src_ip, h.dest_ip, h.protocol, h.identification)
    
    if key not in reassembly_table:
        reassembly_table[key] = {'buffer': {}, 'bytes_rcv': 0, 'len': -1}
        
    entry = reassembly_table[key]
    byte_offset = h.fragment_offset * 8
    print(f"    -> Storing {len(fragment.payload)} bytes at offset {byte_offset}. MF={h.mf}")
    
    entry['buffer'][byte_offset] = fragment.payload
    entry['bytes_rcv'] += len(fragment.payload)
    
    if h.mf == 0:
        entry['len'] = byte_offset + len(fragment.payload)
        
    # Check if all bytes are received and length is known
    if entry['len'] != -1 and entry['bytes_rcv'] == entry['len']:
        expected_offset = 0
        complete_payload = b""
        
        # Verify contiguous chunks (no gaps)
        for off in sorted(entry['buffer'].keys()):
            if off != expected_offset:
                print("    -> Waiting for missing fragments...")
                return None
            chunk = entry['buffer'][off]
            complete_payload += chunk
            expected_offset += len(chunk)
            
        print("    -> SUCCESS: Datagram fully reassembled!")
        del reassembly_table[key]
        return complete_payload
        
    return None
