from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPainter, QPen, QColor
import math


class HUDCore(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(320, 320)
        self.a1 = 0
        self.a2 = 180

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(25)

    def animate(self):
        self.a1 = (self.a1 + 1) % 360
        self.a2 = (self.a2 - 2) % 360
        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        c = self.rect().center()

        p.setPen(QPen(QColor(0, 200, 255), 3))
        p.drawArc(10, 10, 300, 300, self.a1 * 16, 280 * 16)

        p.setPen(QPen(QColor(0, 150, 220), 2))
        p.drawArc(45, 45, 230, 230, self.a2 * 16, 220 * 16)

        p.setPen(QPen(QColor(0, 246, 255), 1))
        p.drawEllipse(90, 90, 140, 140)

        p.setBrush(QColor(0, 246, 255))
        p.setPen(QColor(0, 246, 255))
        p.drawEllipse(c, 10, 10)

        p.setPen(QPen(QColor(0, 200, 255), 1))
        for i in range(0, 360, 12):
            r = math.radians(i + self.a1)
            x1 = c.x() + math.cos(r) * 130
            y1 = c.y() + math.sin(r) * 130
            x2 = c.x() + math.cos(r) * 150
            y2 = c.y() + math.sin(r) * 150
            p.drawLine(int(x1), int(y1), int(x2), int(y2))
