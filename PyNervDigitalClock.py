import time
import sys
import math
import platform
import cpuinfo
import psutil
import string
from queue import Queue
from PySide.QtCore import *
from PySide.QtGui import *
import threading


class PyNervDigitalClock(QDialog):

    def __init__(self):
        self.strSysInfo = ""
        super(PyNervDigitalClock, self).__init__()
        self.InitUI()
        self.MainTimer = QTimer(self)
        self.MainTimer.timeout.connect(self.MainTimer_Tick)
        self.MainTimer.start(1000)

    def MainTimer_Tick(self):
        # get the current local time in hh:mm:ss format
        self.lblTimeDisplay.setText(time.strftime('%H:%M:%S'))
        self.lblDateDisplay.setText(time.strftime('<center><b>%A</b><br>%d %B %Y</center>'))
        self.lblSysInfo.setText(self.SysInfoString())

    def SysInfoString(self):
        SysInfo = '<b>System Information</b>'
        SysInfo += '<br>OS : {0}'.format(platform.platform())
        SysInfo += '<br>CPU : {0}'.format(cpuinfo.get_cpu_info()['brand'])
        SysInfo += '<br>CPU Utilization : '
        CPUPercent = psutil.cpu_percent(interval = 0, percpu = True)
        for a in CPUPercent:
            SysInfo += 'CPU#{1} : {0}% '.format(a, CPUPercent.index(a))
        MemInfo = psutil.virtual_memory()
        SysInfo += '<br>RAM Total : {0:.2} GB, Used : {1} %'.format(MemInfo.total / math.pow(1024,3), 
                                                                    MemInfo.percent)
        return SysInfo

    def InitUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedWidth(620)
        self.setFixedHeight(400)
        self.setWindowTitle("NERV Digital Clock")

        # lblTimeDisplay
        self.lblTimeDisplay = QLabel(self)
        self.lblTimeDisplay.move(208, 50)
        self.lblTimeDisplay.setStyleSheet('font-size: 50px; font-family:"Roboto"; font-weight:bold; color:rgb(150,100,0); text-align:center;')
        self.lblTimeDisplay.setText(time.strftime('%H:%M:%S'))

        # lblDateDisplay
        self.lblDateDisplay = QLabel(self)
        self.lblDateDisplay.move(185,105)
        self.lblDateDisplay.setFixedWidth(250)
        self.lblDateDisplay.setStyleSheet('font-size: 17px; font-family:"Roboto"; font-weight:light; color:rgb(150,100,0); text-align:center;')
        self.lblDateDisplay.setText(time.strftime('<center><b>%A</b><br>%d %B %Y</center>'))

        #lblSysInfo
        self.lblSysInfo = QLabel(self)
        self.lblSysInfo.move(20,250)
        self.lblSysInfo.setFixedWidth(200)
        self.lblSysInfo.setWordWrap(True)
        self.lblSysInfo.setStyleSheet('font-size: 12px; font-family:"Roboto"; font-weight:light; color:rgb(150,100,0); text-align:center;')
        self.lblSysInfo.setText(self.SysInfoString())
        self.show()

    def sizeHint(self):
        return QSize(625, 480)

    
    def mousePressEvent(self, event):
        self.offset = event.pos()

    def mouseMoveEvent(self, event):
        x = event.globalX()
        y = event.globalY()
        x_w = self.offset.x()
        y_w = self.offset.y()
        self.move(x-x_w, y-y_w)

    def paintEvent(self, event):
        # All decorations go here
        w = 200
        h = 200
        r = 200/2.0
        n = 6
        wf = 220
        hf = 220
        rf = 220/2.0
        maginame = ['Melchior 1', 'Balthasar 2', 'Casper 3']
        qp = QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.Antialiasing);
        qp.setPen(Qt.NoPen)
        qp.setBrush(QColor(0, 0, 0, 200))
        qp.drawRect(0, 5, 620, 395)
        qp.setBrush(QColor(30, 15, 5, 200))
        qp.drawRect(0, 5, 620, 395)
        
        # Draw top/bottom red border
        for a in range(-1, 63):
            qp.setBrush(QColor(150, 0, 0, 230))
            if a % 2 != 0 :
                qpolyb = QPolygon()
                qpolyu = QPolygon()
                if a < 31 :
                    qpolyb << QPoint(10 + 10 * a, 380) << QPoint(20 + 10 * a, 380) << QPoint(10 + 10 * a, 400) << QPoint(0 + 10 * a, 400)
                    qpolyu << QPoint(0 + 10 * a, 5) << QPoint(10 + 10 * a, 5) << QPoint(20 + 10 * a, 25) << QPoint(10 + 10 * a, 25)
                else :
                    if a >= 31 and a < 61:
                        qpolyb << QPoint(0 + 10 * a, 380) << QPoint(10 + 10 * a, 380) << QPoint(20 + 10 * a, 400) << QPoint(10 + 10 * a, 400)
                        qpolyu << QPoint(10 + 10 * a, 5) << QPoint(20 + 10 * a, 5) << QPoint(10 + 10 * a, 25) << QPoint(0 + 10 * a, 25)
                    else :
                        qpolyb << QPoint(0 + 10 * a, 380) << QPoint(10 + 10 * a, 380) << QPoint(10 + 10 * a, 400)
                        qpolyu << QPoint(10 + 10 * a, 5) << QPoint(10 + 10 * a, 25) << QPoint(0 + 10 * a, 25)

                qp.drawPolygon(qpolyb)
                qp.drawPolygon(qpolyu)
        
        # Draw hexagons
        for m in range(1,4):    
            qp.setPen(Qt.NoPen);
            qpoly = QPolygon()
            xtext = 0
            ytext = 0
            qpolyf = QPolygon()
            for i in range(0,7):
                x = r * math.cos(2 * math.pi * i / n) + (w * m - 20 * m) - 50
                if i == 3: 
                    xtext = x 
                y = h - r * math.sin(2 * math.pi * i / n) + 50
                if m % 2 != 0:
                    y = h / 2 - r * math.sin(2 * math.pi * i / n)  + 50
                if i == 3:
                    ytext = y
                qpoly << QPoint(x,y)
                xf = (rf * math.cos(2 * math.pi * i / n) + (wf * m - 20 * m)) - 20 * m - 50
                yf = hf - rf * math.sin(2 * math.pi * i / n) + 30
                if m % 2 != 0:
                    yf = hf/2-rf*math.sin(2*math.pi*i/n) + 40
                qpolyf << QPoint(xf,yf)
            qp.drawPolygon(qpoly)
            qp.setPen(QColor(150,100,0,255))
            qp.drawPolyline(qpolyf)
            qp.setFont(QFont('Droid Sans', 10, weight = QFont.Weight.DemiBold))
            qp.drawText(QPoint(xtext + 15, ytext - 5), "MAGI")
            qp.setFont(QFont('Droid Sans', 19, weight = QFont.Weight.DemiBold) )
            qp.drawText(QPoint(xtext + 14, ytext + 15), maginame[m-1])

        # Draw borders
        qp.setPen(QColor(150,100,0,255))
        qp.setBrush(QColor(150,100,0,255))
        qp.drawRect(195, 355, 224, 18)
        qp.drawLine(QPoint(10, 50),QPoint(10, 355))
        qp.drawLine(QPoint(610, 50),QPoint(610, 355))

        qp.drawLine(QPoint(20, 40), QPoint(600, 40))
        qp.drawLine(QPoint(10, 35), QPoint(10, 45))
        qp.drawLine(QPoint(5, 40),QPoint(15, 40))
        qp.drawLine(QPoint(610, 35), QPoint(610, 45))
        qp.drawLine(QPoint(605, 40),QPoint(615, 40))

        qp.drawLine(QPoint(20, 365), QPoint(600, 365))
        qp.drawLine(QPoint(10, 360), QPoint(10, 370))
        qp.drawLine(QPoint(5,365),QPoint(15,365))
        qp.drawLine(QPoint(610, 360), QPoint(610, 370))
        qp.drawLine(QPoint(605,365),QPoint(615,365))

        qp.setPen(QColor(30, 15, 5, 200))
        qp.setFont(QFont('Droid Sans', 12, weight = QFont.Weight.DemiBold))
        qp.drawText(QPoint(200, 370), "FOR NERV PERSONNEL ONLY")
        qp.setOpacity(0.85)
        qp.drawPixmap(QRect(410, 250,(330/100)*50,(210/100)*50), QPixmap('nerv wall.png'))
        qp.end()

a = QApplication(sys.argv)
rw = PyNervDigitalClock()
rw.show()
a.exec_()
