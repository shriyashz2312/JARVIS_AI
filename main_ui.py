import sys
import threading
import psutil

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel,
    QVBoxLayout, QHBoxLayout, QPushButton
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

from hud_core import HUDCore
from waveform import Waveform
from background_grid import BackgroundGrid
from voice import JarvisVoice
from listener import JarvisListener
from commands import CommandProcessor


class JarvisUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("J.A.R.V.I.S")
        self.setFixedSize(1400, 800)

        # 🔥 Futuristic background
        self.setStyleSheet("""
        QMainWindow {
            background-color: qradialgradient(
                cx:0.5, cy:0.5, radius:1,
                stop:0 #0a2740,
                stop:0.6 #020914,
                stop:1 #00060c
            );
            color: #00f6ff;
        }
        """)

        # Core systems
        self.voice = JarvisVoice()
        self.listener = JarvisListener()
        self.commander = CommandProcessor(self.voice)

        self.voice.speak("System online. Jarvis activated.")

        self.init_ui()
        self.start_monitor()

    # ================= UI ================= #

    def init_ui(self):
        grid = BackgroundGrid(self)
        grid.setGeometry(0, 0, 1400, 800)
        grid.lower()

        central = QWidget()
        central.setStyleSheet("background: transparent;")
        self.setCentralWidget(central)

        main = QHBoxLayout(central)
        main.setContentsMargins(20, 20, 20, 20)
        main.setSpacing(20)

        # LEFT PANEL
        left = self.hud_panel()
        ll = QVBoxLayout(left)
        ll.addWidget(self.title("LISTENING"))
        ll.addWidget(Waveform())

        btn = QPushButton("START LISTENING")
        btn.setStyleSheet(self.btn_style())
        btn.clicked.connect(self.listen)
        ll.addWidget(btn)
        ll.addStretch()

        # CENTER CORE
        center = QVBoxLayout()
        center.addStretch()
        center.addWidget(HUDCore(), alignment=Qt.AlignCenter)
        center.addStretch()

        # RIGHT PANEL
        right = self.hud_panel()
        rl = QVBoxLayout(right)

        rl.addWidget(self.title("RESPONDING"))

        msg = QLabel("How can I assist you?")
        msg.setStyleSheet("""
            QLabel {
                color: #c9f7ff;
                padding: 6px;
                font-size: 12px;
            }
        """)
        rl.addWidget(msg)

        rl.addSpacing(20)
        rl.addWidget(self.title("SYSTEM STATUS"))

        self.cpu = QLabel("CPU: 0%")
        self.ram = QLabel("RAM: 0%")

        for lbl in (self.cpu, self.ram):
            lbl.setStyleSheet("""
                QLabel {
                    color: #c9f7ff;
                    padding: 6px;
                    font-size: 12px;
                }
            """)

        rl.addWidget(self.cpu)
        rl.addWidget(self.ram)
        rl.addStretch()

        main.addWidget(left, 2)
        main.addLayout(center, 3)
        main.addWidget(right, 2)

        bottom = QLabel("Awake, Jarvis...")
        bottom.setAlignment(Qt.AlignCenter)
        bottom.setStyleSheet("""
            background-color: rgba(0, 30, 60, 180);
            padding: 12px;
            border-top: 1px solid #00f6ff;
        """)
        bottom.setParent(self)
        bottom.setGeometry(0, 750, 1400, 50)

    def hud_panel(self):
        w = QWidget()
        w.setStyleSheet("""
        QWidget {
            background-color: rgba(0, 25, 45, 180);
            border: 1px solid #00f6ff;
            border-radius: 16px;
        }
        """)
        return w

    def title(self, text):
        l = QLabel(text)
        l.setFont(QFont("Orbitron", 15))
        l.setAlignment(Qt.AlignLeft)
        l.setStyleSheet("""
            QLabel {
                color: #00f6ff;
                background-color: rgba(0, 60, 100, 200);
                padding: 8px 14px;
                border: 1px solid #00f6ff;
                border-radius: 10px;
                letter-spacing: 3px;
            }
        """)
        return l

    def btn_style(self):
        return """
        QPushButton {
            background-color: rgba(0, 40, 70, 200);
            border: 1px solid #00f6ff;
            padding: 14px;
            color: #00f6ff;
            border-radius: 10px;
        }
        QPushButton:hover {
            background-color: #00f6ff;
            color: black;
        }
        """

    # ================= VOICE THREAD ================= #

    def listen(self):
        threading.Thread(
            target=self.listen_loop,
            daemon=True
        ).start()

    def listen_loop(self):
        self.voice.speak("Listening mode activated")

        while True:
            text = self.listener.listen_once()
            if not text:
                continue

            result = self.commander.process(text)

            if result == "STOP":
                self.voice.speak("Listening stopped")
                break

    # ================= SYSTEM MONITOR ================= #

    def start_monitor(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(1000)

    def update_stats(self):
        self.cpu.setText(f"CPU: {psutil.cpu_percent()}%")
        self.ram.setText(f"RAM: {psutil.virtual_memory().percent}%")


# ================= MAIN ================= #

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = JarvisUI()
    win.show()
    sys.exit(app.exec_())
