from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPainter, QPen, QColor
import random


class Waveform(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(70)
        self.data = [10] * 50

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_wave)
        self.timer.start(80)

    def update_wave(self):
        self.data.pop(0)
        self.data.append(random.randint(5, 30))
        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        h = self.height()
        step = self.width() // len(self.data)

        # 🔵 GLOW PASS (soft outer glow)
        glow_pen = QPen(QColor(0, 246, 255, 80), 6)
        p.setPen(glow_pen)
        for i, v in enumerate(self.data):
            x = i * step
            p.drawLine(x, h // 2 - v, x, h // 2 + v)

        # 🔵 MAIN WAVE (sharp cyan)
        main_pen = QPen(QColor(0, 246, 255), 2)
        p.setPen(main_pen)
        for i, v in enumerate(self.data):
            x = i * step
            p.drawLine(x, h // 2 - v, x, h // 2 + v)
