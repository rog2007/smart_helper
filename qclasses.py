from PyQt6.QtCore import QSize, QTimer, QObject, pyqtSignal
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6 import uic

import functions


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
    label.setObjectName("label")
    layout = QHBoxLayout()
    spacer = QSpacerItem(1, 1, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
    layout.addItem(spacer)
    layout.addWidget(label)
    return [layout, label]


def format_bot_message(text):
    label = QLabel(text)
    label.setStyleSheet(userMessageStyle)
    label.setAlignment(Qt.AlignmentFlag.AlignLeft)
    label.setWordWrap(True)
    label.setScaledContents(True)
    label.adjustSize()
    label.setObjectName("label")
    layout = QHBoxLayout()
    spacer = QSpacerItem(1, 1, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
    layout.addWidget(label)
    layout.addItem(spacer)
    return [layout, label]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("mainwindow.ui", self)

        self.progress.setMinimum(0)
        self.progress.setMaximum(100)
        self.progressValue = 0
        self.progressTarget = 0
        self.newMessage = True
        self.lastBotMessage = None

        self.mysign = signalHub
        self.mysign.loadSignal.connect(self.set_progress_target)
        self.mysign.earsSignal.connect(self.ears_heard)
        self.mysign.newMessage.connect(self.set_new_message)

        self.textInput.returnPressed.connect(self.request_processing)

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
        self.textInput.setText("")
        self.verticalLayout_3.addLayout(format_user_message(text)[0])
        signalHub.question.emit(text)

    def set_text_output(self, text):
        #print("!!дошло", a)
        if self.newMessage:
            self.lastBotMessage = format_bot_message(text)
            self.verticalLayout_3.addLayout(self.lastBotMessage[0])
        else:
            self.lastBotMessage[1].setText(text)

    def closeEvent(self, event):
        functions.SOCK.put("!!!close!!!")
        functions.SOCK.close()
        functions.shut_down()
        super().closeEvent(event)

    # def eventFilter(self, widget, event):
    #     return super().eventFilter(widget, event)

    def ears_heard(self, text):
        self.textInput.setText(text)
        self.request_processing()

    def set_new_message(self, newMessage):
        self.newMessage = newMessage


class mySignalHub(QObject):
    loadSignal = pyqtSignal(int)
    question = pyqtSignal(str)
    answer = pyqtSignal(str)
    earsSignal = pyqtSignal(str)
    newMessage = pyqtSignal(bool)


signalHub = mySignalHub()
