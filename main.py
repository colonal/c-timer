
from PyQt5 import QtCore
from PyQt5.QtCore import QThread,pyqtSignal,Qt,QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QSizePolicy,
                             QWidget,
                             QVBoxLayout,
                             QHBoxLayout,
                             QLabel,
                             QPushButton,
                             QSystemTrayIcon,
                             QStyle,
                             QMenu,
                             QAction,
                             QDesktopWidget,
                             qApp)


from time import sleep,localtime,strftime
from sys import exit, argv
from os import path
import sys


screenSize = 0,0


        
        
class Thread(QThread):
    timeNow = pyqtSignal(str)
    
    def run(self):
        while True:
            t = localtime()
            self.Time = strftime("%I:%M:%S",t)
            self.timeNow.emit(str(self.Time))
            sleep(1)
        
        

class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Time")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        # self.setWindowOpacity(0.5)
        # self.setStyleSheet("background-color: #000")
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowFlags(Qt.FramelessWindowHint| Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint | Qt.ToolTip)
        # self.setWindowFlags( QtCore.Qt.FramelessWindowHint)
        # self.setWindowFlags(
        # QtCore.Qt.Window |
        # QtCore.Qt.CustomizeWindowHint |
        # QtCore.Qt.WindowTitleHint |
        # QtCore.Qt.WindowCloseButtonHint |
        # QtCore.Qt.WindowStaysOnTopHint
        # )
        self.isTransparency = False
        self.ui()
        self.desine()
        self.tray()
        self.thread = Thread()
        self.thread.timeNow.connect(self.setTime)
        self.thread.start()
        self.leaveEvent = lambda e:self.windowLeave(e)
        self.enterEvent = lambda e:self.windowEnter(e)
        
    
    def ui(self):
        self.wid = QWidget()
        self.VBox = QVBoxLayout()
        self.HBox = QHBoxLayout()
        self.HBoxMain = QHBoxLayout()
        
        self.TimeLabel = QLabel("")
        
        self.ExitButton = QPushButton()
        
        self.MaxButton = QPushButton()
        
        self.HideButton = QPushButton()
        
        self.TransparencyButton = QPushButton()
        
        
        self.HBox.addWidget(self.ExitButton)
        self.HBox.addWidget(self.MaxButton)
        self.HBox.addWidget(self.TransparencyButton)
        self.HBox.addWidget(self.HideButton)
        
        self.VBox.addLayout(self.HBox)
        self.VBox.addWidget(self.TimeLabel,alignment=Qt.AlignCenter)
        self.wid.setLayout(self.VBox)
        self.HBoxMain.addWidget(self.wid)
        self.setLayout(self.HBoxMain)
        
    def desine(self):
        # self.setFixedSize(200,70)
        self.TimeLabel.setStyleSheet("QLabel{font-size:50px; color:#ffffff;}")
        # self.TimeLabel.adjustSize()
        # self.TimeLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.wid.setStyleSheet("background-color: rgba(0,0,0,0.3)")
        
        self.ExitButton.setStyleSheet("background-color: rgba(225,225,225,0)")
        self.ExitButton.setIcon(QIcon(resource_path('image\\close.png')))
        self.ExitButton.clicked.connect(self.EXIT)
        self.ExitButton.hide()
        self.ExitButton.leaveEvent = lambda e:self.ExitButtonLeave(e)
        self.ExitButton.enterEvent = lambda e:self.ExitButtonEnter(e)
        
        self.MaxButton.setStyleSheet("background-color: rgba(225,225,225,0)")
        self.MaxButton.setIcon(QIcon(resource_path('image\\maximize.png')))
        self.MaxButton.clicked.connect(self.MAX)
        self.MaxButton.hide()
        self.MaxButton.leaveEvent = lambda e:self.MaxButtonLeave(e)
        self.MaxButton.enterEvent = lambda e:self.MaxButtonEnter(e)
        
        self.TransparencyButton.setStyleSheet("background-color: rgba(225,225,225,0)")
        self.TransparencyButton.setIcon(QIcon(resource_path('image\\opacity.png')))
        self.TransparencyButton.clicked.connect(self.Transparency)
        self.TransparencyButton.hide()
        self.TransparencyButton.leaveEvent = lambda e:self.TransparencyButtonLeave(e)
        self.TransparencyButton.enterEvent = lambda e:self.TransparencyButtonEnter(e)
        
        self.HideButton.setStyleSheet("background-color: rgba(225,225,225,0)")
        self.HideButton.setIcon(QIcon(resource_path('image\\minus.png')))
        self.HideButton.clicked.connect(self.HIDE)
        self.HideButton.hide()
        self.HideButton.leaveEvent = lambda e:self.HideButtonLeave(e)
        self.HideButton.enterEvent = lambda e:self.HideButtonEnter(e)
        
        self.HBox.setContentsMargins(0,0,0,0)
        # self.HBox.addStretch()
        self.VBox.setContentsMargins(0,0,0,0)
        self.HBoxMain.setContentsMargins(0,0,0,0)
        self.wid.setContentsMargins(0,0,0,0)
    
    def setTime(self, time):
        self.TimeLabel.setText(str(time))
    
    def ExitButtonLeave(self,_):       
        self.ExitButton.setIconSize(QSize(24, 20))
    
    def ExitButtonEnter(self,_):
        self.ExitButton.setIconSize(QSize(28, 24))
    
    def HideButtonLeave(self,_):
        self.HideButton.setIconSize(QSize(24, 20))
    
    def HideButtonEnter(self,_):
        self.HideButton.setIconSize(QSize(28, 24))
    
    def MaxButtonLeave(self,_):
        self.MaxButton.setIconSize(QSize(24, 20))
    
    def MaxButtonEnter(self,_):
        self.MaxButton.setIconSize(QSize(28, 24))
        
    def TransparencyButtonLeave(self,_):
        self.MaxButton.setIconSize(QSize(24, 20))
    
    def TransparencyButtonEnter(self,_):
        self.MaxButton.setIconSize(QSize(28, 24))
    
    def windowLeave(self,_):
        w = self.size()
        if (w.width()< 300):
            self.wid.setStyleSheet("background-color: rgba(0,0,0,0.3)")
            self.ExitButton.hide()
            self.HideButton.hide()
            self.MaxButton.hide()
            self.setFixedSize(200,70)
    
    def windowEnter(self,_):
        w = self.size()
        if (w.width()< 300):
            self.setFixedSize(200,90)
            self.wid.setStyleSheet("background-color: rgba(0,0,0,0.6)")
            self.ExitButton.show()
            self.HideButton.show()
            self.MaxButton.show()
    
    def HIDE(self):
        # self.showMinimized()
        self.hide() 
    def EXIT(_):
        qApp.quit()
    def Transparency(self):

        
        if self.isTransparency:
            self.isTransparency = False
            self.wid.setStyleSheet("background-color: rgba(0,0,0,0.3)")
            self.TransparencyButton.setIcon(QIcon(resource_path('image\\opacity.png')))
        else:
            self.wid.setStyleSheet("background-color: rgba(0,0,0,1)")
            self.TransparencyButton.setIcon(QIcon(resource_path('image\\transparency.png')))
            self.isTransparency = True
    def MAX(self):
        
        w = self.size()
        print(w.width())
        
        if w.width() < 300:

            sizeObject = QDesktopWidget().screenGeometry(-1)
            print(" Screen size : "  + str(sizeObject.height()) + "x"  + str(sizeObject.width()))
            self.move(0,0)
            self.setFixedSize(sizeObject.width(),sizeObject.height())
            self.TimeLabel.setStyleSheet("QLabel{font-size:150px; color:#ffffff;}")
            self.MaxButton.setIcon(QIcon(resource_path('image\\minimize.png'),))
            self.TransparencyButton.show()
            self.isTransparency = False
            self.wid.setStyleSheet("background-color: rgba(0,0,0,0.3)")
            self.TransparencyButton.setIcon(QIcon(resource_path('image\\opacity.png')))

        else:

            self.setFixedSize(200,70)
            self.TimeLabel.setStyleSheet("QLabel{font-size:50px; color:#ffffff;}")
            self.MaxButton.setIcon(QIcon(resource_path('image\\maximize.png')))
            self.TransparencyButton.hide()

        
    def tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.messageClicked.connect(lambda: self.show())
        self.tray_icon.activated.connect(self.systemIcon)
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        self.tray_icon.setIcon(QIcon(resource_path("image\\clock.png")))
        tray_menu = QMenu()
        show_action = QAction("Show", self)
        quit_action = QAction("Exit", self)
        hide_action = QAction("Hide", self)
        show_action.triggered.connect(lambda: self.show())
        hide_action.triggered.connect(lambda: self.hide())
        quit_action.triggered.connect(qApp.quit)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show() 
    
    def systemIcon(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            print ('Clicked')
            self.show()  
    
    def mousePressEvent(self,event):
        w = self.size()
        if (w.width()< 300):
            if event.button() == Qt.LeftButton:
                self.moving = True
                self.offset = event.pos()

    def mouseMoveEvent(self,event):
        w = self.size()
        if (w.width()< 300):
            if self.moving:
                self.move(event.globalPos()-self.offset)
        
        

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = path.abspath(".")

    return path.join(base_path, relative_path)
if __name__ == "__main__":
    app = QApplication(argv)
    window = MainWindow()
    window.show()
    exit(app.exec_())
            

        
        