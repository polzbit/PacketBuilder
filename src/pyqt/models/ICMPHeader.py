from PyQt5.QtWidgets import QWidget, QGroupBox, QHBoxLayout, QVBoxLayout, QGridLayout, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from pyqt.models.LabelModel import Label
from pyqt.models.InputModel import Input
from pyqt.models.PacketField import PacketField
from utils import numConvert

class ICMPHeader(QWidget):
    ''' ICMP Header Component '''
    def __init__(self, master):
        QWidget.__init__(self, master)
        self.master = master
        # IP Details
        # ------------------------------ Widgets Setup ------------------------------ #
        # row 1
        self.icmp_type = PacketField(parent=self.master, name='pkt_field', text='Type\n(8 bits)', in_txt='8', width=80, height=40)
        self.code = PacketField(parent=self.master, name='pkt_field', text='Code\n(8 bits)', in_txt='0', width=80, height=40)
        self.checksum = PacketField(parent=self.master, name='pkt_field', text='ICMP Checksum\n(16 bits)', in_txt='0', width=160, height=40)

        self.icmp_id = PacketField(parent=self.master, name='pkt_field', text='ICMP Id\n(16 bits)', in_txt='0', width=160, height=40)
        self.icmp_seq = PacketField(parent=self.master, name='pkt_field', text='ICMP Sequence\n(16 bits)', in_txt='0', width=160, height=40)

        # ------------------------------ Layout Setup ------------------------------ #
        
        # row 1
        row = QHBoxLayout()
        row.addWidget(self.icmp_type)
        row.addWidget(self.code)
        row.addWidget(self.checksum)
        row.addStretch()
        # row 2
        row2 = QHBoxLayout()
        row2.addWidget(self.icmp_id)
        row2.addWidget(self.icmp_seq)
        row2.addStretch()

        main_layout = QVBoxLayout(self) 
        main_layout.addLayout(row)
        main_layout.addLayout(row2)
        main_layout.addStretch()
        # layout.setContentsMargins(60, 6, 60, 6)

    def set_header(self, icmp_type='8', code='0', checksum='0', icmp_id='0', icmp_seq='0'):
        ''' Set header values '''
        self.icmp_type.setText(icmp_type)
        self.code.setText(code)
        self.checksum.setText(checksum)
        self.icmp_id.setText(icmp_id)
        self.icmp_seq.setText(icmp_seq)
    
    def get_header(self):
        ''' Get header values '''
        return {
            'type': numConvert(self.icmp_type.text(), 'DEC'),
            'code': numConvert(self.code.text(), 'DEC'),
            'checksum': numConvert(self.checksum.text(), 'DEC'),
            'id': numConvert(self.icmp_id.text(), 'DEC'),
            'seq': numConvert(self.icmp_seq.text(), 'DEC')
        }
        
    def convert(self, to):
        ''' Convert header values '''
        self.set_header( 
            icmp_type=numConvert(self.icmp_type.text(), to, toString=True), 
            code=numConvert(self.code.text(), to, toString=True), 
            checksum=numConvert(self.checksum.text(), to, toString=True),
            icmp_id=numConvert(self.icmp_id.text(), to, toString=True),
            icmp_seq=numConvert(self.icmp_seq.text(), to, toString=True)
        )

