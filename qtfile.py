import threading

from PyQt6.QtCore import QSize, QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QProgressBar
from PyQt6 import uic
import qclasses

import sys, main


WINDOW = None


def window_init():
    global WINDOW
    app = QApplication(sys.argv)

    WINDOW = qclasses.MainWindow()
    WINDOW.show()
    thread = threading.Thread(target=main.load, daemon=True)
    thread.start()
    qclasses.signalHub.answer.connect(WINDOW.set_text_output)

    app.exec()


if __name__ == "__main__":
    window_init()
