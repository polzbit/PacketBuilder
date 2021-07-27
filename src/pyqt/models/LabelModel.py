from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class Label(QLabel):
    def __init__(self, parent=None, name='', text='', width=50, height=50, bold=False, align=Qt.AlignCenter):
        super().__init__(parent)
        self.setText(text)
        self.setAlignment(align)
        self.setMinimumSize(width, height)
        self.setMaximumSize(width, height)
        self.setWordWrap(True)
        self.setContentsMargins(0, 0, 0, 0)
        if name != '':
            self.setObjectName(name)
        if bold:
            detailsFont = QFont('Verdana', 10)
            detailsFont.setBold(True)
            self.setFont(detailsFont)
