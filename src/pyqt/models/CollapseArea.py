from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout,QWidget, QToolButton, QScrollArea, QSizePolicy, QFrame
from PyQt5.QtCore import Qt, QParallelAnimationGroup, QPropertyAnimation, QAbstractAnimation, pyqtSlot
# from PyQt5.QtGui import *
from pyqt.models.CollapseBox import CollapseBox
from pyqt.styles.StyleSheet import StyleSheet


class CollapseArea(QWidget):
    def __init__(self, title="", parent=None):
        super(CollapseArea, self).__init__(parent)
        self.parent = parent
        # ---------------- Widgets -------------------------
        l2_lay = QHBoxLayout()
        l2_lay.addWidget(self.parent.ether_header)
        l2_lay.addStretch()
        l2_box = CollapseBox('L2: Ethernet Frame', self)
        l2_box.setContentLayout(l2_lay)

        l3_lay = QHBoxLayout()
        l3_lay.addWidget(self.parent.ip_header)
        l3_lay.addStretch()
        l3_box = CollapseBox('L3: IP Packet', self)
        l3_box.setContentLayout(l3_lay)

        l3_icmp_lay = QHBoxLayout()
        l3_icmp_lay.addWidget(self.parent.icmp_header)
        l3_icmp_lay.addStretch()
        l3_icmp_box = CollapseBox('L3: ICMP Protocol', self)
        l3_icmp_box.setContentLayout(l3_icmp_lay)

        l4_tcp_lay = QHBoxLayout()
        l4_tcp_lay.addWidget(self.parent.tcp_header)
        l4_tcp_lay.addStretch()
        l4_tcp_box = CollapseBox('L4: TCP Protocol', self)
        l4_tcp_box.setContentLayout(l4_tcp_lay)

        l4_udp_lay = QHBoxLayout()
        l4_udp_lay.addWidget(self.parent.udp_header)
        l4_udp_lay.addStretch()
        l4_udp_box = CollapseBox('L4: UDP Protocol', self)
        l4_udp_box.setContentLayout(l4_udp_lay)

        payload_lay = QHBoxLayout()
        payload_lay.addWidget(self.parent.payload_header)
        payload_lay.addStretch()
        payload_box = CollapseBox('Payload', self)
        payload_box.setContentLayout(payload_lay)
        # ---------------- Layout --------------------------
        self.lay = QVBoxLayout(self)
        self.lay.addWidget(l2_box)
        self.lay.addWidget(l3_box)
        self.lay.addWidget(l3_icmp_box)
        self.lay.addWidget(l4_tcp_box)
        self.lay.addWidget(l4_udp_box)
        self.lay.addWidget(payload_box)
        self.lay.addStretch()
        self.lay.setContentsMargins(0, 0, 0, 0)
        self.lay.setSpacing(0)
        #self.setHidden(0)
        self.setHidden(2)
        self.setHidden(3)
        self.setHidden(4)
        self.setHidden(5)

    def hideAll(self):
        for i in range(1,self.lay.count() - 1):
            self.setHidden(i)

    def setHidden(self, index, isHiddden=True):
        item = self.lay.itemAt(index).widget() 
        if isHiddden:
            item.hide()
        else:
            item.show()