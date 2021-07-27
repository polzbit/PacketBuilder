from PyQt5.QtWidgets import QWidget,QScrollArea,QHeaderView, QGroupBox, QHBoxLayout, QVBoxLayout, QGridLayout, QPushButton, QComboBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from pyqt.models.LabelModel import Label
from pyqt.models.InputModel import Input
from pyqt.models.TableModel import TableWidget
from rules.rule_parser import RuleParser
from utils import numConvert, ipConvert

class RuleDetails(QWidget):
    def __init__(self, master):
        QWidget.__init__(self, master)
        self.master = master
        self.current_rule = None
        self.parser = None
        self.setFont(QFont('Courier New', 10))
        # IP Details
        # ------------------------------ Widgets Setup ------------------------------ #
        # row 1
        src_lbl = Label(parent=self.master, name='rule_lbl', text="SOURCE", width=100, height=40, bold=True, align=Qt.AlignRight|Qt.AlignTop)
        self.src_addr = Label(parent=self.master, text="any", width=120, height=40, align=Qt.AlignLeft)
        self.src_port = Label(parent=self.master, text="any", width=120, height=40, align=Qt.AlignLeft)

        dst_lbl = Label(parent=self.master, name='rule_lbl', text="DESTINATION", width=100, height=40, bold=True, align=Qt.AlignRight|Qt.AlignTop)
        self.dst_addr = Label(parent=self.master, text="any", width=120, height=40, align=Qt.AlignLeft)
        self.dst_port = Label(parent=self.master, text="any", width=120, height=40, align=Qt.AlignLeft)

        proto_lbl = Label(parent=self.master, name='rule_lbl', text="PROTOCOL", width=100, height=40, bold=True, align=Qt.AlignRight|Qt.AlignTop)
        self.proto = Label(parent=self.master, text="any", width=100, height=40, align=Qt.AlignLeft)

        msg_lbl = Label(parent=self.master, name='rule_lbl', text="MESSAGE", width=100, height=40, bold=True, align=Qt.AlignRight|Qt.AlignTop)
        self.msg = Label(parent=self.master, text="", width=400, height=40, align=Qt.AlignLeft|Qt.AlignTop)

        opt_lbl = Label(parent=self.master, name='rule_lbl', text="OPTIONS", width=100, height=40, bold=True, align=Qt.AlignRight|Qt.AlignTop)

        rules_lbl = Label(parent=self.master, name='rule_lbl', text="RULES", width=100, height=40, bold=True, align=Qt.AlignRight|Qt.AlignVCenter)
        self.rules_drop = QComboBox()
        self.rules_drop.setFixedWidth(300)
        self.rules_drop.currentIndexChanged.connect(self.master.on_rule_click)
        # opt table
        opt_table_headers = ['#', 'Key', 'Value', 'args']
        self.opt_table = TableWidget(opt_table_headers)
        # self.opt_table.itemSelectionChanged.connect(self.on_rule_click)
        self.opt_table.setColumnWidth(0, 25)
        self.opt_table.setColumnWidth(1, 100)
        opt_header = self.opt_table.horizontalHeader()       
        opt_header.setSectionResizeMode(2, QHeaderView.Stretch)
        
        load_btn = QPushButton()
        load_btn.clicked.connect(self.set_rule_pkt)
        load_btn.setText('LOAD RULE')
        load_btn.setMinimumSize(80, 30)
        load_btn.setMaximumSize(80, 30)
        detailsFont = QFont()
        detailsFont.setBold(True)
        load_btn.setFont(detailsFont)

        # ------------------------------ Layout Setup ------------------------------ #

        # opt layout
        opt_layout = QVBoxLayout()
        opt_layout.setContentsMargins(0, 0, 0, 0)
        opt_layout.addWidget(self.opt_table)

        opt_area = QScrollArea()
        opt_area.setWidgetResizable(True)
        opt_area.setStyleSheet("background: white;")
        opt_area.setLayout(opt_layout)

        row = QHBoxLayout() 
        row.addWidget(rules_lbl)
        row.addWidget(self.rules_drop)
        row.addWidget(load_btn)
        row.addStretch()

        first_row = QHBoxLayout() 
        first_row.addWidget(msg_lbl)
        first_row.addWidget(self.msg)
        first_row.addStretch()

        second_row = QHBoxLayout()
        second_row.addWidget(src_lbl)
        second_row.addWidget(self.src_addr)
        second_row.addWidget(self.src_port)
        second_row.addStretch()

        third_row = QHBoxLayout()
        third_row.addWidget(dst_lbl)
        third_row.addWidget(self.dst_addr)
        third_row.addWidget(self.dst_port)
        third_row.addStretch()

        fourth_row = QHBoxLayout()
        fourth_row.addWidget(proto_lbl)
        fourth_row.addWidget(self.proto)
        fourth_row.addStretch()

        fifth_row = QHBoxLayout() 
        fifth_row.addWidget(opt_lbl)
        fifth_row.addStretch()

        six_row = QHBoxLayout()
        six_row.addWidget(opt_area)

        details_layout = QVBoxLayout(self) 
        details_layout.addLayout(row)
        details_layout.addLayout(first_row)
        details_layout.addLayout(second_row)
        details_layout.addLayout(third_row)
        details_layout.addLayout(fourth_row)
        details_layout.addLayout(fifth_row)
        details_layout.addLayout(six_row)

    def set_rule_pkt(self):
        # get covert type
        conv = self.master.toolbar.convert_modes.get_btn().text()
        # parse rule data
        self.parser = RuleParser(self.master, self.current_rule)
        # show and set ip header
        self.master.toolbar.type_drop.setCurrentIndex(1)
        self.master.ip_header.set_header(
            ttl=numConvert(str(self.parser.ttl), to=conv, toString=True), 
            flags=numConvert(str(self.parser.frag_flags), to=conv, toString=True), 
            proto=numConvert(str(self.parser.proto), to=conv, toString=True), 
            src=ipConvert(str(self.parser.src_addr), to=conv), 
            dst=ipConvert(str(self.parser.dst_addr), to=conv)
        )  
        # load data in headers
        if self.current_rule.data['protocol'] == "tcp":
            # show tcp header
            self.master.toolbar.type_drop.setCurrentIndex(3)
            self.master.tcp_header.set_header(
                src=numConvert(str(self.parser.src_port), to=conv, toString=True), 
                dst=numConvert(str(self.parser.dst_port), to=conv, toString=True), 
                flags=numConvert(str(self.parser.flags), to=conv, toString=True), 
                seq=numConvert(str(self.parser.seq), to=conv, toString=True), 
                ack=numConvert(str(self.parser.ack), to=conv, toString=True), 
                window=numConvert(str(self.parser.win), to=conv, toString=True)
            )
        elif self.current_rule.data['protocol'] == "udp":
            # show udp header
            self.master.toolbar.type_drop.setCurrentIndex(4)
            self.master.udp_header.set_header(
                src=numConvert(str(self.parser.src_port), to=conv, toString=True), 
                dst=numConvert(str(self.parser.dst_port), to=conv, toString=True)
            )
        elif self.current_rule.data['protocol'] == "icmp":
            # show icmp header
            self.master.toolbar.type_drop.setCurrentIndex(2)
            self.master.icmp_header.set_header(
                icmp_type=numConvert(str(self.parser.itype), to=conv, toString=True), 
                code=numConvert(str(self.parser.icode), to=conv, toString=True),
                icmp_id=numConvert(str(self.parser.icmp_id), to=conv, toString=True),
                icmp_seq=numConvert(str(self.parser.icmp_seq), to=conv, toString=True)
            )
        
        # check for payload
        if self.parser.content != bytearray():
            hex_str = str(self.parser.content.hex())
            split_string = [hex_str[i:i+2] for i in range(0, len(hex_str), 2)]
            hex_str = ' '.join(split_string)
            self.master.payload_header.set_header(load=hex_str)
            self.master.toolbar.payload_mode.setChecked(True)
        else:
            self.master.toolbar.payload_mode.setChecked(False)
        self.master.on_payload_mode()

    def load_details(self, rule_index):
        # clear last data
        self.opt_table._clear()
        # get rule
        self.current_rule = self.master.manager.rules[rule_index]
        # set rule data on gui
        self.src_addr.setText(self.current_rule.data['source ip'])
        self.src_port.setText(self.current_rule.data['source port'])
        self.dst_addr.setText(self.current_rule.data['destination ip'])
        self.dst_port.setText(self.current_rule.data['destination port'])
        self.proto.setText(self.current_rule.data['protocol'])
        self.msg.setText(self.current_rule.data['msg'])
        # insert data to contant table
        for index, opt in enumerate(self.current_rule.data['options']):
            args_str = ','.join(opt['args'])
            self.opt_table._addRow([index, opt['name'], opt['value'], args_str])

        