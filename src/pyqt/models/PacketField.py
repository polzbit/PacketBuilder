from PyQt5.QtWidgets import QWidget, QGroupBox, QHBoxLayout, QVBoxLayout, QGridLayout, QPushButton, QCheckBox
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont,QIcon
from pyqt.models.LabelModel import Label
from pyqt.models.InputModel import Input
import os

class PacketField(QWidget):
    ''' IP Header Component '''
    def __init__(self, parent=None, name='', text='', in_txt='', width=10, height=10, in_width=0, in_height=0, checkbox=False, align=Qt.AlignCenter):
        QWidget.__init__(self, parent)
        self.parent = parent
        
        if in_width == 0:
            in_width = width
        if in_height == 0:
            in_height = height
        if name != '':
            self.setObjectName(name)
        lbl = Label(parent=parent, text=text, width=width, height=height, bold=True, align=Qt.AlignLeft|Qt.AlignVCenter)
        self.input = Input(parent=parent,name='pkt_input', text=in_txt, width=in_width, height=in_height, bold=True, align=align)
        lbl.setFont(QFont('Arial', 8))
        self.input.setFont(QFont('Arial', 8))
        # todo add checkbox for flags
        self.checkbox = QCheckBox(parent)

        if checkbox:
            self.input.hide()
            self.checkbox.show()
            self.checkbox.setFixedHeight(15)
            lbl.setFixedWidth(25)
        else:
            self.input.show()
            self.checkbox.hide()

        layout = QVBoxLayout(self) 
        layout.addWidget(lbl)
        layout.addWidget(self.checkbox)
        layout.addWidget(self.input)
        layout.addStretch()
        layout.setSpacing(0)

    def text(self):
        return self.input.text()

    def setText(self, txt):
        self.input.setText(txt)

    def setCheck(self, check=False):
        if check == '1':
            check = True
        
        self.checkbox.setChecked(check)

    def getText(self):
        return self.input.text()

    def isChecked(self):
        if self.checkbox.isChecked():
            return '1'
        return '0'