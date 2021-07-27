from PyQt5.QtWidgets import QWidget, QGroupBox, QHBoxLayout, QVBoxLayout, QGridLayout, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from pyqt.models.LabelModel import Label
from pyqt.models.InputModel import Input
from pyqt.models.ButtonModel import Button
from utils import numConvert
from pyqt.models.PacketField import PacketField

class TCPHeader(QWidget):
    ''' Tcp Header Component '''
    def __init__(self, master):
        QWidget.__init__(self, master)
        self.master = master
        # IP Details
        # ------------------------------ Widgets Setup ------------------------------ #
        # row 1
        self.src = PacketField(parent=self.master, name='pkt_field', text='Source Port\n(16 bits)', in_txt='20', width=130, height=40)
        self.dst = PacketField(parent=self.master, name='pkt_field', text='Destination Port\n(16 bits)', in_txt='80', width=130, height=40)

        gen_src_btn = Button(parent=self, name='pkt_btn', icon="./src/pyqt/img/shuffle.png", width=30, height=30, iwidth=25, ihight=25, bold=False, tooltip='Generate port')
        gen_src_btn.clicked.connect(self.gen_src_port)
        gen_dst_btn = Button(parent=self, name='pkt_btn', icon="./src/pyqt/img/shuffle.png", width=30, height=30, iwidth=25, ihight=25, bold=False, tooltip='Generate port')
        gen_dst_btn.clicked.connect(self.gen_dst_port)
        # row 2
        self.seq = PacketField(parent=self.master, name='pkt_field', text='Sequence Number\n(32 bits)', in_txt='0', width=320, height=40)

        # row 3
        self.ack = PacketField(parent=self.master, name='pkt_field', text='Acknowledge Number\n(32 bits)', in_txt='0', width=320, height=40)

        # row 4
        self.offset = PacketField(parent=self.master, name='pkt_field', text='Offset\n(4 bits)', in_txt='0', width=40, height=40)
        self.reserved = PacketField(parent=self.master, name='pkt_field', text='Reserved\n(6 bits)', in_txt='0', width=60, height=40)

        self.fin_f = PacketField(parent=self.master, name='pkt_field', text='FIN', width=5, height=15, checkbox=True)
        self.syn_f = PacketField(parent=self.master, name='pkt_field', text='SYN', width=5, height=15, checkbox=True)
        self.rst_f = PacketField(parent=self.master, name='pkt_field', text='RST', width=5, height=15, checkbox=True)
        self.psh_f = PacketField(parent=self.master, name='pkt_field', text='PSH', width=5, height=15, checkbox=True)
        self.ack_f = PacketField(parent=self.master, name='pkt_field', text='ACK', width=5, height=15, checkbox=True)
        self.urg_f = PacketField(parent=self.master, name='pkt_field', text='URG', width=5, height=15, checkbox=True)
        self.ece_f = PacketField(parent=self.master, name='pkt_field', text='ECE', width=5, height=15, checkbox=True)
        self.cwr_f = PacketField(parent=self.master, name='pkt_field', text='CWR', width=5, height=15, checkbox=True)
        self.win = PacketField(parent=self.master, name='pkt_field', text='Window Size\n(16 bits)', in_txt='8192', width=160, height=40, in_width=150)
        # row 5
        self.checksum = PacketField(parent=self.master, name='pkt_field', text='Checksum\n(16 bits)', in_txt='', width=160, height=40)
        self.urg = PacketField(parent=self.master, name='pkt_field', text='Urgent Pointer\n(16 bits)', in_txt='0', width=160, height=40)
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
        row2.addWidget(self.seq)
        row2.addStretch()
        # row 3
        row3 = QHBoxLayout()
        row3.addWidget(self.ack)
        row3.addStretch()
        # row 4
        row4 = QHBoxLayout()
        row4.setSpacing(0)
        row4.addWidget(self.offset)
        row4.addWidget(self.reserved)
        row4.addWidget(self.win)
        row4.addStretch()
        # row 5
        flags_row = QHBoxLayout()
        flags_row.addWidget(self.cwr_f)
        flags_row.addWidget(self.ece_f)
        flags_row.addWidget(self.urg_f)
        flags_row.addWidget(self.ack_f)
        flags_row.addWidget(self.psh_f)
        flags_row.addWidget(self.rst_f)
        flags_row.addWidget(self.syn_f)
        flags_row.addWidget(self.fin_f)

        flags_grp = QGroupBox("TCP Flags")
        flags_grp.setObjectName('header')
        flags_grp.setLayout(flags_row)
        flags_grp.setFont(QFont('Verdana', 8))

        row5 = QHBoxLayout()
        row5.addWidget(flags_grp)
        row5.addStretch()
        # row 6
        row6 = QHBoxLayout()
        row6.addWidget(self.checksum)
        row6.addWidget(self.urg)
        row6.addStretch()
        
        main_layout = QVBoxLayout() 
        main_layout.addLayout(row1)
        main_layout.addLayout(row2)
        main_layout.addLayout(row3)
        main_layout.addLayout(row4)
        main_layout.addLayout(row5)
        main_layout.addLayout(row6)
        main_layout.addStretch()
        main_layout.setSpacing(0)
        self.setLayout(main_layout)

    def set_flags(self, flags_value):
        flags_bin = numConvert(flags_value, 'BIN', toString=True)
        if len(flags_bin):
            self.cwr_f.setCheck(False if flags_bin[0] == '0' else True)
        if len(flags_bin) > 1:
            self.ece_f.setCheck(False if flags_bin[1] == '0' else True)
        if len(flags_bin) > 2:
            self.urg_f.setCheck(False if flags_bin[2] == '0' else True)
        if len(flags_bin) > 3:
            self.ack_f.setCheck(False if flags_bin[3] == '0' else True)
        if len(flags_bin) > 4:
            self.psh_f.setCheck(False if flags_bin[4] == '0' else True)
        if len(flags_bin) > 5:
            self.rst_f.setCheck(False if flags_bin[5] == '0' else True)
        if len(flags_bin) > 6:
            self.syn_f.setCheck(False if flags_bin[6] == '0' else True)
        if len(flags_bin) > 7:
            self.fin_f.setCheck(False if flags_bin[7] == '0' else True)

    def get_flags(self, convert='HEX'):
        flags_bin = ''
        flags_bin += self.cwr_f.isChecked() 
        flags_bin += self.ece_f.isChecked() 
        flags_bin += self.urg_f.isChecked() 
        flags_bin += self.ack_f.isChecked() 
        flags_bin += self.psh_f.isChecked() 
        flags_bin += self.rst_f.isChecked() 
        flags_bin += self.syn_f.isChecked() 
        flags_bin += self.fin_f.isChecked() 
        return numConvert(flags_bin, convert)

    def set_header(self, src='20', dst='80', seq='0', ack='0', offset='',reserved='0', flags='0', window='8192', checksum='', urg='0'):
        ''' Set header values '''
        self.src.setText(src)
        self.dst.setText(dst)
        self.seq.setText(seq)
        self.ack.setText(ack)
        self.offset.setText(offset)
        self.reserved.setText(reserved)
        self.win.setText(window)
        self.checksum.setText(checksum)
        self.urg.setText(urg)

        self.set_flags(flags)

    def get_header(self):
        ''' Get header values '''
        return {
            'src': numConvert(self.src.text(), 'DEC'),
            'dst': numConvert(self.dst.text(), 'DEC'),
            'seq': numConvert(self.seq.text(), 'DEC'),
            'ack': numConvert(self.ack.text(), 'DEC'),
            'offset': numConvert(self.offset.text(), 'DEC'),
            'reserved': numConvert(self.reserved.text(), 'DEC'),
            'flags': self.get_flags('DEC'),
            'window': numConvert(self.win.text(), 'DEC'),
            'checksum': numConvert(self.checksum.text(), 'DEC'),
            'urg': numConvert(self.urg.text(), 'DEC')
        }

    def convert(self, to):
        ''' Convert header values '''
        self.set_header( 
            src=numConvert(self.src.text(), to, toString=True), 
            dst=numConvert(self.dst.text(), to, toString=True), 
            seq=numConvert(self.seq.text(), to, toString=True), 
            ack=numConvert(self.ack.text(), to, toString=True), 
            offset=numConvert(self.offset.text(), to, toString=True),
            reserved=numConvert(self.reserved.text(), to, toString=True), 
            window=numConvert(self.win.text(), to, toString=True), 
            checksum=numConvert(self.checksum.text(), to, toString=True), 
            urg=numConvert(self.urg.text(), to, toString=True)
        )

    def gen_src_port(self):
        # get covert type
        conv = self.master.toolbar.convert_modes.get_btn().text()
        self.src.setText(numConvert(str(self.master.manager.generate_port()), conv, toString=True))
    
    def gen_dst_port(self):
        # get covert type
        conv = self.master.toolbar.convert_modes.get_btn().text()
        self.dst.setText(numConvert(str(self.master.manager.generate_port()), conv, toString=True))
