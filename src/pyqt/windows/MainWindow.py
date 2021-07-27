from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from pyqt.styles.StyleSheet import StyleSheet
from pyqt.windows.PreloaderWindow import PreloaderWindow
from pyqt.windows.SettingsWindow import SettingsWindow
from builder.packet_manager import PacketManager
from pyqt.models.TableModel import TableWidget
from pyqt.models.IPHeader import IPHeader
from pyqt.models.LabelModel import Label
from pyqt.models.InputModel import Input
from pyqt.models.RuleDetails import RuleDetails
from pyqt.models.TCPHeader import TCPHeader
from pyqt.models.UDPHeader import UDPHeader
from pyqt.models.EtherHeader import EtherHeader
from pyqt.models.PayloadHeader import PayloadHeader
from pyqt.models.ICMPHeader import ICMPHeader
from pyqt.models.RadioGroup import RadioGroup
from pyqt.models.CollapseArea import CollapseArea
from pyqt.models.ToolbarModel import ToolBar
import os

class Signals(QObject):
    onShow = pyqtSignal()
    onHide = pyqtSignal()
    addRule = pyqtSignal(list)
    onSend = pyqtSignal()
    onFinSend = pyqtSignal(int)

class MainWindow(QMainWindow):
    # Override the class constructor
    def __init__(self):
        # -------------------------------------------- App Setup ------------------------------------------- #
        QMainWindow.__init__(self)
        # hide - show preloader
        self.hide()
        self.signals = Signals()
        self.signals.onShow.connect(self.on_show)
        self.signals.onHide.connect(self.on_hide)
        self.signals.addRule.connect(self.on_add_rule)
        self.signals.onSend.connect(self.on_send)
        self.signals.onFinSend.connect(self.on_fin_send)
        # Fonts 
        self.detailsFont = QFont('Verdana', 10)
        self.detailsFont.setBold(True)
        self.manager = PacketManager(self)
        # windows
        self.settings_window = SettingsWindow(self)
        self.preloader_window = PreloaderWindow(self)
        self.preloader_window.signals.onShow.emit()

        # UI setup
        self.icon = QIcon("./src/pyqt/img/logo.png")
        self.setWindowIcon(self.icon)
        self.init_systemTray()
        self.collapse = None
        self.initUI()

        # center window 
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

    def initUI(self):
        # ------------------------------ UI Setup ------------------------------ #
        self.setMinimumSize(1080, 600)             
        self.setWindowTitle("Packet Builder") 
        # ------------------------------ Top Toolbar ------------------------------ #
        mainMenu = self.menuBar()
        # top menus
        fileMenu = mainMenu.addMenu('File')
        helpMenu = mainMenu.addMenu('Help')
        # file sun-menu
        setAct = fileMenu.addAction('Settings')
        exitAct = fileMenu.addAction('Exit')
        # connect actions
        setAct.triggered.connect(self.launchSettingsDialog)
        exitAct.triggered.connect(self.quitEvent)
        # ------------------------------ Widgets Setup ------------------------------ #
        self.central_widget = QWidget(self)           
        self.setCentralWidget(self.central_widget) 
        self.central_widget.setStyleSheet(StyleSheet())
                
        # Rule Details
        self.details = RuleDetails(self)
        
        # tools
        self.toolbar = ToolBar(self)
        
        # bottom
        # Ether Header
        self.ether_header = EtherHeader(self)
        # IP Header
        self.ip_header = IPHeader(self)
        # TCP Header
        self.tcp_header = TCPHeader(self)
        # UDP Header
        self.udp_header = UDPHeader(self)
        # UDP Header
        self.icmp_header = ICMPHeader(self)
        # Payload Header
        self.payload_header = PayloadHeader(self)

        # collapse tree
        self.collapse = CollapseArea('', self)
        # seperator
        seperator = QFrame(self)
        seperator.setFrameShape(QFrame.HLine)
        seperator.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        pal = seperator.palette()
        pal.setColor(QPalette.WindowText, QColor(185,185,185))
        seperator.setPalette(pal)
        # ------------------------------ Layout Setup ------------------------------ #
        main_layout = QVBoxLayout()  
        main_layout.setContentsMargins(0, 0, 0, 0) 
        self.central_widget.setLayout(main_layout) 

        # rules layout
        details_lay = QVBoxLayout()
        details_lay.addWidget(self.details)

        view_grp = QGroupBox("Rule View")
        view_grp.setObjectName('header')
        view_grp.setLayout(details_lay)
        view_grp.setFont(self.detailsFont)
        ruls_lay = QVBoxLayout()
        ruls_lay.addWidget(view_grp)

        top = QHBoxLayout()
        top.addWidget(self.toolbar)

        # packet layout
        pkt_area = QScrollArea(self)
        pkt_area.setWidgetResizable(True)
        pkt_area.setStyleSheet("background: #E5E5E5;")
        pkt_area.setWidget(self.collapse)
        pkt_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        pkt_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        view_lay = QHBoxLayout()
        view_lay.addLayout(ruls_lay)
        view_lay.addWidget(pkt_area)
        view_lay.setContentsMargins(5, 5, 5, 5)

        main_layout.addLayout(top)
        main_layout.addWidget(seperator)
        main_layout.addLayout(view_lay)
        main_layout.setContentsMargins(0, 0, 0, 0)
        # Bottom Status Bar
        self.statusBar().showMessage('Ready', 3000)
    
    def launchSettingsDialog(self):
        if self.settings_window.isVisible():
            self.settings_window.hide()
        else:
            self.settings_window.show()

    def get_modes(self):
        return {
            'type_mode': self.toolbar.type_drop.currentText(),
            'payload_mode': self.toolbar.payload_mode.isChecked()
        }

    def on_convert_mode(self, btn):
        self.ether_header.convert(btn.text())
        self.ip_header.convert(btn.text())
        self.tcp_header.convert(btn.text())
        self.udp_header.convert(btn.text())
        self.icmp_header.convert(btn.text())
   
    def on_payload_mode(self):
        if self.toolbar.payload_mode.isChecked():
            self.collapse.setHidden(5, False)
        else:
            self.collapse.setHidden(5, True)

    def typeChange(self, index):
        if self.collapse != None:
            item = self.toolbar.type_drop.itemText(index)
            self.collapse.hideAll()
            if item == 'Frame':
                self.collapse.setHidden(0, False)
            elif item == 'IPv4':
                self.collapse.setHidden(1, False)
            elif item == 'ICMP':
                self.collapse.setHidden(1, False)
                self.collapse.setHidden(2, False)
            elif item == 'IPv4 TCP':
                self.collapse.setHidden(1, False)
                self.collapse.setHidden(3, False)
            elif item == 'IPv4 UDP':
                self.collapse.setHidden(1, False)
                self.collapse.setHidden(4, False)

    def on_rule_click(self):
        index = self.details.rules_drop.currentIndex()
        self.details.load_details(index)

    @pyqtSlot()
    def on_send(self):
        count = int(self.toolbar.count_in.text())
        self.toolbar.send_btn.setText('Sending...')
        self.toolbar.send_btn.setEnabled(False)
        self.manager.on_send(count=count)

    @pyqtSlot(int)
    def on_fin_send(self, count):
        self.toolbar.send_btn.setText('SEND')
        self.toolbar.send_btn.setEnabled(True)
        self.statusBar().showMessage(f'{count} packets sent.', 3000)

    @pyqtSlot(list)
    def on_add_rule(self, data):
        self.details.rules_drop.addItem(f'{data[0]}#\t[{data[2]}] {data[1]}'.expandtabs(4))

    @pyqtSlot()
    def on_show(self):
        self.show()

    @pyqtSlot()
    def on_hide(self):
        self.hide()
 
    # -------------------------------------------- System Tray ------------------------------------------- #
    def init_systemTray(self):
        # ------ Init System Tray ---- #
        # Init QSystemTrayIcon
        self.tray_icon = QSystemTrayIcon(self)
        # self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        self.tray_icon.setIcon(self.icon)
        # ------ System Tray Menu ------ #
        show_action = QAction("Open...", self)
        settings_action = QAction("Settings", self)
        quit_action = QAction("Exit", self)
        show_action.triggered.connect(self.show) # or self.hide
        settings_action.triggered.connect(self.launchSettingsDialog)
        quit_action.triggered.connect(self.quitEvent)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(settings_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        # on tray event call systemIcon()
        self.tray_icon.activated.connect(self.systemIcon)
        self.tray_icon.show()

    # on system tray double click show app
    def systemIcon(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()

    # -------------------------------------------- Exit Event ------------------------------------------- #
    # Override closeEvent, to intercept the window closing event
    # The window will be closed only if there is no check mark in the check box
    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "Tray Program",
            "Application was minimized to Tray",
            QSystemTrayIcon.Information,
            2000
        )

    def quitEvent(self):
        self.manager.thread_manager._clear()
        qApp.quit()

    def resizeEvent(self, event):
        QMainWindow.resizeEvent(self, event)