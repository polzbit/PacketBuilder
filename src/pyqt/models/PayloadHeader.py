from PyQt5.QtWidgets import QWidget, QGroupBox, QHBoxLayout, QVBoxLayout, QGridLayout, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from pyqt.models.LabelModel import Label
from pyqt.models.InputModel import Input
from utils import numConvert
from pyqt.models.PacketField import PacketField

class PayloadHeader(QWidget):
    ''' Payload Header Component '''
    def __init__(self, master):
        QWidget.__init__(self, master)
        self.master = master
        # IP Details
        # ------------------------------ Widgets Setup ------------------------------ #
        # row 1
        self.load = PacketField(parent=self.master, name='pkt_field', text='Load', in_txt='', width=320, height=40, in_height=200, align=Qt.AlignLeft|Qt.AlignTop)

        # ------------------------------ Layout Setup ------------------------------ #
        main_layout = QVBoxLayout() 
        # row 1
        row1 = QHBoxLayout()
        row1.addWidget(self.load)
        row1.addStretch()

        main_layout.addLayout(row1)
        main_layout.addStretch()

        
        self.setLayout(main_layout)

    def set_header(self, load=''):
        ''' Set header values '''
        self.load.setText(load)

    def get_header(self):
        ''' Get header values '''
        payload = bytearray()
        for hex_num in self.load.text().split():
            payload.extend(bytes.fromhex(hex_num))
        return {
            'load': bytes(payload)
        }
        
    def convert(self, to):
        ''' Convert header values '''
        self.set_header( 
            load=self.load.text()
        )