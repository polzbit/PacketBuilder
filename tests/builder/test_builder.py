import unittest
import sys
sys.path.append('./src')
from src.builder.packet_manager import PacketManager

class TestBuilder(unittest.TestCase):

    def test_builder(self):
        manager = PacketManager(None)
        # test rules file
        self.assertTrue(manager.get_rules())
   

if __name__ == '__main__':
    unittest.main()