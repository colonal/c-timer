
from typing import overload
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import QThread,pyqtSignal,Qt,QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QLineEdit, QSizePolicy,
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


from time import sleep,localtime,strftime, time
from datetime import datetime
from sys import exit, argv
from os import path
import sys


screenSize = 0,0


def  QCustomLabel():
    label = QLabel()
    label.setText(":")
    label.setStyleSheet("""
                    QLabel{
                            color:#fff;
                            font-size:25px;
                            }
                        """)
    return label
        
class Thread(QThread):
    timeNow = pyqtSignal(str)
    brack = True
    
    def run(self):
        while self.brack:
            t = localtime()
            self.Time = strftime("%I:%M:%S",t)
            self.timeNow.emit(str(self.Time))
            sleep(1)
    
    def changeStopwatchStates(self):
        self.brack = not self.brack
    
    def changeStopwatchStop(self):
        self.brack = False

class ThreadStopwatch(QThread):
    timeNow = pyqtSignal(str)
    brack = False
    t = "00:00:00"
    def run(self):
        c = 0
        
        while self.brack:
            #############################################
            d = str(self.t)
            h,m,s = map(int,d.split(":"))
            h = int(h)
            m=int(m)
            s= int(s)
            if(s<59):
                s+=1
            elif(s==59):
                s=0
                if(m<59):
                    m+=1
                elif(m==59):
                    m=0
                    h+=1
            if(h<10):
                h = str(0)+str(h)
            else:
                h= str(h)
            if(m<10):
                m = str(0)+str(m)
            else:
                m = str(m)
            if(s<10):
                s=str(0)+str(s)
            else:
                s=str(s)
            self.Time =h+":"+m+":"+s
            #############################################
            self.t = self.Time
            self.timeNow.emit(str(self.Time))
            sleep(1)
            c += 1
    
    def resetTimer(self):
        self.t = "00:00:00"
        self.timeNow.emit("00:00:00")
    
    def changeStopwatchStates(self):
        self.brack = not self.brack
    
    def timer(self,count,time):
        
        if(count==0):
            d = str(time)
            h,m,s = map(int,d.split(":"))
            h = int(h)
            m=int(m)
            s= int(s)
            if(s<59):
                s+=1
            elif(s==59):
                s=0
                if(m<59):
                    m+=1
                elif(m==59):
                    m=0
                    h+=1
            if(h<10):
                h = str(0)+str(h)
            else:
                h= str(h)
            if(m<10):
                m = str(0)+str(m)
            else:
                m = str(m)
            if(s<10):
                s=str(0)+str(s)
            else:
                s=str(s)
            d =h+":"+m+":"+s          
            return d
            
        
class ThreadTemporary(QThread):
    timeNow = pyqtSignal(str)
    brack = False
    t = "00:00:00"
    def run(self):
        c = 0
        
        while self.brack:         
            #############################################
            d = str(self.t)
            h,m,s = map(int,d.split(":"))
            h = int(h)
            m=int(m)
            s= int(s)
            
            if(s>0):
                s -=1
            elif(s==0):
                s=59
                if(m > 0):
                    m -= 1
                elif(m==0):
                    m=59
                    if h == 0:
                        self.timeNow.emit(str("End Temporary"))
                        break
                    h -= 1
            if(h<10):
                h = str(0)+str(h)
            else:
                h= str(h)
            if(m<10):
                m = str(0)+str(m)
            else:
                m = str(m)
            if(s<10):
                s=str(0)+str(s)
            else:
                s=str(s)
            self.Time =h+":"+m+":"+s
            #############################################
            self.t = self.Time
            self.timeNow.emit(str(self.Time))
            sleep(1)
            c += 1
    
    def resetTimer(self):
        self.t = "00:00:00"
        self.timeNow.emit("00:00:00")
    
    def setTimer(self, time):
        self.t = time;
        self.timeNow.emit(time)
        
    def changeStopwatchStates(self):
        self.brack = not self.brack
    
    def changeStopwatchStop(self):
        self.brack = False
class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Time")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint| Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint | Qt.ToolTip)
        self.isTransparency = False
        self.StopwatchStates = False
        self.StopwatchPlayStates = False
        self.TemporaryPlayStates = False
        self.TemporaryStates = False
        self.ui()
        self.desine()
        self.tray()
        self.threadTimer = Thread()
        self.threadTimer.timeNow.connect(self.setTime)
        self.threadTimer.start()
        
        self.ThreadStopwatch = ThreadStopwatch()
        self.ThreadStopwatch.timeNow.connect(self.setTime)
        
        self.ThreadTemporary = ThreadTemporary()
        self.ThreadTemporary.timeNow.connect(self.setTime)
        
        self.leaveEvent = lambda e:self.windowLeave(e)
        self.enterEvent = lambda e:self.windowEnter(e)
        
    
    def ui(self):
        self.wid = QWidget()
        self.VBox = QVBoxLayout()
        self.HBox = QHBoxLayout()
        self.HBoxMain = QHBoxLayout()
        self.VBoxButtonRight = QVBoxLayout()
        self.VBoxButtonLeft = QVBoxLayout()
        self.HBoxTB = QHBoxLayout()
        
        self.TimeLabel = QLabel("")
        
        self.TemporaryWidget = QWidget()
        self.TemporaryWidget.hide()
        
        self.LineHours = QLineEdit()
        
        self.LineMinutes = QLineEdit()
        
        self.LineSeconds = QLineEdit()
        
        self.Stopwatch = QPushButton()
        
        self.Temporary = QPushButton()
        
        self.StopwatchPlay = QPushButton()
        
        self.StopwatchResut = QPushButton()
        
        self.TemporaryPlay = QPushButton()
        
        self.TemporaryResut = QPushButton()
        
        self.ExitButton = QPushButton()
        
        self.MaxButton = QPushButton()
        
        self.HideButton = QPushButton()
        
        self.TransparencyButton = QPushButton()
        
        
        self.HBox.addWidget(self.ExitButton)
        self.HBox.addWidget(self.MaxButton)
        self.HBox.addWidget(self.TransparencyButton)
        self.HBox.addWidget(self.HideButton)
        
        self.VBox.addLayout(self.HBox)
        
        self.VBoxButtonRight.addWidget(self.Stopwatch)
        
        self.VBoxButtonRight.addWidget(self.Temporary)
        
        self.VBoxButtonLeft.addWidget(self.StopwatchPlay)
        self.VBoxButtonLeft.addWidget(self.StopwatchResut)
        self.VBoxButtonLeft.addWidget(self.TemporaryPlay)
        self.VBoxButtonLeft.addWidget(self.TemporaryResut)
        self.VBox.addStretch()
        self.HBoxTB.addLayout(self.VBoxButtonLeft)
        self.HBoxTB.addStretch()
        self.HBoxTB.addWidget(self.TimeLabel,alignment=Qt.AlignCenter)
        self.HBoxTB.addWidget(self.TemporaryWidget,alignment=Qt.AlignCenter)
        self.HBoxTB.addStretch()
        self.HBoxTB.addLayout(self.VBoxButtonRight)
        
        self.VBox.addLayout(self.HBoxTB)
        self.VBox.addStretch()
        
        self.wid.setLayout(self.VBox)
        self.HBoxMain.addWidget(self.wid)
        self.setLayout(self.HBoxMain)
        
    def desine(self):
        self.TimeLabel.setStyleSheet("QLabel{font-size:50px; color:#ffffff;}")
        self.wid.setStyleSheet("background-color: rgba(0,0,0,0.3)")
        
        self.Stopwatch.setStyleSheet("background-color: rgba(225,225,225,0)")
        self.Stopwatch.setIcon(QIcon(resource_path('image\\stopwatchS.png')))
        self.Stopwatch.clicked.connect(self.StopwatchChange)
        self.Stopwatch.hide()
        self.Stopwatch.setToolTip("Stopwatch")
        
        self.Temporary.setStyleSheet("background-color: rgba(225,225,225,0)")
        self.Temporary.setIcon(QIcon(resource_path('image\\temporary.png')))
        self.Temporary.clicked.connect(self.TemporaryChange)
        self.Temporary.hide()
        self.Temporary.setToolTip("Temporary")
        
        self.StopwatchPlay.setStyleSheet("background-color: rgba(225,225,225,0)")
        self.StopwatchPlay.setIcon(QIcon(resource_path('image\\power-button.png')))
        self.StopwatchPlay.clicked.connect(self.StopwatchPlayChange)
        self.StopwatchPlay.hide()
        
        self.StopwatchResut.setStyleSheet("background-color: rgba(225,225,225,0)")
        self.StopwatchResut.setIcon(QIcon(resource_path('image\\arrow.png')))
        self.StopwatchResut.clicked.connect(self.StopwatchResutChange)
        self.StopwatchResut.hide()
        
        
        self.TemporaryPlay.setStyleSheet("background-color: rgba(225,225,225,0)")
        self.TemporaryPlay.setIcon(QIcon(resource_path('image\\power-button.png')))
        self.TemporaryPlay.clicked.connect(self.TemporaryPlayChange)
        self.TemporaryPlay.hide()
        
        self.TemporaryResut.setStyleSheet("background-color: rgba(225,225,225,0)")
        self.TemporaryResut.setIcon(QIcon(resource_path('image\\arrow.png')))
        self.TemporaryResut.clicked.connect(self.TemporaryResutChange)
        self.TemporaryResut.hide()
        
        
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
        
        self.TemporaryWidgetUI()
        
        self.HBox.setContentsMargins(0,0,0,0)
        self.HBox.addStretch()
        self.VBox.setContentsMargins(0,0,0,0)
        self.HBoxMain.setContentsMargins(0,0,0,0)
        self.VBoxButtonRight.setContentsMargins(0,0,0,0)
        self.VBoxButtonLeft.setContentsMargins(0,0,0,0)
        self.wid.setContentsMargins(0,0,0,0)
    
    def TemporaryWidgetUI(self):
        hBox = QHBoxLayout()
        
        rx  = QtCore.QRegExp("[0-9]{2}")                               
        val = QtGui.QRegExpValidator(rx)                              
        self.LineHours.setValidator(val)
        self.LineHours.setText("00")
        self.LineHours.setSelection(0,2)
        
        self.LineHours.textChanged.connect(lambda: self.TextChanged(self.LineHours,self.LineMinutes))
        self.LineMinutes.setValidator(val)
        self.LineMinutes.setText("00")
        self.LineMinutes.setSelection(0,2)
        self.LineMinutes.textChanged.connect(lambda: self.TextChanged(self.LineMinutes,self.LineSeconds))
        self.LineSeconds.setValidator(val)
        self.LineSeconds.setText("00")
        self.LineSeconds.setSelection(0,2)
        
        hBox.addWidget(self.LineHours)
        hBox.addWidget(QCustomLabel())
        hBox.addWidget(self.LineMinutes)
        hBox.addWidget(QCustomLabel())
        hBox.addWidget(self.LineSeconds)
        
        hBox.setContentsMargins(0,0,0,0)
        self.TemporaryWidget.setContentsMargins(0,0,0,0)
        
        self.TemporaryWidget.setLayout(hBox)
        
        self.LineHours.setStyleSheet(self.LineStyle())
        self.LineMinutes.setStyleSheet(self.LineStyle())
        self.LineSeconds.setStyleSheet(self.LineStyle())
    def LineStyle (self) -> str:
        return """
                QLineEdit{
                    color:#fff;
                    font-size:15px;
                }
                """
    def TextChanged(self,widget,nextF):
        if len(widget.text()) >= 2:
            nextF.setFocus()
            
    def setTime(self, time):
        if time =="End Temporary":
            self.TemporaryPlayChange()
            self.TimeLabel.setText("00:00:00")
            return
        self.TimeLabel.setText(str(time))
    
    def TemporaryPlayChange(self):
        Hours  = self.LineHours.text()
        Minutes  = self.LineMinutes.text()
        Seconds  = self.LineSeconds.text()
        
        if (not self.TemporaryPlayStates):
            
            self.TemporaryPlayStates = True
            if self.TemporaryWidget.isVisible() or self.TimeLabel.text() == "00:00:00":
                self.ThreadTemporary.setTimer(f"{Hours}:{Minutes}:{int(Seconds)+1}")
            self.TemporaryWidget.hide()
            self.TimeLabel.show()
            
            self.threadTimer.changeStopwatchStates()
            self.ThreadTemporary.changeStopwatchStates()
            
            
            self.ThreadTemporary.start()
            self.TemporaryPlay.setIcon(QIcon(resource_path('image\\stop-button.png')))
            
        else:
            self.TemporaryPlayStates = False
            self.TemporaryPlay.setIcon(QIcon(resource_path('image\\power-button.png')))
            self.ThreadTemporary.changeStopwatchStates()
            
            
        
    
    def TemporaryResutChange(self):
        self.TemporaryPlayChange()
        self.ThreadTemporary.resetTimer()
        self.TimeLabel.hide()
        self.TemporaryWidget.show()
    
    def StopwatchResutChange(self):
        self.ThreadStopwatch.resetTimer()
    
    def StopwatchChange(self):
        if not self.StopwatchStates :
            self.setTime("00:00:00")
            self.ThreadTemporary.changeStopwatchStop()
            self.Temporary.setIcon(QIcon(resource_path('image\\temporary.png')))
            self.TemporaryStates = False
            self.TemporaryPlayStates = False   
            self.TemporaryWidget.hide()
            self.TemporaryPlay.hide()
            self.TemporaryResut.hide()
            self.TimeLabel.show()
            
            if self.size().width()<300:
                self.TimeLabel.setStyleSheet("QLabel{font-size:35px;color:#ffffff;}")
            else:
                self.TimeLabel.setStyleSheet("QLabel{font-size:150px;color:#ffffff;}")
            self.StopwatchStates = True
            self.threadTimer.changeStopwatchStates()
            self.Stopwatch.setIcon(QIcon(resource_path('image\\stopwatchE.png')))
            self.StopwatchPlay.show()
            self.StopwatchResut.show()
            self.setTime("00:00:00")
            
        else:
            if self.size().width()<300:
                self.TimeLabel.setStyleSheet("QLabel{font-size:35px;color:#ffffff;}")
            else:
                self.TimeLabel.setStyleSheet("QLabel{font-size:150px;color:#ffffff;}")
            self.StopwatchStates = False
            self.StopwatchPlay.hide()
            self.StopwatchResut.hide()
            self.threadTimer.changeStopwatchStates()
            if(not self.threadTimer.brack):
                self.threadTimer.brack = True
            self.threadTimer.start()
            self.Stopwatch.setIcon(QIcon(resource_path('image\\stopwatchS.png')))

    def TemporaryChange(self):
        if not self.TemporaryWidget.isVisible():
            if  self.StopwatchStates:
                self.StopwatchChange()
            if(self.ThreadStopwatch.brack):
                self.ThreadStopwatch.brack = False
            self.TemporaryStates = True
            if self.size().width()<300:
                self.TimeLabel.setStyleSheet("QLabel{font-size:35px;color:#ffffff;}")
            else:
                self.TimeLabel.setStyleSheet("QLabel{font-size:150px;color:#ffffff;}")
            self.TimeLabel.hide()
            self.TemporaryWidget.show()
            self.LineHours.setFocus()
            self.TemporaryPlay.show()
            self.TemporaryResut.show()
            self.StopwatchPlay.hide()
            self.StopwatchResut.hide()
            self.Temporary.setIcon(QIcon(resource_path('image\\temporary-offer.png')))
            
                
        else:
            self.TemporaryStates = False
            if self.size().width()<300:
                self.TimeLabel.setStyleSheet("QLabel{font-size:35px;color:#ffffff;}")
            else:
                self.TimeLabel.setStyleSheet("QLabel{font-size:150px;color:#ffffff;}")
                
            if(self.threadTimer.brack == False):
                self.threadTimer.brack = True
                self.threadTimer.start()
            self.TimeLabel.show()
            self.TemporaryWidget.hide()
            self.TemporaryPlay.hide()
            self.TemporaryResut.hide()
            self.Temporary.setIcon(QIcon(resource_path('image\\temporary.png')))
                    
    def StopwatchPlayChange(self):
        if not self.StopwatchPlayStates:
            self.StopwatchPlayStates = True
            self.ThreadStopwatch.changeStopwatchStates()
            self.ThreadStopwatch.start()
            self.StopwatchPlay.setIcon(QIcon(resource_path('image\\stop-button.png')))
            
        else:
            self.StopwatchPlay.setIcon(QIcon(resource_path('image\\power-button.png')))
            self.StopwatchPlayStates = False
            self.ThreadStopwatch.changeStopwatchStates()
    
    
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
            self.TimeLabel.setStyleSheet("QLabel{font-size:50px;color:#ffffff;}")
            self.ExitButton.hide()
            self.HideButton.hide()
            self.MaxButton.hide()
            self.Stopwatch.hide()
            self.Temporary.hide()
            self.StopwatchPlay.hide()
            self.StopwatchResut.hide()
            self.TemporaryPlay.hide()
            self.TemporaryResut.hide()
            self.setFixedSize(200,70)
    
    def windowEnter(self,_):
        w = self.size()
        if (w.width()< 300):
            self.setFixedSize(210,90)
            self.TimeLabel.setStyleSheet("QLabel{font-size:35px;color:#ffffff;}")
            self.wid.setStyleSheet("background-color: rgba(0,0,0,0.6)")
            self.ExitButton.show()
            self.HideButton.show()
            self.MaxButton.show()
            self.Stopwatch.show()
            self.Temporary.show()
            
            if  self.StopwatchStates:
                self.TimeLabel.setStyleSheet("QLabel{font-size:35px;color:#ffffff;}")
                self.StopwatchPlay.show()
                self.StopwatchResut.show()
            
            if self.TemporaryStates:
                self.TimeLabel.setStyleSheet("QLabel{font-size:35px;color:#ffffff;}")
                self.TemporaryPlay.show()
                self.TemporaryResut.show()
    
    def HIDE(self):
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
        
        if w.width() < 300:

            sizeObject = QDesktopWidget().screenGeometry(-1)
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
            

        
        