#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QPushButton, QWidget, QDialog, QApplication, QMainWindow, QGraphicsScene, QGraphicsItem, \
    QGraphicsRectItem, QGraphicsSceneMouseEvent,QGraphicsEllipseItem ,QFrame
from PyQt5.QtCore import Qt, QMimeData, QPoint, QRect, QSize, QRectF, QSizeF, QPropertyAnimation, QTimeLine, QObject, \
    QTimer
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
COLS = 3
ROWS = 3
MARGIN = 40
#размер квадратика (мб потом станет прямоугольничком ,который не квадратик )
XYSIDE = 60
# это отступ для второго поля
MARGIN2 = 400
# квадратик ( элемент пазла ,мб в будущем переделан в прямоугольничек ,который не квадратик )
squares = []
class Square (QGraphicsRectItem):
    def __init__(self, sx, sy,img_number):
        super().__init__()
        self.image = QImage('numbers/{}.jpg'.format(img_number))
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        #задаём его размеры ,первые 2 арга можно игнорировать
        self.setRect(0, 0, XYSIDE, XYSIDE)
        #задаём его координаты
        self.startX = sx + MARGIN
        self.startY = sy + MARGIN
        self.setPos(self.startX, self.startY)
        #цвет
        #self.clr = random.randrange(0xFF000000,0xFFFFFFFF,1000000)
        self.clr = random.randint(0xFF000000, 0xFFFFFFFF)
        #self.setTextureImage(self.image)
    #функция его отрисовки
    def paint(self, painter, option, widget):
        super().paint(painter, option, widget)
        if self.image.isNull():
            #единицы сделаны ,чтобы объеки имел рамку
            painter.fillRect(1, 1, XYSIDE - 1, XYSIDE - 1, QColor(self.clr))
        else:
            #painter.drawImage(QPoint(0, 0), self.image)
            painter.drawImage(QPoint(1, 1), self.image)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        #это параметр ,который регулирует то , будет ли данный объект над другими при перемещении или нет
        #когда мы перемещаем квадратик ,он должен быть над всеми другими ,поэтому ставим 1
        self.start_ZValue = self.zValue()
        self.setZValue(1)
        #тут сохраняем его изначальные координаты ,чтобы при перемещении в "неправильную область"
        #он вернулся на место
        self.startX = self.pos().x()
        self.startY = self.pos().y()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        try:
            #тк просто получая координаты ивета ,мы получим координаты щелчка мыши относительно квадратика
            #мы должны их перевести в аболютные координаты
            scenePt = self.mapToScene(event.pos())
            cur_x = scenePt.x()
            cur_y = scenePt.y()
            #print(scenePt)
            self.check_pos(cur_x,cur_y)
        except Exception as e:
            print(e)
        #возвращаем начальный зет-параметр ,чтобы ZValue=1 был только у перемещаемого квадрата
        self.setZValue(self.start_ZValue)


    def check_pos(self,cur_x,cur_y):
        self.handle_collision(cur_x,cur_y)
        if stop_handle_collision:
            return
        #тут проверяется ,находится ли щелчок мыши внутри первого или второго поля
        comp1 = cur_x >= MARGIN + MARGIN2 and cur_x <= (MARGIN + MARGIN2) + COLS * XYSIDE
        comp2 = cur_y >= MARGIN  and cur_y <= MARGIN  + ROWS * XYSIDE
        comp3 = cur_x >= MARGIN  and cur_x <= (MARGIN) + COLS * XYSIDE
        comp4 = cur_y >= MARGIN  and cur_y <= MARGIN  + ROWS * XYSIDE
        #если ни в первом поле ,ни во втором ,то возращаем на место
        if not ((comp1 and comp2) or (comp3 and comp4)) :
            print(123)
            self.setPos(self.startX, self.startY)
            return
        #если х правее ,чем конец первого поля ,то обращаемся ко второму
        if (cur_x > MARGIN + XYSIDE * COLS):
            self.insert_in_cell(MARGIN + MARGIN2,MARGIN,cur_x,cur_y)
        #в ином случаее к первому
        else:
            self.insert_in_cell(MARGIN , MARGIN,cur_x,cur_y)
    #тут просто смотрим ,в какую ячейку щелчок попал и ставим квадратик в соотвествующую позицию
    def insert_in_cell(self,x_square_start,y_square_start,cur_x,cur_y):
        for iy in range(COLS):
            for ix in range(ROWS):
                comp1 = cur_x >= x_square_start + XYSIDE * ix and cur_x <= x_square_start + XYSIDE * (ix + 1)
                comp2 = cur_y >=y_square_start + XYSIDE * iy and cur_y <= y_square_start  + XYSIDE * (iy + 1)
                if comp1 and comp2:
                    self.setPos(x_square_start + XYSIDE * ix, y_square_start + XYSIDE * iy)

    def handle_collision(self,cur_x,cur_y):
        global stop_handle_collision
        stop_handle_collision = False
        print('***')
        CollObj = None
        for elem in squares:
            #если рассматриваемый объект(elem) не равен текущему(self) и рассматриваемый объект содержит точку щелчка мыши
            if elem != self and QRectF(elem.pos(), QSizeF(XYSIDE, XYSIDE)).contains(QPoint(cur_x,cur_y)):
                CollObj = elem
        #если была коллизия и щелчок был на 2-ом поле и текущий объект был изначально на втором поле
        if CollObj != None and cur_x >= MARGIN + MARGIN2 and self.startX >= MARGIN + MARGIN2:
            # свопаем
            first_x,first_y = CollObj.pos().x(),CollObj.pos().y()
            second_x,second_y =self.startX,self.startY
            CollObj.setPos(second_x,second_y)
            self.setPos(first_x,first_y)
            stop_handle_collision = True
        #если была коллизия всё-таки ,но прошлые условия не выполнелись
        elif CollObj != None:
            print('возвращаю обратно')
            self.setPos(self.startX, self.startY)
            stop_handle_collision = True
#класс - оболочная ,нужный ,чтобы класс анимаций связать с квадратати
class AnimSquare(QObject):
    def __init__(self, p_square):
        super().__init__()
        self.square = p_square

    def _set_pos(self, pos):
        self.square.setPos(pos)

    def _set_angle(self, angle):
        self.square.setRotation(angle)

    pos = pyqtProperty(QPointF, fset=_set_pos)
    angle = pyqtProperty(float, fset=_set_angle)

#сцена ,на которой всё отрисовывается
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

class MainWnd(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        timer = QTimer()


    def initUI(self):
        uic.loadUi('MainWindow.ui', self)
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

    def confirm(self):
        pass

    def start_game(self):
        print('нав')

    def shuffle(self):
        print('я начинаю мешать')
        numbers = [i for i in range(1,ROWS*COLS+1,1)]
        random.shuffle(numbers)
        self.set_img_numbers(numbers)


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
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWnd()
    ex.show()
    app.exec_()
