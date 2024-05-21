from abc import abstractmethod, ABC
import subprocess, random, requests, json, wikipedia, pymorphy3
from geopy.geocoders import Nominatim
wikipedia.set_lang("ru")
ANALIZER = pymorphy3.MorphAnalyzer()


class Command(ABC):
    @abstractmethod
    def action(self, context, begin, end):
        pass


class Hello(Command):
    def action(self, context, begin, end):
        return "Привет, я голосовой помощник!"


class OpenBrows(Command):
    def action(self, context, begin, end):
        url = 'https://www.example.com'
        cmd = "python -m webbrowser -t " + url
        subprocess.Popen(cmd, shell=True)
        return "браузер открыт!"


class OpenVideo(Command):
    def action(self, context, begin, end):
        url = 'https://www.youtube.com/results?search_query=' + context.replace(' ', '+')
        cmd = "python -m webbrowser -t " + url
        subprocess.Popen(cmd, shell=True)
        return "видео открыто!"


class TellJoke(Command):
    def action(self, context, begin, end):
        url = "http://rzhunemogu.ru/RandJSON.aspx?CType=1"
        ans = requests.get(url)
        if ans.status_code != 200:
            return "Ошибка " + str(ans.status_code)
        a = " ".join(ans.text.split())
        anecdot = json.loads(a)
        return anecdot["content"]


class FlipCoin(Command):
    def action(self, context, begin, end):
        a = random.randint(0, 1)
        if a:
            return "На монетке выпала решка."
        return "На монетке выпал орёл."


class Wiki(Command):
    def action(self, context, begin, end):
        context = context[:begin] + context[end:]
        result = wikipedia.search(context)
        page = wikipedia.page(result[0])
        return page.summary


class Whether(Command):
    def action(self, context, begin, end):
        city = context[end:].split()[0]
        city = ANALIZER.parse(city)[0][2]

        loc = Nominatim(user_agent="GetLoc")
        getloc = loc.geocode(city)

        response = requests.get(
            f"https://api.openweathermap.org/data/2.5/find?lat={getloc.latitude}&lon={getloc.longitude}&appid={"04d0ad62774a5e1b91a2c642e3ad4ceb"}")

        if response.status_code != 200:
            return "Ошибка " + str(response.status_code)

        response_json = json.loads(response.text)
        info = response_json["list"][0]
        return f"Темпрература {info["main"]["temp"] - 273}, ощущается как {info["main"]["feels_like"] - 273}, скорость ветра - {info["wind"]["speed"]}"


commandsConfig = {
    "greetings": {
        "examples": ["привет", "здравствуйте"],
        "response": Hello()
    },
    "open_browser": {
        "examples": ["открой браузер", "запусти браузер"],
        "response": OpenBrows()
    },
    "open_video": {
        "examples": ["видео", "найди видос"],
        "response": OpenVideo()
    },
    "tell_joke": {
        "examples": ["анекдот", "расскажи анекдот"],
        "response": TellJoke()
    },
    "flip_coin": {
        "examples": ["монетку подбрось", "подбрось монетку"],
        "response": FlipCoin()
    },
    "wiki": {
        "examples": ["вики", "найди в википедии"],
        "response": Wiki()
    },
    "whether": {
        "examples": ["погода", "погода в"],
        "response": Whether()
    }
}
