import cv2
import numpy as np

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen, QPolygon
from PyQt5.QtCore import Qt, QTimer, QRect, QPoint

from traider_bots.VisualTraider_v2 import VisualTraider_v2

def draw_borders(img,traider:VisualTraider_v2):
    attrs = vars(traider)
    for item in attrs.items():
        i = item[1]
        if type(i) == tuple:
            if len(i) == 4:
                points = np.array([[i[0],i[1]],[i[2],i[1]],[i[2],i[3]],[i[0],i[3]]], np.int32)
                cv2.polylines(img,[points],True,(255,0,0),1)
    cv2.imwrite('screens\windows.png',img)


class DrawingWindow(QMainWindow):
    def __init__(self, trader_list):
        super().__init__()
        self.setWindowTitle("Transparent Drawing Window")
        self.setGeometry(0, 0, QApplication.desktop().screenGeometry().width(),
                         QApplication.desktop().screenGeometry().height())
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.painter = QPainter()
        self.painter.setRenderHint(QPainter.Antialiasing)
        self.pen_color = QColor(255, 0, 0)  # Set the initial pen color to red
        self.pen_width = 1  # Set the initial pen width to 4
        self.trader_list = trader_list  # Store the coordinates for drawing rectangles
        self.draw_timer = QTimer()
        self.draw_timer.start(10)  # Update the window every 10 milliseconds

    def paintEvent(self, event):
        self.painter.begin(self)
        self.painter.setPen(Qt.NoPen)
        self.painter.setBrush(QBrush(Qt.transparent))
        self.painter.drawRect(QRect(0, 0, self.width(), self.height()))  # Draw a transparent background
        self.painter.setPen(QPen(QColor(self.pen_color), self.pen_width))
        self.painter.setBrush(QBrush(Qt.transparent))
        for trader in self.trader_list:
            self.draw_trader(trader)
        self.painter.end()
        QTimer.singleShot(1000, self.update)  # Schedule a repaint after 1 second
        
    def draw_trader(self,trader):
        attrs = vars(trader)
        for item in attrs.items():
            i = item[1]
            if type(i) == tuple:
                if len(i) == 4:
                    points = [[i[0],i[1]],[i[2],i[1]],[i[2],i[3]],[i[0],i[3]]]
                    qplg = QPolygon()
                    for p in points:
                        qplg.append(QPoint(p[0],p[1]))
                    self.painter.drawPolyline(qplg)

def draw_borders_online(list_traders:list):
    app = QApplication([])
    window = DrawingWindow(list_traders)  # Create an instance of the DrawingWindow class with the given coordinates
    window.show()  # Display the window
    app.exec_()