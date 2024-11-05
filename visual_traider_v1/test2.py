import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen, QPolygon
from PyQt5.QtCore import Qt, QTimer, QRect, QPoint

from traider_bots.Collector1 import Collector1 as Traider1
from wrappers.GroupBotWrapper import GroupBotWrapper

gbw = GroupBotWrapper(
    Traider1,
    ['Stock1','Stock2','Stock3','Stock4'],
    51,
    1364,
    529,
    222,
    474,
    499,
    701,
    60,
    1)


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
        self.pen_width = 4  # Set the initial pen width to 4
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


if __name__ == "__main__":
    # coordinates = [(524, 474, 818-524, 689-474), (524, 367, 818-524, 473-367)]

    app = QApplication(sys.argv)

    window = DrawingWindow(gbw.traders)  # Create an instance of the DrawingWindow class with the given coordinates
    window.show()  # Display the window

    sys.exit(app.exec_())  # Start the application event loop and exit when it's finished

