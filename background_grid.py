from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QPen


class BackgroundGrid(QWidget):
    def paintEvent(self, e):
        p = QPainter(self)
        p.setPen(QPen(QColor(0, 246, 255, 25), 1))

        step = 45
        w, h = self.width(), self.height()

        for x in range(0, w, step):
            p.drawLine(x, 0, x, h)
        for y in range(0, h, step):
            p.drawLine(0, y, w, y)
