from threads.qthread_manager import QThreadManager
from rules.rule import Rule
from rules.protocols import get_protocol
from scapy.all import Ether, IP, TCP, UDP, ICMP, send, Raw
from const import Const
from random import randrange, choice

class PacketManager:
    def __init__(self, master):
        ''' Packet Maker '''
        self.master = master
        self.const = Const()
        self.rules = []
        self.thread_manager = QThreadManager(self.master)
    
    def load_rules(self):
        ''' Start loading rules thread '''
        self.thread_manager._start("loading_rules", self._load_rules, self.on_loading_fin)

    def on_loading_fin(self, res):
        ''' hide preloader on loading finish '''
        self.master.preloader_window.signals.onFin.emit()
        
    def _load_rules(self, stop_condition, **kwargs):
        ''' Load Rules File '''
        f = self.get_rules()
        print("[ IDS ] Loading Rules...")
        for index, line in enumerate(f):
            if stop_condition(line):
                return
            if index > 16:
                r = Rule(line)
                self.rules.append(r)
                self.master.signals.addRule.emit([len(self.rules), r.data['msg'], r.data['protocol']])
        print("[ IDS ] Loading Finished.")
    
    def get_rules(self):
        ''' get rules from file '''
        with open(self.const.RULES_PATH, 'r') as f:
            return f.readlines()

    def on_send(self, count=1):
        ''' Start send packet thread '''
        self.thread_manager._start("send_pkt", self.send, self.on_send_fin, count=count)

    def on_send_fin(self, res):
        self.master.signals.onFinSend.emit(res)

    def send(self, stop_condition, **kwargs):
        ''' Send packet using scapy '''
        count = kwargs.get('count')
        modes = self.master.get_modes()
        packet = None
        if 'IPv4' in modes['type_mode']:
            ip_data = self.master.ip_header.get_header()
            # print(ip_data)
            packet = IP(
                version=ip_data['version'], 
                ihl=ip_data['ihl'], 
                tos=ip_data['tos'], 
                len=ip_data['length'], 
                id=ip_data['id'], 
                flags=ip_data['flags'], 
                frag=ip_data['frag'], 
                ttl=ip_data['ttl'], 
                proto=ip_data['proto'], 
                chksum=ip_data['checksum'],
                src=ip_data['src'], 
                dst=ip_data['dst']
            )
        if modes['type_mode'] == 'IPv4 TCP':
            # send tcp header
            tcp_data = self.master.tcp_header.get_header()
            # print(tcp_data)
            packet = packet/TCP(
                sport=tcp_data['src'], 
                dport=tcp_data['dst'], 
                seq=tcp_data['seq'], 
                ack=tcp_data['ack'], 
                dataofs=tcp_data['offset'], 
                chksum=tcp_data['checksum'],
                reserved=tcp_data['reserved'], 
                flags=tcp_data['flags'],
                window=tcp_data['window'],
                urgptr=tcp_data['urg'] 
            )
        elif modes['type_mode'] == 'IPv4 UDP':
            # send udp header
            udp_data = self.master.udp_header.get_header()
            packet = packet/UDP(
                sport=udp_data['src'], 
                dport=udp_data['dst'], 
                len=udp_data['length'], 
            )
        elif modes['type_mode'] == 'ICMP':
            # send icmp header
            icmp_data = self.master.icmp_header.get_header()
            packet = packet/ICMP(
                type=icmp_data['type'], 
                code=icmp_data['code'], 
            )
        elif modes['type_mode'] == "Frame":
            # send ethernet frame header
            print('frame')
            ether_data = self.master.ether_header.get_header()
            packet = Ether(
                dst=ether_data['dst'], 
                src=ether_data['src'],
                type=ether_data['type']
            )

        #del packet[IP].chksum

        if modes['payload_mode']:
            # add payload
            payload_data = self.master.payload_header.get_header()
            packet = packet/payload_data['load']

        if packet != None:
            packet.show2()
            send(packet ,count=count)
        else:
            print('[!] No Packet')
        return count

    def generate_public_addr(self):
        ''' Generate Public IP '''
        octs = ['10', '172' , '192']
        first = choice([i for i in range(0,256) if i not in octs])
        return f"{first}.{str(randrange(0, 256))}.{str(randrange(0, 256))}.{str(randrange(0, 256))}"

    def generate_private_addr(self):
        ''' Generate Private IP '''
        octs = ['10', '172' , '192']
        first = octs[randrange(0, len(octs))]
        if int(octs[0]) == 10:
            return f"10.{str(randrange(0, 256))}.{str(randrange(0, 256))}.{str(randrange(0, 256))}"
        elif int(octs[0]) == 172:
            return f"172.{str(randrange(16, 32))}.{str(randrange(0, 256))}.{str(randrange(0, 256))}"
        elif int(octs[0]) == 192:
            return f"192.168.{str(randrange(0, 256))}.{str(randrange(0, 256))}"
    
    def generate_ip(self, ip_type):
        ''' Generate Rule IP '''
        ip = '0.0.0.0'
        if ip_type == "$EXTERNAL_NET":
            ip = self.generate_public_addr()
        elif ip_type == "$HOME_NET" or ip_type == "$TELNET_SERVERS" or ip_type == "$SMTP_SERVERS" or ip_type == "$HTTP_SERVERS" or ip_type == "$SQL_SERVERS" or ip_type == "$SIP_SERVERS":
            ip = self.generate_private_addr()
        else:
            ip = ip_type
        return ip

    def generate_port(self, port_type=''):
        ''' Generate Rule Port '''
        if ':' in port_type:
            port_type= port_type.replace(':', '')
            return self.generate_port(port_type)
        port = randrange(0, 65535)
        if port_type[0] == '[':
            ports_list = port_type[1:port_type.find(']')].split(',')
            port = ports_list[randrange(0, len(ports_list))]
            port = int(port)
        if port_type.isdigit():
            port = int(port_type)
        else:
            for p in self.const.known_ports:
                if p['name'] == port_type:
                    port = p['ports'][randrange(0, len(p['ports']))]
                    break
        return port
        
