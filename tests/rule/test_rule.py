import unittest
import sys
sys.path.append('./src')
from src.rules.protocols import get_protocol, Protocol
from src.rules.rule_parser import RuleParser

class TestRule(unittest.TestCase):

    def test_protocol(self):
        """ Test protocol function """
        bad = [ 'tcp', 'TCP', None, 'Udp', 'icmp', ' icmp' , '']
        good = [ 'tcp', 'TCP',  'Udp', 'icmp', ' icmp']
        for proto in good:
            self.assertIn(get_protocol(proto), Protocol)
    
    def test_parser():
        pass
        

if __name__ == '__main__':
    unittest.main()