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

from PyQt5.uic.properties import QtGui
from Square import *
COLS = 3
ROWS = 3
MARGIN = 40
#размер квадратика (мб потом станет прямоугольничком ,который не квадратик )
XYSIDE = 60
# это отступ для второго поля
MARGIN2 = 400
# квадратик ( элемент пазла ,мб в будущем переделан в прямоугольничек ,который не квадратик )




class Scene (QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.setSceneRect(0, 0, 700, 500)
    #отрисовывать поле
    def drawSquare(self, painter, x0, y0):
        try:
            for x in range(COLS + 1):
                painter.drawLine(x0 + x * XYSIDE, y0, x0 + x * XYSIDE, y0 + XYSIDE * ROWS)
            for y in range(ROWS + 1):
                painter.drawLine(x0, y0 + y * XYSIDE, x0 + XYSIDE * COLS, y0 + y * XYSIDE)
        except Exception as e:
            print(e)

    def drawBackground(self, painter, rect):
        try:
            super().drawBackground(painter, rect)
            #painter.fillRect(self.sceneRect, Qt.GlobalColor.green)
            #просток так
            painter.fillRect(0, 0, 10, 10, Qt.GlobalColor.red)
            #отрисовываем 2 поля
            self.drawSquare(painter, MARGIN, MARGIN)
            self.drawSquare(painter, MARGIN + MARGIN2, MARGIN)
        except Exception as e:
            print(e)


def initUI(self):
    uic.loadUi('MainWindow.ui', self)
    #print('u',self.label_timer.text())
    START_TIME = 5

    #self.set_time()

    #устанавдиваем сцену
    self.scene = Scene()
    #графиксвью - это отображение сцены
    #у одной сцены может быть несколько графиксвью
    #например,одна будет иметь поворот 0 градусов ,а дургая 180 (и они будут одновремменно
    #отображать сцену
    self.graphicsView.setScene(self.scene)
    #добавляем квадратики c картиночками
    self.btn_start_game.clicked.connect(self.start_game)
    self.btn_confirm.clicked.connect(self.confirm)

    set_img_numbers(self,list(range(1,ROWS*COLS+1,1)))
    #self.shuffle()

def set_img_numbers(self,numbers):
    self.scene.clear()
    self.squares.clear()
    u = 0
    for y in range(COLS):
        for x in range(ROWS):
            obj = Square(x * XYSIDE, y * XYSIDE,numbers[u],self)
            self.scene.addItem(obj)
            self.squares.append(obj)
            u += 1
