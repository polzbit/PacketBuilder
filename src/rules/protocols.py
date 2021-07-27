from enum import Enum
from scapy.all import TCP, UDP, ICMP, IP 

class Protocol(Enum):
    """ IP packet Protocols """
    TCP = TCP
    UDP = UDP
    ICMP = ICMP
    IP = IP

def get_protocol(protocol_name):
    """ Return Protocol corresponding to the string """
    if protocol_name != None and protocol_name.strip() != '':
        protocol_name = protocol_name.lower().strip()
        for data in Protocol:
            if data.name.lower() == protocol_name:
                return data
    raise ValueError(f"Invalid rule : invalid protocol type: '{protocol_name}'.")

def find_protocol(pkt):
    if pkt.haslayer(TCP):
        return Protocol.TCP
    elif pkt.haslayer(UDP):
        return Protocol.UDP
    elif pkt.haslayer(ICMP):
        return Protocol.ICMP
    else:
        return Protocol.IP

