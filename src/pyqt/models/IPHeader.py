from PyQt5.QtWidgets import QWidget, QGroupBox, QHBoxLayout, QVBoxLayout, QGridLayout, QPushButton, QCheckBox
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont,QIcon
from pyqt.models.LabelModel import Label
from pyqt.models.InputModel import Input
from pyqt.models.ButtonModel import Button
from utils import ipConvert, numConvert
from pyqt.models.PacketField import PacketField
import os

class IPHeader(QWidget):
    ''' IP Header Component '''
    def __init__(self, master):
        QWidget.__init__(self, master)
        self.master = master
        # IP Details
        # ------------------------------ Widgets Setup ------------------------------ #
        # row 1
        self.ver = PacketField(parent=self.master, name='pkt_field', text='Version\n(4 bits)', in_txt='4', width=40, height=40)
        self.ihl = PacketField(parent=self.master, name='pkt_field', text='IHL\n(4 bits)', in_txt='5', width=40, height=40)
        self.tos = PacketField(parent=self.master, name='pkt_field', text='ToS\n(8 bits)', in_txt='0', width=80, height=40)
        self.length = PacketField(parent=self.master, name='pkt_field', text='Length\n(16 bits)', in_txt='', width=160, height=40)
        # row 2
        self.id = PacketField(parent=self.master, name='pkt_field', text='ID\n(16 bits)', in_txt='1', width=160, height=40)
        
        self.r_flag = PacketField(parent=self.master, name='pkt_field', text='R', width=5, height=15, checkbox=True)
        self.DF_flag = PacketField(parent=self.master, name='pkt_field', text='DF', width=5, height=15, checkbox=True)
        self.MF_flag = PacketField(parent=self.master, name='pkt_field', text='MF', width=5, height=15, checkbox=True)
        # flags_lbl = Label(text="Flags\n(3 bits)", width=30, height=40, bold=True, align=Qt.AlignLeft|Qt.AlignVCenter)
        self.frag = PacketField(parent=self.master, name='pkt_field', text='Offset\n(13 bits)', in_txt='0', width=130, height=40)

        # row 3
        self.ttl = PacketField(parent=self.master, name='pkt_field', text='TTL\n(8 bits)', in_txt='64', width=80, height=40)
        self.proto = PacketField(parent=self.master, name='pkt_field', text='Protocol\n(8 bits)', in_txt='64', width=80, height=40)
        self.checksum = PacketField(parent=self.master, name='pkt_field', text='Checksum\n(16 bits)', in_txt='', width=160, height=40)
        
        # row 4
        self.src = PacketField(parent=self.master, name='pkt_field', text='Source Address\n(32 bits)', in_txt='', width=320, height=40)
        # row 5
        self.dst = PacketField(parent=self.master, name='pkt_field', text='Destination Address\n(32 bits)', in_txt='', width=320, height=40)

        generate_private_src = Button(parent=self, name='pkt_btn', icon="./src/pyqt/img/private.png", width=30, height=30, iwidth=25, ihight=25, bold=False, tooltip='Generate private ip address')
        generate_private_src.clicked.connect(self.gen_private_src)

        generate_public_src = Button(parent=self, name='pkt_btn', icon="./src/pyqt/img/public.png", width=30, height=30, iwidth=25, ihight=25, bold=False, tooltip='Generate public ip address')
        generate_public_src.clicked.connect(self.gen_public_src)

        generate_private_dst = Button(parent=self, name='pkt_btn', icon="./src/pyqt/img/private.png", width=30, height=30, iwidth=25, ihight=25, bold=False, tooltip='Generate private ip address')
        generate_private_dst.clicked.connect(self.gen_private_dst)

        generate_public_dst = Button(parent=self, name='pkt_btn', icon="./src/pyqt/img/public.png", width=30, height=30, iwidth=25, ihight=25, bold=False, tooltip='Generate public ip address')
        generate_public_dst.clicked.connect(self.gen_public_dst)
        # ------------------------------ Layout Setup ------------------------------ #
        
        # row 1
        row1 = QHBoxLayout()
        row1.addWidget(self.ver)
        row1.addWidget(self.ihl)
        row1.addWidget(self.tos)
        row1.addWidget(self.length)
        row1.addStretch()
        row1.setSpacing(0)
        # row 2
        row2 = QHBoxLayout()
        row2.addWidget(self.id)
        row2.addWidget(self.frag)
        row2.addStretch()
        row2.setSpacing(0)
        # row 3
        flags_row = QHBoxLayout()
        flags_row.addWidget(self.r_flag)
        flags_row.addWidget(self.DF_flag)
        flags_row.addWidget(self.MF_flag)
        flags_row.setSpacing(0)

        flags_grp = QGroupBox("Fragment Flags")
        flags_grp.setObjectName('header')
        flags_grp.setLayout(flags_row)
        flags_grp.setFont(QFont('Verdana', 8))

        row3 = QHBoxLayout()
        row3.addWidget(flags_grp)
        row3.addStretch()
        # row 4
        row4 = QHBoxLayout()
        row4.addWidget(self.ttl)
        row4.addWidget(self.proto)
        row4.addWidget(self.checksum)
        row4.addStretch()
        row4.setSpacing(0)
        # row 5
        src_btns_lay = QVBoxLayout()
        src_btns_lay.addStretch()
        src_btns_lay.addWidget(generate_public_src)
        src_btns_lay.addWidget(generate_private_src)
        src_btns_lay.setSpacing(5)

        row5 = QHBoxLayout()
        row5.addWidget(self.src)
        row5.addLayout(src_btns_lay)
        row5.addStretch()
        
        # row 6
        dst_btns_lay = QVBoxLayout()
        dst_btns_lay.addStretch()
        dst_btns_lay.addWidget(generate_public_dst)
        dst_btns_lay.addWidget(generate_private_dst)
        dst_btns_lay.setSpacing(5)

        row6 = QHBoxLayout()
        row6.addWidget(self.dst)
        row6.addLayout(dst_btns_lay)
        row6.addStretch()
        row6.setSpacing(0)

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

    def set_header(self, ver='4', ihl='5', tos='0', total_len='', pid='1', ttl='64', flags='0', frag='0', proto='0', checksum='', src='', dst=''):
        ''' Set header values '''
        self.ver.setText(ver)
        self.ihl.setText(ihl)
        self.tos.setText(tos)
        self.length.setText(total_len)
        self.ttl.setText(ttl)
        self.id.setText(pid)
        self.frag.setText(frag)
        self.proto.setText(proto)
        self.checksum.setText(checksum)
        self.src.setText(src)
        self.dst.setText(dst)

        self.set_flags(flags)
    
    def set_flags(self, flags_value):
        flags_bin = numConvert(flags_value, 'BIN', toString=True)
        if len(flags_bin):
            self.r_flag.setCheck(False if flags_bin[0] == '0' else True)
        if len(flags_bin) > 1:
            self.MF_flag.setCheck(False if flags_bin[1] == '0' else True)
        if len(flags_bin) > 2:
            self.DF_flag.setCheck(False if flags_bin[2] == '0' else True)

    def get_flags(self, convert='HEX'):
        flags_bin = ''
        flags_bin += self.r_flag.isChecked()
        flags_bin += self.MF_flag.isChecked()
        flags_bin += self.DF_flag.isChecked()
       
        return numConvert(flags_bin, convert)

    def get_header(self):
        ''' Get header values '''
        return {
            'version': numConvert(self.ver.text(), 'DEC'),
            'ihl': numConvert(self.ihl.text(), 'DEC'),
            'tos': numConvert(self.tos.text(), 'DEC'),
            'length': numConvert(self.length.text(), 'DEC'),
            'id': numConvert(self.id.text(), 'DEC'),
            'flags': self.get_flags('DEC'),
            'frag': numConvert(self.frag.text(), 'DEC'),
            'ttl': numConvert(self.ttl.text(), 'DEC'),
            'proto': numConvert(self.proto.text(), 'DEC'),
            'checksum': numConvert(self.checksum.text(), 'DEC'),
            'src': ipConvert(self.src.text(), 'DEC'),
            'dst': ipConvert(self.dst.text(), 'DEC')
        }

    def convert(self, to):
        ''' Convert header values '''
        self.set_header(
            ver = numConvert(self.ver.text(), to, toString=True),
            ihl = numConvert(self.ihl.text(), to, toString=True),
            tos = numConvert(self.tos.text(), to, toString=True), 
            total_len = numConvert(self.length.text(), to, toString=True),
            pid = numConvert(self.id.text(), to, toString=True),
            frag = numConvert(self.frag.text(), to, toString=True),
            ttl = numConvert(self.ttl.text(), to, toString=True),
            proto = numConvert(self.proto.text(), to, toString=True),
            checksum = numConvert(self.checksum.text(), to, toString=True),
            src = ipConvert(self.src.text(), to), 
            dst = ipConvert(self.dst.text(), to)
        )

    def gen_private_src(self):
        # get covert type
        conv = self.master.toolbar.convert_modes.get_btn().text()
        self.src.setText(ipConvert(self.master.manager.generate_private_addr(), conv))

    def gen_public_src(self):
        conv = self.master.toolbar.convert_modes.get_btn().text()
        self.src.setText(ipConvert(self.master.manager.generate_public_addr(), conv))

    def gen_public_dst(self):
        conv = self.master.toolbar.convert_modes.get_btn().text()
        self.dst.setText(ipConvert(self.master.manager.generate_public_addr(), conv))

    def gen_private_dst(self):
        conv = self.master.toolbar.convert_modes.get_btn().text()
        self.dst.setText(ipConvert(self.master.manager.generate_private_addr(), conv))