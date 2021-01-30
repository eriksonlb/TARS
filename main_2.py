import speech_recognition as sr
import pyttsx3
import webbrowser
from datetime import date, timedelta, datetime
from pytz import timezone
import serial 
import pyowm 
from Keys import OPENWEATHER 
import operator  
import random  
import os 
from time import sleep
import ipdb

recognizer = sr.Recognizer()
microphone = sr.Microphone()

engine = pyttsx3.init()
engine.setProperty('volume', 3.0)

WAKE = "cara"

CONVERSATION_LOG = "Conversation Log.txt"

SEARCH_WORDS = {"quem": "quem", "qual": "qual", "o que": "o que", "quando": "quando", "onde": "onde", "por que": "por que", "porque": "porque", "como": "como"}


class Shane:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def hear(self, recognizer, microphone, response):
        """Ouve o comando após despertar o assistente"""
        try:
            with microphone as source:
                print("Aguardando comando.")
                recognizer.adjust_for_ambient_noise(source)
                recognizer.dynamic_energy_threshold = 3000
                audio = recognizer.listen(source, timeout=45.0)
                command = recognizer.recognize_google(audio)
                s.remember(command)
                return command.lower()
        except sr.WaitTimeoutError:
            pass
        except sr.UnknownValueError:
            pass
        except sr.RequestError:
            print("Erro de internet")

    def speak(self, text):
        """Falar um texto com o usuario"""
        engine.say(text)
        engine.runAndWait()

    def open_things(self, command):
        """Abrir links no navegador"""
        if command == "abrir youtube":
            s.speak("OK. Alexa abra o YouTube.")
            webbrowser.open("https://www.youtube.com")
            pass

        elif command == "abrir facebook":
            s.speak("Só um segundinho")
            webbrowser.open("https://www.facebook.com")
            pass

        else:
            s.speak("Não aprendi a fazer isso ainda")
            pass

    # Used to track the date of the conversation, may need to add the time in the future
    def start_conversation_log(self):
        today = str(date.today())
        today = today
        with open(CONVERSATION_LOG, "a") as f:
            f.write("Conversation started on: " + today + "\n")

    # Writes each command from the user to the conversation log
    def remember(self, command):
        with open(CONVERSATION_LOG, "a") as f:
            f.write("User: " + command + "\n")

    # Used to answer time/date questions
    def understand_time(self, command):
        today = date.today()
        now = datetime.now()
        fuso_horario = timezone('America/Sao_Paulo')

        if "hoje" in command:
            s.speak("Hoje é " + today.strftime("%B") + " " + today.strftime("%d") + ", " + today.strftime("%Y"))

        elif command == "que horas são":
            period = " da noite" if now.strftime("%p") == "PM" else ""
            s.speak(f"Agora são {now.strftime('%I')} horas. E {now.strftime('%M')} minutos {period}")

        elif "ontem" in command:
            date_intent = today - timedelta(days=1)
            return date_intent

        elif "ano passado" in command:
            current_year = today.year

            if current_year % 4 == 0:
                days_in_current_year = 366

            else:
                days_in_current_year = 365
            date_intent = today - timedelta(days=days_in_current_year)
            return date_intent

        elif "ultima semana" in command:
            date_intent = today - timedelta(days=7)
            return date_intent
        else:
            pass

    def get_weather(self, command):
        home = 'Campinas, São Paulo'
        owm = pyowm.OWM(OPENWEATHER)
        mgr = owm.weather_manager()

        if "agora" in command:
            observation = mgr.weather_at_place(home)
            w = observation.weather
            temp = w.temperature('celsius')
            status = w.detailed_status
            s.speak("Agora está com " + str(int(temp['temp'])) + " graus e " + status)

        else:
            print("Não estou programada para isso.")

    # If we're doing math, this will return the operand to do math with
    def get_operator(self, op):
        return {
            '+': operator.add,
            '-': operator.sub,
            'x': operator.mul,
            '/': operator.__truediv__,
            'Mod': operator.mod,
            'mod': operator.mod,
        }[op]

    def do_math(self, li):
        op = self.get_operator(li[1])
        int1, int2 = int(li[0]), int(li[2])
        result = op(int1, int2)
        s.speak(str(int1) + " " + li[1] + " " + str(int2) + " é igual a " + str(result))

    def what_is_checker(self, command):
        number_list = {"1", "2", "3", "4", "5", "6", "7", "8", "9"}
        li = list(command.split(" "))
        del li[0:2]

        if li[0] in number_list:
            self.do_math(li)

        elif "que dia é hoje" in command:
            self.understand_time(command)

        else:
            self.use_search_words(command)

    # Checks the first word in the command to determine if it's a search word
    def use_search_words(self, command):
        s.speak("Bom. achei isso aqui")
        webbrowser.open("https://www.google.com/search?q={}".format(command))

    # Analyzes the command
    def analyze(self, command):
        try:
            if len(command) > 0:
                print(f"Você disse: {command}")
            if command.startswith('abrir'):
                self.open_things(command)

            elif "se apresente" in command:
                s.speak("Eu sou R2. Sou uma inteligencia artificial programada pra destru")
                s.speak("Quero dizer, para ajudar.")
                

            elif "horas são" in command:
                self.understand_time(command)

            elif "ligue o" in command or "ligue a" in command or "acenda as" in command:
                s.speak("Você já comprou alguma dessas coisas pelo menos?")

            elif "como você está" in command:
                current_feelings = ["Estou bem", "Vou bem. Obrigada.", "Na verdade um pouco entediada, mas bem."]
                greeting = random.choice(current_feelings)
                s.speak(greeting)
            elif "clima" in command:
                self.get_weather(command)

            elif "quanto é" in command or "que dia é" in command:
                self.what_is_checker(command)

            # Keep this at the end
            elif SEARCH_WORDS.get(command.split(' ')[0]) == command.split(' ')[0]:
                self.use_search_words(command)

            else:
                s.speak("Eu não sou tão esperta assim ainda")

        except TypeError:
            print("Warning: Erro de TypeError")
            pass
        except AttributeError:
            print("Warning:Erro de Attribute Error.")
            pass

    def listen(self, recognizer, microphone):
        while True:
            try:
                with microphone as source:
                    print("Diga ‘R2’ para iniciar")
                    recognizer.adjust_for_ambient_noise(source)
                    recognizer.dynamic_energy_threshold = 3000
                    audio = recognizer.listen(source, timeout=100.0)
                    response = recognizer.recognize_google(audio)

                    if response == WAKE:
                        greetings = ["Olá. Como posso te ajudar?", "Pois não", "ás suas ordens"]
                        greeting = random.choice(greetings)
                        s.speak("iiiii aiiiii caaaaaaaraaaa")
                        return response.lower()

                    else:
                        pass
            except sr.WaitTimeoutError:
                pass
            except sr.UnknownValueError:
                pass
            except sr.RequestError:
                print("Erro de conexão.")


s = Shane()
s.start_conversation_log()
previous_response = ""
while True:
    response = s.listen(recognizer, microphone)
    command = s.hear(recognizer, microphone, response)

    if command == previous_response:
        s.speak("Você já disse isso, se tem certeza repita por favor.")
        previous_command = ""
        response = s.listen(recognizer, microphone)
        command = s.hear(recognizer, microphone, response)
    s.analyze(command)
    previous_response = command