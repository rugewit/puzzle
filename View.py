import sys
from PyQt5.QtWidgets import QPushButton, QWidget, QDialog, QApplication, QMainWindow, QGraphicsScene, QGraphicsItem, \
    QGraphicsRectItem, QGraphicsSceneMouseEvent, QGraphicsEllipseItem, QFrame, QLabel, QGraphicsTextItem
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
# qwe
from PyQt5.uic.properties import QtGui
from Square import *
import settings


# квадратик ( элемент пазла ,мб в будущем переделан в прямоугольничек ,который не квадратик )


class Scene(QGraphicsScene):
    def __init__(self,win):
        super().__init__()
        self.setSceneRect(0, 0, 700, 500)

    # отрисовывать поле
    def drawSquare(self, painter, x0, y0):
        try:
            for x in range(settings.COLS + 1):
                painter.drawLine(x0 + x * settings.XYSIDE, y0, x0 + x * settings.XYSIDE, y0 + settings.XYSIDE * settings.ROWS)
            for y in range(settings.ROWS + 1):
                painter.drawLine(x0, y0 + y * settings.XYSIDE, x0 + settings.XYSIDE * settings.COLS, y0 + y * settings.XYSIDE)
        except Exception as e:
            print(e)

    def drawBackground(self, painter, rect):
        try:
            super().drawBackground(painter, rect)
            # отрисовываем 2 поля
            self.drawSquare(painter, settings.MARGIN, settings.MARGIN)
            self.drawSquare(painter, settings.MARGIN + settings.MARGIN2, settings.MARGIN)
        except Exception as e:
            print(e)


def initUI(self):
    uic.loadUi('MainWindow.ui', self)

    # устанавдиваем сцену
    self.scene = Scene(self)
    # графиксвью - это отображение сцены
    # у одной сцены может быть несколько графиксвью
    # например,одна будет иметь поворот 0 градусов ,а дургая 180 (и они будут одновремменно
    # отображать сцену
    self.graphicsView.setScene(self.scene)
    # добавляем квадратики c картиночками
    self.btn_start_game.clicked.connect(self.start_game)
    self.btn_confirm.clicked.connect(self.confirm)
    self.btn_confirm.setEnabled(False)
    #self.lineEdit_time[str].connect(self.change_time)
    self.btn_change_time.clicked.connect(self.change_time)
    text1 = 'После нажатия на кнопку "играем!" у вас будет {} секунд на то ,чтобы запомнить расположение квадратов.'.format(settings.TIME)
    self.label = QLabel()
    #автопереносы
    self.label.setWordWrap(True)
    self.label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter | Qt.AlignCenter)
    self.label.setFont(QFont("monospace", 18))
    self.label.setText(text1)
    self.label.setStyleSheet("QLabel { background-color : white}")
    self.scene.addWidget(self.label).setGeometry(QRectF(50, settings.MARGIN + settings.XYSIDE * settings.ROWS+2, 600, 200))
    set_img_numbers(self, list(range(1, settings.ROWS * settings.COLS + 1, 1)))
    # self.shuffle()

#установить квадраты с числами
def set_img_numbers(self, numbers):
    for elem in self.scene.items():
        if type(elem) == Square:
            self.scene.removeItem(elem)
    self.squares.clear()
    u = 0
    for y in range(settings.COLS):
        for x in range(settings.ROWS):
            obj = Square(x * settings.XYSIDE, y * settings.XYSIDE, numbers[u], self)
            self.scene.addItem(obj)
            self.squares.append(obj)
            u += 1

