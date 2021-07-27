from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon

class Button(QPushButton):
    def __init__(self, parent=None, name='', icon='', text='', width=50, height=50, iwidth=40, ihight=40, bold=False, tooltip=''):
        super().__init__(parent)
        self.setText(text)
        self.setMinimumSize(width, height)
        self.setMaximumSize(width, height)
        self.setContentsMargins(0, 0, 0, 0)
        if icon != '':
            self.setIcon(QIcon(icon))
            self.setIconSize(QSize(iwidth, ihight))
        self.setToolTip(tooltip)
        if name != '':
            self.setObjectName(name)
        if bold:
            detailsFont = QFont('Verdana', 10)
            detailsFont.setBold(True)
            self.setFont(detailsFont)