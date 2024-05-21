'''
    файл с кастомными командами
'''
from commands import Command


class HelloWorld(Command):
    '''
        класс команды должен наследоваться от класса Command
        действие исполняемое по команде должно содержаться в методе action
        context - текст, введённый пользователем
        begin, end - начало и конец распознанной команды
    '''
    def action(self, context, begin, end):
        return "Hello, world!"


'''
    hello_world - програмное название команды(может быть любым)
    по ключу examples хранится массив команд по которым будет вызываться action у класса под ключём response
'''
customCommandsConfig = {
    "hello_world": {
        "examples": ["hello"],
        "response": HelloWorld()
    }
}