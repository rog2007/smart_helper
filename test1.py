from PyQt6.QtCore import QSize, QTimer, QObject, pyqtSignal
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QProgressBar, QHBoxLayout, QLabel, QWidget, QScrollArea, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6 import uic

import sys

userMessageStyle = ("background-color:#C7FFA2;"
                    "padding:10px;"
                    "border-radius:15%;"
                    "margin-left:30px;")

botMessageStyle = ("background-color:#AAE385;"
                   "padding:10px;"
                   "border-radius:15%;"
                   "margin-left:30px;")


def format_user_message(text):
    label = QLabel(text)
    label.setStyleSheet(userMessageStyle)
    label.setAlignment(Qt.AlignmentFlag.AlignRight)
    label.setWordWrap(True)
    label.setScaledContents(True)
    label.adjustSize()
    layout = QHBoxLayout()
    spacer = QSpacerItem(1, 1, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
    layout.addItem(spacer)
    layout.addWidget(label)
    return layout


def format_bot_message(text):
    label = QLabel(text)
    label.setStyleSheet(userMessageStyle)
    label.setAlignment(Qt.AlignmentFlag.AlignLeft)
    label.setWordWrap(True)
    label.setScaledContents(True)
    label.adjustSize()
    layout = QHBoxLayout()
    spacer = QSpacerItem(1, 1, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
    layout.addWidget(label)
    layout.addItem(spacer)
    return layout


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("mainwindow_test.ui", self)

        self.progress.setMinimum(0)
        self.progress.setMaximum(100)
        self.progressValue = 0
        self.progressTarget = 0

        self.mysign = signalHub
        self.mysign.loadSignal.connect(self.set_progress_target)
        #self.mysign.earsSignal.connect(self.ears_heard)

        self.textInput.returnPressed.connect(self.request_processing)

        self.set_progress_target(100)

        #self.installEventFilter(self)

    def move_progress(self):
        if self.progressValue < self.progressTarget:
            self.progressValue += 1
            self.progress.setValue(self.progressValue)
        else:
            self.timer.stop()

        print(self.progressValue, self.progress.maximum())
        if self.progressValue == self.progress.maximum():
            self.pageChoose.setCurrentIndex(1)

    def set_progress_target(self, target):
        self.progressTarget = target
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.move_progress)
        self.timer.start()

    def request_processing(self):
        text = self.textInput.text()
        self.verticalLayout_3.addLayout(format_user_message(text))
        signalHub.question.emit(text)

    def set_text_output(self, a):
        #print("!!дошло", a)
        self.textOutput.setText(a)


class mySignalHub(QObject):
    loadSignal = pyqtSignal(int)
    question = pyqtSignal(str)
    answer = pyqtSignal(str)
    earsSignal = pyqtSignal(str)



signalHub = mySignalHub()


app = QApplication(sys.argv)
WINDOW = MainWindow()
WINDOW.show()
app.exec()


# app = QApplication([])
#
# layout = QVBoxLayout()
# for i in range(10):
#     for j in range(5):
#         button = QLabel(f'{i}x{j}')
#         layout.addWidget(button)
#
# w = QWidget()
# w.setLayout(layout)
#
# mw = QScrollArea()
# mw.setWidget(w)
# mw.resize(200, 200)
# mw.show()
#
# app.exec()