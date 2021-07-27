from PyQt5.QtWidgets import QWidget, QGroupBox, QHBoxLayout, QVBoxLayout, QToolButton, QPushButton, QButtonGroup
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from pyqt.models.LabelModel import Label
from pyqt.models.InputModel import Input

class RadioGroup(QWidget):
    def __init__(self, master, modes, action):
        QWidget.__init__(self, master)
        self.master = master
        self.radios = []
        # IP Details
        # ------------------------------ Widgets Setup ------------------------------ #
        for mode in modes:
            self.radios.append(QToolButton(text=mode, checkable=True, checked=False))
        self.radios[0].setChecked(True)
        # ------------------------------ Layout Setup ------------------------------ #
        self.grp = QButtonGroup(self)
        main_layout = QHBoxLayout() 
        for radio in self.radios:
            self.grp.addButton(radio)
            main_layout.addWidget(radio)
        self.grp.buttonClicked.connect(action)
        # layout.setContentsMargins(60, 6, 60, 6)
        self.setLayout(main_layout)
    
    def get_btn(self):
        return self.grp.checkedButton()
    
    def setChecked(self, index):
        for i, radio in enumerate(self.radios):
            if i == index:
                radio.setChecked(True)
            else:
                radio.setChecked(False)
