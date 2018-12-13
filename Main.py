import sys
from PyQt5.QtWidgets import QPushButton, QWidget, QDialog, QApplication, QMainWindow, QGraphicsScene, QGraphicsItem, \
    QGraphicsRectItem, QGraphicsSceneMouseEvent, QGraphicsEllipseItem, QFrame, QLabel
from PyQt5.QtCore import Qt, QMimeData, QPoint, QRect, QSize, QRectF, QSizeF, QPropertyAnimation, QTimeLine, QObject, \
    QTimer, QTime
from PyQt5.QtGui import QDrag, QImage, QColor, QTransform
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
from Stopwatch import *
from View import *

COLS = 3
ROWS = 3
MARGIN = 40
# размер квадратика (мб потом станет прямоугольничком ,который не квадратик )
XYSIDE = 60
# это отступ для второго поля
MARGIN2 = 400
# квадратик ( элемент пазла ,мб в будущем переделан в прямоугольничек ,который не квадратик )


# qwe


class MainWnd(QWidget):

    def __init__(self):
        super().__init__()
        self.squares = []
        self.ans = []
        self.true_ans = []
        self.START_TIME = 10
        initUI(self)
        self.stopWatch = Stopwatch(self.START_TIME, self.btn_start_game, self.label_timer,self.label,self)

    def confirm(self):
        self.ans = []
        for y in range(0, COLS ):
            for x in range(0, ROWS):
                y_cord = MARGIN + XYSIDE * y + 1
                x_cord = MARGIN + MARGIN2 + XYSIDE * x + 1
                #print(x_cord,y_cord)
                u = -1
                try:
                    u = self.scene.itemAt(x_cord, y_cord, QTransform())
                    index = self.squares.index(u)
                #print(u)
                except Exception:
                    continue

                self.ans.append(self.squares[index].number)
        if self.ans == self.true_ans:
            self.label.setStyleSheet("QLabel { background-color : white; color : green; }")
            self.label.setText('Правильно!')
            self.label.setStyleSheet("QLabel { background-color : white;}")
        else:
            self.label.setStyleSheet("QLabel { background-color : white; color : red; }")
            self.label.setText('Неверно')
            self.label.setStyleSheet("QLabel { background-color : white;}")
        self.btn_start_game.setEnabled(True)
        self.btn_confirm.setEnabled(False)


    def start_game(self):
        self.btn_confirm.setEnabled(True)
        try:
            self.shuffle()
            text2 = 'Запоминайте расположение квадратов'
            self.squares_movable(0)
            for elem in self.squares:
                print(elem.ItemIsMovable)
            # statusText_set_text(self,text2)
            self.label.setText(text2)
            self.stopWatch.start(1)
            #self.stopWatch.timer.stop()
        except Exception as e:
            print(e)

    def shuffle(self):
        print('я начинаю мешать')
        numbers = [i for i in range(1, ROWS * COLS + 1, 1)]
        random.shuffle(numbers)
        self.true_ans = numbers
        set_img_numbers(self, numbers)

    def squares_movable(self,bool):
        for elem in self.squares:
            elem.setFlag(QGraphicsItem.ItemIsMovable, bool)
            elem.setFlag(QGraphicsItem.ItemIsSelectable, bool)


    '''
    def AnimeButton_clicked(self):
        try:
            self.animation = QPropertyAnimation(AnimSquare(self.squares[0]), b'pos')
            self.animation.setDuration(200)
            self.animation.setStartValue(QPointF(0, 0))
            self.animation.setKeyValueAt(0.3, QPointF(0, 30))
            self.animation.setKeyValueAt(0.5, QPointF(0, 60))
            self.animation.setKeyValueAt(0.8, QPointF(0, 90))
            self.animation.setEndValue(QPointF(0, 120))
            self.animation.start()
            
            self.animation = QPropertyAnimation(AnimSquare(squares[0]), b'angle')
            self.animation.setDuration(8000)
            self.animation.setStartValue(-90)
            self.animation.setKeyValueAt(0.3, -10)
            self.animation.setKeyValueAt(0.5, 0)
            self.animation.setKeyValueAt(0.8, 10)
            self.animation.setEndValue(30)
            self.animation.start()
            
    '''



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWnd()
    ex.show()
    app.exec_()
