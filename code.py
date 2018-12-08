#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QPushButton, QWidget, QDialog, QApplication, QMainWindow, QGraphicsScene, QGraphicsItem, \
    QGraphicsRectItem, QGraphicsSceneMouseEvent
from PyQt5.QtCore import Qt, QMimeData, QPoint
from PyQt5.QtGui import QDrag, QImage, QColor
from PyQt5 import uic
import random

COLS = 3
ROWS = 3
MARGIN = 40
XYSIDE = 32

class Square (QGraphicsRectItem):
    def __init__(self, sx, sy):
        super().__init__()
        self.image = QImage()
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)

        self.setRect(0, 0, XYSIDE, XYSIDE)
        self.startX = sx + MARGIN
        self.startY = sy + MARGIN
        self.setPos(self.startX, self.startY)
        self.clr = random.randint(0xFF000000, 0xFFFFFFFF)

    def paint(self, painter, option, widget):
        super().paint(painter, option, widget)
        if self.image.isNull():
            painter.fillRect(1, 1, XYSIDE - 1, XYSIDE - 1, QColor(self.clr))
        else:
            painter.drawImage(QPoint(1, 1), self.image)

    def mousePressEvent(self, mevent):
        super().mousePressEvent(mevent)
        self.startX = self.pos().x()
        self.startY = self.pos().y()
        pass

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        try:
            scenePt = self.mapToScene(event.pos())
            cur_x = scenePt.x()
            cur_y = scenePt.y()
            print(scenePt)
            self.check_pos(cur_x,cur_y)
        except Exception as e:
            print(e)

    def check_pos(self,cur_x,cur_y):
        comp1 = cur_x >= MARGIN + 140 and cur_x <= (MARGIN + 140) + COLS * XYSIDE
        comp2 = cur_y >= MARGIN  and cur_y <= MARGIN  + ROWS * XYSIDE
        comp3 = cur_x >= MARGIN  and cur_x <= (MARGIN) + COLS * XYSIDE
        comp4 = cur_y >= MARGIN  and cur_y <= MARGIN  + ROWS * XYSIDE
        if not ((comp1 and comp2) or (comp3 and comp4)) :
            print(123)
            self.setPos(self.startX, self.startY)
        if (cur_x > MARGIN + XYSIDE * COLS):
            self.insert_in_cell(MARGIN + 140,MARGIN,cur_x,cur_y)
        else:
            self.insert_in_cell(MARGIN , MARGIN,cur_x,cur_y)

    def insert_in_cell(self,x_square_start,y_square_start,cur_x,cur_y):
        for iy in range(COLS):
            for ix in range(ROWS):
                comp1 = cur_x >= x_square_start + XYSIDE * ix and cur_x <= x_square_start + XYSIDE * (ix + 1)
                comp2 = cur_y >=y_square_start + XYSIDE * iy and cur_y <= y_square_start  + XYSIDE * (iy + 1)
                if comp1 and comp2:
                    self.setPos(x_square_start + XYSIDE * ix, y_square_start + XYSIDE * iy)

class Scene (QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.setSceneRect(0, 0, 700, 500)

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
            painter.fillRect(0, 0, 10, 10, Qt.GlobalColor.red)

            self.drawSquare(painter, MARGIN, MARGIN)
            self.drawSquare(painter, MARGIN + 140, MARGIN)
        except Exception as e:
            print(e)

class MainWnd(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('MainWindow.ui', self)
        scene = Scene()
        self.graphicsView.setScene(scene)
        for y in range(COLS):
            for x in range(ROWS):
                scene.addItem(Square(x * XYSIDE, y * XYSIDE))

    def accept(self):
        pass

    def reject(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWnd()
    ex.show()
    app.exec_()
