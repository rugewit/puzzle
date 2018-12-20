from PyQt5.QtWidgets import  QGraphicsItem, QGraphicsRectItem
from PyQt5.QtCore import Qt, QPoint,  QRectF, QSizeF
from PyQt5.QtGui import QImage, QTextOption, QFont, QBrush, QColor
import random
from PyQt5.QtCore import (QObject, QPointF,pyqtProperty)
import settings
#квадратик
class Square (QGraphicsRectItem):
    def __init__(self, sx, sy,number,win):
        super().__init__()
        
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        #задаём его размеры ,первые 2 арга можно игнорировать
        self.setRect(0, 0, settings.XYSIDE, settings.XYSIDE)
        #задаём его координаты
        self.startX = sx + settings.MARGIN
        self.startY = sy + settings.MARGIN
        self.setPos(self.startX, self.startY)
        #цвет
        #self.clr = random.randint(0xFF000000, 0xFFFFFFFF)
        #экземляр класса MainWnd
        self.win = win
        #номер квадратика
        self.number = number
    #функция его отрисовки
    def paint(self, painter, option, widget):
        super().paint(painter, option, widget)
        painter.setFont(QFont("Roboto", 30))
        painter.fillRect(QRectF(1, 1, settings.XYSIDE - 1, settings.XYSIDE - 1), QColor("red"))
        painter.drawText(QRectF(1, 1, settings.XYSIDE - 1, settings.XYSIDE - 1), str(self.number), QTextOption(Qt.AlignmentFlag.AlignCenter))

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
        #тк просто получая координаты ивета ,мы получим координаты щелчка мыши относительно квадратика
        #мы должны их перевести в аболютные координаты
        scenePt = self.mapToScene(event.pos())
        cur_x = scenePt.x()
        cur_y = scenePt.y()
        self.check_pos(cur_x,cur_y)
        #возвращаем начальный зет-параметр ,чтобы ZValue=1 был только у перемещаемого квадрата
        self.setZValue(self.start_ZValue)


    def check_pos(self,cur_x,cur_y):
        self.handle_collision(cur_x,cur_y)
        if stop_handle_collision:
            return
        #тут проверяется ,находится ли щелчок мыши внутри первого или второго поля
        comp1 = cur_x >= settings.MARGIN + settings.MARGIN2 and cur_x <= (settings.MARGIN + settings.MARGIN2) + settings.COLS * settings.XYSIDE
        comp2 = cur_y >= settings.MARGIN  and cur_y <= settings.MARGIN  + settings.ROWS * settings.XYSIDE
        comp3 = cur_x >= settings.MARGIN  and cur_x <= (settings.MARGIN) + settings.COLS * settings.XYSIDE
        comp4 = cur_y >=settings.MARGIN  and cur_y <= settings.MARGIN  + settings.ROWS * settings.XYSIDE
        #если ни в первом поле ,ни во втором ,то возращаем на место
        if not ((comp1 and comp2) or (comp3 and comp4)) :
            print(123)
            self.setPos(self.startX, self.startY)
            return
        #если х правее ,чем конец первого поля ,то обращаемся ко второму
        if (cur_x > settings.MARGIN + settings.XYSIDE * settings.COLS):
            self.insert_in_cell(settings.MARGIN + settings.MARGIN2,settings.MARGIN,cur_x,cur_y)
        #в ином случаее к первому
        else:
            self.insert_in_cell(settings.MARGIN , settings.MARGIN,cur_x,cur_y)
    #тут просто смотрим ,в какую ячейку щелчок попал и ставим квадратик в соотвествующую позицию
    def insert_in_cell(self,x_square_start,y_square_start,cur_x,cur_y):
        for iy in range(settings.COLS):
            for ix in range(settings.ROWS):
                comp1 = cur_x >= x_square_start + settings.XYSIDE * ix and cur_x <= x_square_start + settings.XYSIDE * (ix + 1)
                comp2 = cur_y >=y_square_start + settings.XYSIDE * iy and cur_y <= y_square_start  + settings.XYSIDE * (iy + 1)
                if comp1 and comp2:
                    self.setPos(x_square_start + settings.XYSIDE * ix, y_square_start + settings.XYSIDE * iy)

    def handle_collision(self,cur_x,cur_y):
        global stop_handle_collision
        stop_handle_collision = False
        CollObj = None
        for elem in self.win.squares:
            #если рассматриваемый объект(elem) не равен текущему(self) и рассматриваемый объект содержит точку щелчка мыши
            if elem != self and QRectF(elem.pos(), QSizeF(settings.XYSIDE, settings.XYSIDE)).contains(QPoint(cur_x,cur_y)):
                CollObj = elem
        #если была коллизия и щелчок был на 2-ом поле и текущий объект был изначально на втором поле
        if CollObj != None and cur_x >= settings.MARGIN + settings.MARGIN2 and self.startX >= settings.MARGIN + settings.MARGIN2:
            # свопаем
            first_x,first_y = CollObj.pos().x(),CollObj.pos().y()
            second_x,second_y =self.startX,self.startY
            CollObj.setPos(second_x,second_y)
            self.setPos(first_x,first_y)
            stop_handle_collision = True
        #если была коллизия всё-таки ,но прошлые условия не выполнелись
        elif CollObj != None:
            self.setPos(self.startX, self.startY)
            stop_handle_collision = True
# (на будущее)
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