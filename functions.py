import json, pyaudio, pyttsx3, socket, pymorphy3, commands, os, subprocess, custom_commands

from vosk import Model, KaldiRecognizer
from rapidfuzz import fuzz

MORPH = None
SOCK = None
EARS = None
MOUTH = None
COMMANDER = None
LANG_MODEL = None


class MorphyManager:
    def __init__(self):
        self.analyzer = pymorphy3.MorphAnalyzer()

    def normalize_text(self, text):
        text = list(text.split())
        del_morph = [] #["PREP", "CONJ", "CONJ", "INTJ"]
        ans = ""
        for word in text:
            word_info = self.analyzer.parse(word)[0]
            if word_info.tag.POS not in del_morph:
                ans += ("" if len(ans) == 0 else " ") + word_info.word
        return ans


class SocketManager:
    def __init__(self, curSock):
        self.connection = socket.socket()
        self.connection.connect(("localhost", curSock))

    def put(self, text):
        self.connection.send(text.encode())

    def get(self):
        return self.connection.recv(1024).decode()

    def close(self):
        self.connection.close()


class EarsManager:
    def __init__(self):
        self.model = Model("vosk-model-ru-0.42")
        self.rec = KaldiRecognizer(self.model, 16000)
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
        self.stream.start_stream()
        self.canHear = False

    def listen(self):
        while True:
            if self.canHear:
                data = self.stream.read(4000, exception_on_overflow=False)
                if (self.rec.AcceptWaveform(data)) and (len(data) > 0):
                    answer = json.loads(self.rec.Result())
                    if answer['text']:
                        yield answer['text']

    def set_can_hear(self, value):
        self.canHear = False


class MouthManager:
    def __init__(self):
        self.tts = pyttsx3.init()
        voices = self.tts.getProperty("voices")
        self.tts.setProperty("voice", "ru")
        self.tts.setProperty("rate", 100)
        self.queue = []
        # for i in voices:
        #     if i.name == "russian_test":
        #         self.tts.setProperty("voice", i.id)

    def start_speaking_processing(self):
        while True:
            #print(len(self.queue))
            if len(self.queue):
                self.tts.say(self.queue[0])
                self.tts.runAndWait()
                self.queue.pop(0)

    def add_to_speaking_queue(self, text):
        self.queue.append(text)



class CommandManager:
    def __init__(self):
        self.commands = commands.commandsConfig
        for cmd in custom_commands.customCommandsConfig.keys():
            self.commands[cmd] = custom_commands.customCommandsConfig[cmd]
        self.currentCommand = None
        self.commandContext = ""
        self.beginCommand = 0
        self.endCommand = 0

    def check_command(self, text):
        mx = 0
        mx_cmd = ""
        begin = 0
        end = 0
        norm_text = MORPH.normalize_text(text)
        for cmd in self.commands.keys():
            for example in self.commands[cmd]["examples"]:
                lv = lev_check(norm_text, example)
                if lv[0] > mx:
                    mx = lv[0]
                    begin = lv[1]
                    end = lv[1] + len(example)
                    mx_cmd = cmd

        self.currentCommand = mx_cmd
        self.commandContext = MORPH.normalize_text(text)
        self.beginCommand = begin
        self.endCommand = end
        if mx >= 0.75:
            return True
        return False

    def execute_current_command(self):
        commandAnswer = self.commands[self.currentCommand]["response"].action(self.commandContext, self.beginCommand, self.endCommand)
        return commandAnswer


def initialization():
    global MORPH, MOUTH, EARS, SOCK, COMMANDER, LANG_MODEL
    localSock = socket.socket()
    curSock = 1488
    for trySock in range(1488, 1588):
        try:
            curSock = trySock
            localSock.bind(("", trySock))
            break
        except Exception:
            pass
    print("funk binded")
    localSock.listen(1)
    print("funk listening")
    LANG_MODEL = subprocess.Popen("/home/dima/PycharmProjects/pythonProject1/venv/bin/python /home/dima/PycharmProjects/pythonProject1/lang_model.py -s " + str(curSock) + "&", shell=True)
    conn, addr = localSock.accept()
    user_message = conn.recv(1024).decode()
    while not user_message:
        user_message = conn.recv(1024).decode()
    localSock.close()
    print("functions is geted")
    print(user_message)
    yield 0

    MORPH = MorphyManager()
    yield 1
    SOCK = SocketManager(int(user_message))
    yield 2
    EARS = EarsManager()
    yield 3
    MOUTH = MouthManager()
    yield 4
    COMMANDER = CommandManager()
    yield 5


def lev_check(text, target):
    """Функция фналогична косинусному сходству только без векторизации"""
    score = 0
    pos = 0
    #assert len(text) > len(target)
    for i in range(len(text) - len(target) + 1):
        # делим метрику на 100, т.к. данная метрика находится в пределах от 0 до 100
        current_score = fuzz.ratio(text[i: i + len(target)], target) / 100
        if current_score > score:
            score = current_score
            pos = i
    return (score, pos)


def shut_down():
    LANG_MODEL.kill()
