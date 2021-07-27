from PyQt5.QtWidgets import QWidget, QGroupBox, QHBoxLayout, QVBoxLayout, QGridLayout, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from pyqt.models.LabelModel import Label
from pyqt.models.InputModel import Input
from pyqt.models.PacketField import PacketField
from utils import numConvert

class EtherHeader(QWidget):
    ''' Ether Header Component '''
    def __init__(self, master):
        QWidget.__init__(self, master)
        self.master = master
        # IP Details
        # ------------------------------ Widgets Setup ------------------------------ #
        # row 1
        self.dst = PacketField(parent=self.master, name='pkt_field', text='Destination MAC\n(48 bits)', in_txt='', width=120, height=40)
        self.src = PacketField(parent=self.master, name='pkt_field', text='Source MAC\n(48 bits)', in_txt='', width=120, height=40)
        self.frame_type = PacketField(parent=self.master, name='pkt_field', text='Type\n(16 bits)', in_txt='36864', width=80, height=40)

        # ------------------------------ Layout Setup ------------------------------ #
        main_layout = QVBoxLayout() 
        # row 1
        row1 = QHBoxLayout()
        row1.addWidget(self.src)
        row1.addWidget(self.dst)
        row1.addWidget(self.frame_type)
        row1.addStretch()
        row1.setSpacing(0)

        main_layout.addLayout(row1)
        main_layout.addStretch()

        # layout.setContentsMargins(60, 6, 60, 6)
        self.setLayout(main_layout)
    
    def set_header(self, src='', dst='', ftype='36864'):
        ''' Set header values '''
        self.src.setText(src)
        self.dst.setText(dst)
        self.frame_type.setText(ftype)

    def get_header(self):
        ''' Get header values '''
        return {
            'src': numConvert(self.src.text(), 'DEC'),
            'dst': numConvert(self.dst.text(), 'DEC'),
            'type': numConvert(self.frame_type.text(), 'DEC'),
        }

    def convert(self, to):
        ''' Convert header values '''
        self.set_header( 
            src=numConvert(self.src.text(), to, toString=True), 
            dst=numConvert(self.dst.text(), to, toString=True), 
            ftype=numConvert(self.frame_type.text(), to, toString=True), 
        )