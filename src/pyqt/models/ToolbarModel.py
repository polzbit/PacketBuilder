from PyQt5.QtWidgets import QWidget, QGroupBox, QHBoxLayout, QVBoxLayout, QGridLayout, QPushButton, QCheckBox, QComboBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from pyqt.models.LabelModel import Label
from pyqt.models.InputModel import Input
from pyqt.models.RadioGroup import RadioGroup

class ToolBar(QWidget):
    ''' ToolBar '''
    def __init__(self, master):
        QWidget.__init__(self, master)
        self.master = master
        detailsFont = QFont('Verdana', 10)
        detailsFont.setBold(True)
        self.setFont(detailsFont)
        # ------------------------------ Widgets Setup ------------------------------ #
        self.type_lbl = Label(parent=self.master,text="Packet Type:", width=80, height=30, bold=True, align=Qt.AlignLeft|Qt.AlignVCenter)
        self.type_drop = QComboBox()
        self.type_drop.addItem('Frame')
        self.type_drop.addItem('IPv4')
        self.type_drop.addItem('ICMP')
        self.type_drop.addItem('IPv4 TCP')
        self.type_drop.addItem('IPv4 UDP')
        self.type_drop.currentIndexChanged.connect(self.master.typeChange)
        self.type_drop.setCurrentIndex(1)

        self.convert_modes = RadioGroup(self, ["DEC", "HEX", "BIN"], self.master.on_convert_mode)

        self.payload_mode = QCheckBox('Payload')
        self.payload_mode.stateChanged.connect(self.master.on_payload_mode)

        count_lbl = Label(parent=self.master, text="Packet Count", width=50, height=30, bold=True, align=Qt.AlignLeft|Qt.AlignVCenter)
        self.count_in = Input(parent=self.master, text="1", width=50, height=30, bold=True, align=Qt.AlignCenter)

        self.send_btn = QPushButton()
        self.send_btn.clicked.connect(self.master.on_send)
        self.send_btn.setText('SEND')
        self.send_btn.setMinimumSize(80, 30)
        self.send_btn.setMaximumSize(80, 30)
        # ------------------------------ Layout Setup ------------------------------ #

        convert_modes = QVBoxLayout()
        convert_modes.addWidget(self.convert_modes)
        
        payload_modes = QVBoxLayout()
        payload_modes.addWidget(self.payload_mode)

        topRow = QHBoxLayout(self)
        topRow.addWidget(self.type_lbl)
        topRow.addWidget(self.type_drop)
        topRow.addLayout(convert_modes)
        topRow.addLayout(payload_modes)
        topRow.addStretch()
        topRow.addWidget(count_lbl)
        topRow.addWidget(self.count_in)
        topRow.addWidget(self.send_btn)

    