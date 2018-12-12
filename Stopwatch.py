import sys
from PyQt5.QtWidgets import QPushButton, QWidget, QDialog, QApplication, QMainWindow, QGraphicsScene, QGraphicsItem, \
    QGraphicsRectItem, QGraphicsSceneMouseEvent, QGraphicsEllipseItem, QFrame, QLabel
from PyQt5.QtCore import Qt, QMimeData, QPoint, QRect, QSize, QRectF, QSizeF, QPropertyAnimation, QTimeLine, QObject, \
    QTimer, QTime
from PyQt5.QtGui import QDrag, QImage, QColor
from PyQt5 import uic
import random
import winsound
from PyQt5.QtWidgets import (QApplication, QGraphicsView,
        QGraphicsPixmapItem, QGraphicsScene)
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtCore import (QObject, QPointF,
        QPropertyAnimation, pyqtProperty)
import sys
#qwe
from PyQt5.uic.properties import QtGui
from Square import *
from View import *
COLS = 3
ROWS = 3
MARGIN = 40
#размер квадратика (мб потом станет прямоугольничком ,который не квадратик )
XYSIDE = 60
# это отступ для второго поля
MARGIN2 = 400
# квадратик ( элемент пазла ,мб в будущем переделан в прямоугольничек ,который не квадратик )
squares = []



class Stopwatch():
    def __init__(self,t,btn_start_game,label_timer):
        self.START_TIME = t
        self.btn_start_game = btn_start_game
        self.label_timer = label_timer
        self.sec = self.START_TIME
        self.timer = QTimer()
        self.timer.timeout.connect(self.counter)
        self.set_time()
        self.part_one = False
        self.part_two = False

    def start(self,n):
        self.timer.start(1000)
        self.btn_start_game.setEnabled(False)
        if n == 1:
            self.part_one = True
        else:
            self.part_one = False
            self.part_two = True

    def reset(self):
        self.timer.stop()
        self.sec = self.START_TIME
        self.btn_start_game.setEnabled(True)
        self.set_time()

    def counter(self):
        self.sec -= 1
        self.set_time()
        if self.sec == 0 and self.part_one:
            self.reset()
        elif self.sec == 0 and self.part_two:
            self.reset()

    def is_timer_active(self):
        return self.timer.isActive()

    def end_part_one(self):
        pass

    def end_part_two(self):
        pass



    def set_time(self):
        #hora = self.sec / 3600
        minutos = (self.sec % 3600) / 60
        segundos = (self.sec % 3600) % 60
        try:
            self.text = '<html><head/><body><p align="center"><span style=" font-size:48pt;">{}</span></p></body></html>'.format("%02d:%02d" % (minutos, segundos))
            #self.label_timer.setText("%02d:%02d:%02d" % (hora, minutos, segundos))
            self.label_timer.setText(self.text)
        except Exception as e:
            print(e)