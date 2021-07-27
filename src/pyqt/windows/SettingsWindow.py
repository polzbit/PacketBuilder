from PyQt5.QtWidgets import QDialog, QBoxLayout, QVBoxLayout, QLabel, QHBoxLayout, QComboBox, QGroupBox, QGridLayout, QScrollArea, QPushButton, QHeaderView, QDialogButtonBox, QFileDialog
from PyQt5.QtCore import *
from PyQt5.QtGui import QImage, QPixmap, QMovie, QIcon, QFont
import os
from pyqt.styles.StyleSheet import StyleSheet
from pyqt.models.LabelModel import Label

class SettingsWindow(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.resize(300, 150)
        self.setWindowTitle("Settings")
        self.setStyleSheet(StyleSheet()) 
        # pipline setup
        rules_file_lbl = Label(parent=self.parent, name="settings_lbl",text="Rules File:", width=60, height=40, bold=True, align=Qt.AlignLeft|Qt.AlignVCenter)
        self.rules_file_in = Label(parent=self.parent, name="settings_in",text=self.parent.manager.const.RULES_PATH, width=300, height=40, bold=True, align=Qt.AlignLeft|Qt.AlignVCenter)
        self.rules_file_in.setContentsMargins(10, 0, 10, 0)

        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.getRulesFile)
        browse_btn.setMinimumSize(60, 40)
        browse_btn.setMaximumSize(60, 40)
        browse_btn.setContentsMargins(0, 0, 0, 0)

        buttonBox = QDialogButtonBox(self)
        buttonBox.setOrientation(Qt.Horizontal)
        buttonBox.setStandardButtons(QDialogButtonBox.Save|QDialogButtonBox.Cancel)
        buttonBox.layout().setDirection(QBoxLayout.RightToLeft)
        buttonBox.setMinimumSize(100, 40)
        buttonBox.setMaximumSize(100, 40)
        buttonBox.accepted.connect(self._save)
        buttonBox.rejected.connect(self._close)

        lay = QVBoxLayout(self)
        layout = QHBoxLayout()
        layout.addStretch()
        layout.addWidget(rules_file_lbl)
        layout.addWidget(self.rules_file_in)
        layout.addWidget(browse_btn)
        layout.addStretch()

        layout2 = QHBoxLayout()
        layout2.addStretch()
        layout2.addWidget(buttonBox)

        lay.addLayout(layout)
        lay.addLayout(layout2)

    def _save(self):
        self.parent.manager.const.set_rules_path(self.rules_file_in.text())
        self.hide()

    def _close(self):
        self.rules_file_in.setText(self.parent.manager.const.RULES_PATH)
        self.hide()

    def closeEvent(self, event):
        self._close()

    def getRulesFile(self):
        cur_dir = QFileDialog.getOpenFileName(self, 'Select Rules File')
        if cur_dir[0] != "":
            self.rules_file_in.setText(cur_dir[0])
