class IPHeader:
    def __init__(self, dest_ip, src_ip, protocol, payload_len, identification, df=0, mf=0, offset=0, ttl=64):
        self.version = 4
        self.ihl = 5
        self.tos = 0
        self.total_length = 20 + payload_len
        self.identification = identification
        self.df = df
        self.mf = mf
        self.fragment_offset = offset
        self.ttl = ttl
        self.protocol = protocol
        self.src_ip = src_ip
        self.dest_ip = dest_ip
        self.checksum = 0
        self.checksum = self.calculate_checksum()

    def calculate_checksum(self):
        """
        Simulated checksum calculation over 20-byte header.
        Packs fields into 16-bit words and performs 1s complement addition.
        """
        word1 = (self.version << 12) | (self.ihl << 8) | self.tos
        word2 = self.total_length
        word3 = self.identification
        word4 = (self.df << 14) | (self.mf << 13) | self.fragment_offset
        word5 = (self.ttl << 8) | self.protocol
        
        def ip2int(ip):
            parts = list(map(int, ip.split('.')))
            return (parts[0]<<24) + (parts[1]<<16) + (parts[2]<<8) + parts[3]
            
        src = ip2int(self.src_ip)
        dest = ip2int(self.dest_ip)
        
        word6 = (src >> 16) & 0xFFFF
        word7 = src & 0xFFFF
        word8 = (dest >> 16) & 0xFFFF
        word9 = dest & 0xFFFF
        
        words = [word1, word2, word3, word4, word5, word6, word7, word8, word9]
        total = sum(words)
        
        while total > 0xFFFF:
            total = (total & 0xFFFF) + (total >> 16)
            
        return ~total & 0xFFFF


class IPPacket:
    def __init__(self, header: IPHeader, payload: bytes):
        self.header = header
        self.payload = payload
