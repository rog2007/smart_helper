import threading

import functions
import qclasses


def listen_sound():
    for text in functions.EARS.listen():
        print(functions.EARS.canHear, text, "<-услышал")
        if functions.EARS.canHear:
            functions.EARS.set_can_hear(False)
            qclasses.signalHub.earsSignal.emit(text)


def listen_text(text):
    print(text)
    if functions.COMMANDER.check_command(text):
        answer = functions.COMMANDER.execute_current_command()
        functions.MOUTH.add_to_speaking_queue(answer)
        qclasses.signalHub.answer.emit(answer)
        return
    functions.SOCK.put(text)
    answer = functions.SOCK.get()
    punctuationMarks = ['.', ',', '!', '?', ':', ';', '-']
    lastPart = ""
    allPhrase = ""
    while "!!!end_phrase!!!" not in answer:
        for i in answer:
            allPhrase += i
            qclasses.signalHub.answer.emit(allPhrase)
            qclasses.signalHub.newMessage.emit(False)
            if i not in punctuationMarks:
                lastPart += i
            else:
                functions.MOUTH.add_to_speaking_queue(lastPart)
                lastPart = ""
        answer = functions.SOCK.get()
    qclasses.signalHub.newMessage.emit(True)
    functions.EARS.set_can_hear(True)


def start_listen(text):
    thread = threading.Thread(target=listen_text, args=(text,), daemon=True)
    thread.start()


qclasses.signalHub.question.connect(start_listen)


def load():
    sender = qclasses.signalHub
    sender.loadSignal.emit(14)
    print("16 emited")
    for loadingElement in functions.initialization():
        print(loadingElement, "<-loading element")
        if loadingElement == 0:
            sender.loadSignal.emit(28)
        elif loadingElement == 1:
            sender.loadSignal.emit(42)
        elif loadingElement == 2:
            sender.loadSignal.emit(56)
        elif loadingElement == 3:
            thread = threading.Thread(target=listen_sound, daemon=True)
            thread.start()
            sender.loadSignal.emit(70)
        elif loadingElement == 4:
            thread = threading.Thread(target=functions.MOUTH.start_speaking_processing, daemon=True)
            thread.start()
            sender.loadSignal.emit(84)
        elif loadingElement == 5:
            sender.loadSignal.emit(100)
            break

    functions.MOUTH.add_to_speaking_queue('Слушаю вас...')


if __name__ == "__main__":
    main()
