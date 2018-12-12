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
squares = []
START_TIME = 5


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
    self.timer = QTimer()
    #self.set_time()
    self.timer.timeout.connect(self.counter)
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

    self.set_img_numbers(list(range(1,ROWS*COLS+1,1)))
    #self.shuffle()

def set_img_numbers(self,numbers):
    self.scene.clear()
    squares.clear()
    u = 0
    for y in range(COLS):
        for x in range(ROWS):
            obj = Square(x * XYSIDE, y * XYSIDE,numbers[u])
            self.scene.addItem(obj)
            squares.append(obj)
            u += 1




def AnimeButton_clicked(self):
    try:
        self.animation = QPropertyAnimation(AnimSquare(squares[0]), b'pos')
        self.animation.setDuration(200)
        self.animation.setStartValue(QPointF(0, 0))
        self.animation.setKeyValueAt(0.3, QPointF(0, 30))
        self.animation.setKeyValueAt(0.5, QPointF(0, 60))
        self.animation.setKeyValueAt(0.8, QPointF(0, 90))
        self.animation.setEndValue(QPointF(0, 120))
        self.animation.start()
        '''
        self.animation = QPropertyAnimation(AnimSquare(squares[0]), b'angle')
        self.animation.setDuration(8000)
        self.animation.setStartValue(-90)
        self.animation.setKeyValueAt(0.3, -10)
        self.animation.setKeyValueAt(0.5, 0)
        self.animation.setKeyValueAt(0.8, 10)
        self.animation.setEndValue(30)
        self.animation.start()
        '''

    except Exception as e:
        print(e)