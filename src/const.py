from config import Config
import os
from rules.ports import known_ports

class Const:
    def __init__(self):
        self.config = Config()
        self.RULES_PATH = self.config._get("settings", "Rules Path")
        self.known_ports = known_ports
        # operators
        self.operators = ['<','>', '=', '<=', '>=']
        self.sub_operators = ['+', '*', '!']
        # flags
        self.ip_flag_vals = [
            {'key':'M', 'value': 0x01}, 
            {'key':'D', 'value': 0x02}, 
            {'key':'MD', 'value': 0x03},
            {'key':'R', 'value': 0x04},
            {'key':'MDR', 'value': 0x07}
        ]
        self.tcp_flags = [
            { 'key':'F','name':'FIN','value':0x01 },
            { 'key':'S','name':'SYN','value':0x02 },
            { 'key':'R','name':'RST','value':0x04 },
            { 'key':'P','name':'PSH','value':0x08 },
            { 'key':'A','name':'ACK','value':0x10 },
            { 'key':'U','name':'URG','value':0x20 },
            { 'key':'E','name':'ECE','value':0x40 },
            { 'key':'C','name':'CWR','value':0x80 },
            { 'key':'1','name':'ECE','value':0x40 },
            { 'key':'2','name':'CWR','value':0x80 }
        ]

    def set_rules_path(self, path):
        self.RULES_PATH = path
        self.config._set("settings", "Rules Path", path)
