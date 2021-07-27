from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from pyqt.styles.StyleSheet import StyleSheet
import os

class Signals(QObject):
    onShow = pyqtSignal()
    onHide = pyqtSignal()
    onFin = pyqtSignal()

class PreloaderWindow(QDialog):
    def __init__(self, parent):
        # ---------------------------- Setup -------------------------------
        super().__init__(parent)
        self.parent = parent
        self.signals = Signals()
        self.signals.onShow.connect(self.on_show)
        self.signals.onHide.connect(self.on_hide)
        self.signals.onFin.connect(self.on_finish)
        self.resize(300, 200)
        self.setWindowTitle("Loading...")
        self.setStyleSheet(StyleSheet()) 

        self.rules_pic = QLabel(self)
        x_pix = QPixmap("./src/pyqt/img/right-arrow.png")
        v_pix = QPixmap("./src/pyqt/img/check.png")
        self.x_icon = x_pix.scaled(10, 10, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.v_icon = v_pix.scaled(10, 10, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.rules_pic.setPixmap(self.x_icon)
        self.rules_pic.setMinimumSize(15, 15)
        self.rules_pic.setMaximumSize(15, 15)

        self.rule_lbl = QLabel(self)
        self.rule_lbl.setText('Loading Rules')
        self.rule_lbl.setAlignment(Qt.AlignLeft)
        self.rule_lbl.setFont(self.parent.detailsFont)
        self.rule_lbl.setMinimumSize(150, 20)
        self.rule_lbl.setMaximumSize(150, 20)

        layout = QVBoxLayout(self)
        row = QHBoxLayout()
        row.addWidget(self.rules_pic)
        row.addWidget(self.rule_lbl)
        row.addStretch()
        row.setContentsMargins(50, 0, 0, 50)
        layout.addLayout(row)
        self.setup()
    
    def setup(self):
        self.parent.manager.load_rules()

    @pyqtSlot()
    def on_show(self):
        self.show()

    @pyqtSlot()
    def on_hide(self):
        self.hide()

    @pyqtSlot()
    def on_finish(self):
        self.rules_pic.setPixmap(self.v_icon)
        self.hide()
        self.parent.signals.onShow.emit()
        
    
    def closeEvent(self, event):
        self.parent.quitEvent()