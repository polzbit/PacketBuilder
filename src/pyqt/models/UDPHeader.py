from PyQt5.QtWidgets import QWidget, QGroupBox, QHBoxLayout, QVBoxLayout, QGridLayout, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from pyqt.models.LabelModel import Label
from pyqt.models.InputModel import Input
from pyqt.models.ButtonModel import Button
from utils import numConvert
from pyqt.models.PacketField import PacketField

class UDPHeader(QWidget):
    ''' Ucp Header Component '''
    def __init__(self, master):
        QWidget.__init__(self, master)
        self.master = master
        # IP Details
        # ------------------------------ Widgets Setup ------------------------------ #
        # row 1
        self.src = PacketField(parent=self.master, name='pkt_field', text='Source Port\n(16 bits)', in_txt='53', width=130, height=40)
        self.dst = PacketField(parent=self.master, name='pkt_field', text='Destination Port\n(16 bits)', in_txt='53', width=130, height=40)

        gen_src_btn = Button(parent=self, name='pkt_btn', icon="./src/pyqt/img/shuffle.png", width=30, height=30, iwidth=25, ihight=25, bold=False, tooltip='Generate port')
        gen_src_btn.clicked.connect(self.gen_src_port)
        gen_dst_btn = Button(parent=self, name='pkt_btn', icon="./src/pyqt/img/shuffle.png", width=30, height=30, iwidth=25, ihight=25, bold=False, tooltip='Generate port')
        gen_dst_btn.clicked.connect(self.gen_dst_port)
        # row 2
        self.length = PacketField(parent=self.master, name='pkt_field', text='Length\n(16 bits)', in_txt='', width=160, height=40)
        # row 3
        self.checksum = PacketField(parent=self.master, name='pkt_field', text='Checksum\n(16 bits)', in_txt='', width=160, height=40)

        # ------------------------------ Layout Setup ------------------------------ # 
        
        gen_lay1 = QVBoxLayout() 
        gen_lay1.addWidget(gen_src_btn, alignment=Qt.AlignBottom)
        gen_lay1.setContentsMargins(0, 0, 0, 15)
        gen_lay2 = QVBoxLayout() 
        gen_lay2.addWidget(gen_dst_btn, alignment=Qt.AlignBottom)
        gen_lay2.setContentsMargins(0, 0, 0, 15)

        # row 1
        row1 = QHBoxLayout()
        row1.addWidget(self.src)
        row1.addLayout(gen_lay1)
        row1.addWidget(self.dst)
        row1.addLayout(gen_lay2)
        row1.addStretch()
        # row 2
        row2 = QHBoxLayout()
        row2.addWidget(self.length)
        row2.addWidget(self.checksum)
        row2.addStretch()

        main_layout = QVBoxLayout()
        main_layout.addLayout(row1)
        main_layout.addLayout(row2)
        main_layout.addStretch()
        main_layout.setSpacing(0)
        self.setLayout(main_layout)

    def set_header(self, src='53', dst='53', length='', checksum=''):
        ''' Set header values '''
        self.src.setText(src)
        self.dst.setText(dst)
        self.length.setText(length)
        self.checksum.setText(checksum)

    def get_header(self):
        ''' Get header values '''
        return {
            'src': numConvert(self.src.text(), 'DEC'),
            'dst': numConvert(self.dst.text(), 'DEC'),
            'length': numConvert(self.length.text(), 'DEC'),
            'checksum': numConvert(self.checksum.text(), 'DEC')        
        }

    def convert(self, to):
        ''' Convert header values '''
        self.set_header( 
            src=numConvert(self.src.text(), to, toString=True), 
            dst=numConvert(self.dst.text(), to, toString=True), 
            length=numConvert(self.length.text(), to, toString=True), 
            checksum=numConvert(self.checksum.text(), to, toString=True)
        )

    def gen_src_port(self):
        # get covert type
        conv = self.master.toolbar.convert_modes.get_btn().text()
        self.src.setText(numConvert(str(self.master.manager.generate_port()), conv, toString=True))
    
    def gen_dst_port(self):
        # get covert type
        conv = self.master.toolbar.convert_modes.get_btn().text()
        self.dst.setText(numConvert(str(self.master.manager.generate_port()), conv, toString=True))