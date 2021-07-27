# IP Header 
# version: define ipv4 or ipv6
# ihl: size of header, min 5, max 15, depends on options count
# tos: The IP ToS header field in the innovaphone device configuration must be provided as hexadecimal value for the 8-bit ToS field of the IP packet
#   tos has 6 bit of DSCP and 2 bits ECN, define type of services. 0 is standard.
#   for more visit: https://wiki.innovaphone.com/index.php?title=Howto:Calculate_Values_for_Type_of_Service_%28ToS%29_from_DiffServ_or_DSCP_Values
# total length: defines the entire packet size in bytes, including header and data. 
#   The minimum size is 20 bytes (header without data) and the maximum is 65,535 bytes.
# id: used for uniquely identifying the group of fragments of a single IP datagram.
# flags 3-bits:
#       - Reserved: must be zero
#       - DF: dont fragment
#       - MF: more fragments
# frag offset: start at zero and increase on every fragment
# ttl: time to live specified in seconds, but time intervals less than 1 second are rounded up to 1.
# protocol: list of protocols: https://en.wikipedia.org/wiki/List_of_IP_protocol_numbers
#   - TCP: 0x06
#   - UDP: 0x11
#   - ICMP: 0x01 
# checksum: calculate the sum of each 16 bit value within the header, 
#    skipping only the checksum field itself.
# src address: source ip
# dst address: destination ip
# options: if options exists, options end with EOL (End of List = 0x00)
#
# TCP HEADER
# src port: source port
# dst port: destination port
# seq: if SYN flag = 1, corresponding sequence number
#      else SYN flag = 0, this sequence number
# ack: if ACK flag set, this represent the next sequence number
# data offset: size of the TCP header, minimum size of 20 bytes and maximum of 60 bytes, 
# allowing for up to 40 bytes of options in the header
# reserved: for future features
# flags: 
#   FIN = 0x01
#   SYN = 0x02
#   RST = 0x04
#   PSH = 0x08
#   ACK = 0x10
#   URG = 0x20
#   ECE = 0x40
#   CWR = 0x80
# ex: if p['TCP'].flags & FIN:
# window: size of the receive window
# checksum: tcp checksum
# urg: if the URG flag is set, 
# then this 16-bit field is an offset from the sequence number indicating the last urgent data byte
#
# UDP Header
# src port: src port
# dst port: dst port
# length: length in bytes of the UDP header and UDP data. 
# The minimum length is 8 bytes, the length of the header.
# maximum is 65,507 bytes
# checksum: udp checksum
#
# ICMP Header
# type: ICMP type, see https://en.wikipedia.org/wiki/Internet_Control_Message_Protocol#Control_messages
# code: ICMP subtype, see https://en.wikipedia.org/wiki/Internet_Control_Message_Protocol#Control_messages
# checksum: icmp checksum
# data: reset of header

class RuleParser:
    def __init__(self, master, rule):
        ''' Snort Rule Parser '''
        self.master = master
        self.rule = rule
        
        # ip vals
        self.ttl = 64
        self.frag_flags = 0
        self.proto = 0
        self.src_addr = self.master.manager.generate_ip(self.rule.data['source ip'])
        self.dst_addr = self.master.manager.generate_ip(self.rule.data['destination ip'])
        # tcp vals
        self.src_port = self.master.manager.generate_port(self.rule.data['source port'])
        self.dst_port = self.master.manager.generate_port(self.rule.data['destination port'])
        self.flags = 0
        self.seq = 0
        self.ack = 0
        self.win = 8192
        # udp vals
        # icmp vals
        self.itype = 8
        self.icode = 0
        self.icmp_seq = 0
        self.icmp_id = 0
        # payload vals
        self.content = bytearray()
        # start parser
        self.parse()
    
    def parse(self):
        ''' Parse rule data '''
        # check protocol
        self.proto = 0
        if self.rule.data['protocol'] == "tcp":
            self.proto = 6
        elif self.rule.data['protocol'] == "udp":
            self.proto = 17
        elif self.rule.data['protocol'] == "icmp":
            self.proto = 1
        # check options
        for index, opt in enumerate(self.rule.data['options']):
            if opt['name'] == 'content':
                self.content.extend(self.parse_content(opt['value'], opt['args']))
            elif opt['name'] == 'ttl':
                self.ttl = int(opt['value'])
            elif opt['name'] == 'fragbits':
                for flag_val in self.master.manager.const.ip_flag_vals:
                    if flag_val['key'] in opt['value']:
                        self.frag_flags += flag_val['value']
            elif opt['name'] == 'flags':
                data = opt['value'].split(',') 
                for d in data:
                    for flag in self.master.manager.const.tcp_flags:
                        if flag['key'] in d:
                            self.flags += flag['value']
            elif opt['name'] == 'seq':
                self.seq = int(opt['value'])
            elif opt['name'] == 'ack':
                self.ack = int(opt['value'])
            elif opt['name'] == 'itype':
                self.itype = int(opt['value'])
            elif opt['name'] == 'icode':
                code = ''
                for c in opt['value']:
                    if c not in self.master.manager.const.operators + self.master.manager.const.sub_operators:
                        code += c
                self.icode = int(code)
            elif opt['name'] == 'window':
                self.win = int(opt['value'])
            elif opt['name'] =='icmp_seq':
                self.icmp_seq = int(opt['value'])
            elif opt['name'] =='icmp_id':
                self.icmp_id = int(opt['value'])
            elif opt['name'] =='ip_proto':
                self.proto = int(opt['value'])
            elif opt['name'] =='sameip':
                self.dst_addr = self.src_addr
            elif opt['name'] == 'byte_test':
                # test byte at certin location
                pass

    def parse_content(self, content, args):
        data = bytearray()
        fillEnd = 0
        if content[0] != '!':
            # check args
            for arg in args:
                if 'offset' in arg:
                    # fill empty bytes until offset size
                    for i in range(int(arg.split()[1])):
                        data.extend(bytes.fromhex('00'))
                elif 'distance' in arg or 'isdataat' in arg:
                    val  = int(arg.split()[1])
                    if fillEnd < val:
                        fillEnd = val
            # extract bytes
            index = 0
            word = ''
            while index <= len(content) - 1:
                if content[index] == '|':
                    if word != '':
                        data.extend(word.encode())
                        word = ''
                    bytes_end = content.find('|', index+1)
                    if bytes_end != -1:
                        content_bytes = content[index+1 : bytes_end].split()
                        for b in content_bytes:
                            if len(b) == 2:
                                data.extend(bytes.fromhex(b))
                        index = bytes_end
                    else:
                        # no end char
                        pass
                else:
                    word += content[index]
                index += 1
            if word != '':
                data.extend(word.encode())
        
        if fillEnd:
            for i in range(fillEnd):
                data.extend(bytes.fromhex('00'))
        return bytes(data)
