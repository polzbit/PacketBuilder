from scapy.all import IP
from rules.protocols import Protocol, get_protocol, find_protocol
from utils import is_public
from rules.content_args import content_args


class Rule:
    def __init__(self, rule_string):
        self.active = False
        self.content_args = content_args
        self.rule_string = rule_string
        self.data = self.parse_rule(rule_string)
        self.protocol = get_protocol(self.data["protocol"])

    def parse_rule(self, rule_string):
        ''' return rule object from rule string '''
        data = rule_string.split()
        options = rule_string[rule_string.find("(")+1:rule_string.find(")")]
        if data[0] == "#":
            data.pop(0)
        else:
            self.active = True
        
        parsed_data = self.parse_options(options)
        return {
            'action': data[0].strip(),
            'protocol': data[1].strip(),
            'source ip': data[2].strip(),
            'source port': data[3].strip(),
            'direction': data[4].strip(),
            'destination ip': data[5].strip(),
            'destination port': data[6].strip(),
            'options': parsed_data[0],
            'msg': parsed_data[1]
        }
    
    def parse_options(self, options_string):
        ''' return rule options from options string '''
        data = options_string.split(';')
        prev_content = ()
        prev_args = []
        options = []
        msg = ''
        for d in data:
            if d.find(':') > 0:
                obj = d.split(':')
                key = obj[0].strip()
                val = obj[1].strip()
                if key == 'content':
                    if prev_content != ():
                        options.append({
                            'name': 'content',
                            'value': prev_content[1].split(',')[0].strip('"'),
                            'args': self.get_args(prev_content[1], prev_args),
                        })
                        prev_args = []                    
                    prev_content = (key, val)
                elif key == 'msg':
                    msg = val
                else:
                    options.append({
                        'name': key,
                        'value': val,
                        'args': []
                    }) 
            elif prev_content != () and d.strip() in self.content_args:
                prev_args.append(d.strip())
            elif d.strip() == 'file_data' or d.strip() == 'pkt_data':
                options.append({
                        'name': d.strip(),
                        'value': '',
                        'args': []
                    }) 

        if prev_content != ():
            options.insert(0, {
                'name': 'content',
                'value': prev_content[1].split(',')[0].strip('"'),
                'args': self.get_args(prev_content[1], prev_args),
            })
        return (options, msg)
    
    def get_args(self, content, args=[]):
        ''' Get content args '''
        ret_args = args
        # payload_str = payload.load.decode("utf-8")
        if content.find(',') > 0:
            data = content.split(',')
            for d in data:
                ds = d.split()
                if len(ds) > 1 and ds[0] in self.content_args:
                    ret_args.append(d.strip())
                elif d.strip() in self.content_args:
                    ret_args.append(d.strip())
        return ret_args

    def to_json(self):
        return self.data