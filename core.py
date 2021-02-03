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
import sys
from sound import speak_sound
from brain import conversation
import json

from helpers.data import assistent_data

recognizer = sr.Recognizer()
microphone = sr.Microphone()

engine = pyttsx3.init()
engine.setProperty('volume', 3.0)


CONVERSATION_LOG = "Conversation Log.txt"

SEARCH_WORDS = {"quem": "quem", "qual": "qual", "o que": "o que", "quando": "quando", "onde": "onde", "por que": "por que", "porque": "porque", "como": "como"}


class Shane:
    all_names = []
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def hear(self, recognizer, microphone):
        """Ouve o comando após despertar o assistente"""
        try:
            with microphone as source:
                speak_sound()
                print("Fale agora...")
                recognizer.adjust_for_ambient_noise(source, 1)
                recognizer.dynamic_energy_threshold = 3000
                audio = recognizer.listen(source, timeout=45.0)
                command = recognizer.recognize_google(audio, language='pt')
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

    def name(self):
        name_1_text = "Maravilha, vamos lá então. Qual será meu nome?"
        name_2_text = "Poderia repetir mais uma vez?"
        name_3_text = "Preciso ouvir mais uma vez para assimilar."
        validator = 0
        while True:
            print('name1:')
            self.speak(name_1_text) if validator == 0 else None
            name_1 = s.hear(self.recognizer, self.microphone)
            if name_1 != None:
                validator = 0
                while True:   
                    print(name_1)
                    print('\nname2:') 
                    self.speak(name_2_text) if validator == 0 else None                        
                    name_2 = self.hear(self.recognizer, self.microphone)
                    if name_2 != None:  
                        validator = 0
                        while True:
                            print(name_2)
                            print('\nname3')    
                            self.speak(name_3_text) if validator == 0 else None                
                            name_3 = self.hear(self.recognizer, self.microphone)
                            if name_3 != None:
                                print(name_3)
                                break
                            else:
                                self.speak("Entendi não. Poderia repetir por favor?")
                                validator = 1
                        break
                    else:
                        self.speak("Não deu pra entender, repete aí")
                        validator = 1
                names = {
                    "names": {
                        "name_1": name_1,
                        "name_2": name_2,
                        "name_3": name_3
                    }
                }
                return [name_1, names]
                break
            else:
                self.speak("Não entendi. Poderia repetir?")
                validator = 1

    def introduce(self):
        assistent_data()
        with open("data/assistent_personality.json") as json_file:
            data = json.load(json_file)
            if 'names' in data:
                return data
            else:
                introduce_text = 'Olá, eu sou sua nova assistente pessoal. É um prazer te conhecer. Espero ser bem útil'
                information_text = """
                Lembrando. que haverá um sinal sonoro indicando que estou te ouvindo. assim a gente evita algum mal entendido. ok?
                Antes de mais nada. eu preciso de um nome.
                Eu não sou do tipo que fica escutando conversas alheias.
                Então. quando precisar de mim. basta me chamar pelo nome.
                Mas para isso. preciso saber como prefere me chamar. 
                """
                configuration_text = "Podemos fazer isso agora? Ou prefere fazer uma outra hora?"
                

                self.speak(introduce_text)
                self.speak(information_text)
                self.speak(configuration_text)
                while True:
                    configuration = s.hear(self.recognizer, self.microphone)
                    if "não" in configuration or "depois" in configuration or "hora" in configuration:
                        self.speak("Tudo bem, até mais então.")
                        sys.exit()

                    elif "sim" in configuration or "claro" in configuration or "agora" in configuration:
                        assistent = self.name()                    
                        assistent_name =  assistent[0] 
                        all_names = assistent[1]                  
                        confirmation_text = f"Acho que entendi. meu nome então será. {assistent_name}. É isso mesmo?"
                        while True:
                            self.speak(confirmation_text)
                            confirmation =s.hear(self.recognizer, self.microphone)
                            if confirmation != None:
                                if "sim" in confirmation or "isso mesmo" in confirmation:
                                    self.speak(f"Tudo certo, já pode aproveitar minhas funcionalidades, lembre apeenas de me falar {assistent_name} quando precisar.")
                                    with open("data/assistent_personality.json", "w") as json_file:
                                        json.dump(all_names, json_file)
                                        json_file.close()
                                    return all_names
                                elif "não" in confirmation or "errado" in confirmation:
                                    self.speak("Bom, parece que precisamos refazer todo o proccesso.")
                                    self.speak("Deseja fazer agora ou depois?")
                                    check = s.hear(self.recognizer, self.microphone)
                                    if "depois" in check:
                                        sys.exit()
                                    elif "agora" in check:
                                        break
                                    else:
                                        self.speak("Repete aí")
                                break
                            else:
                                self.speak("Não entendir, repete vai.")


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
    def analyze(self, command, trated_response):
        try:
            if len(command) > 0:
                print(f"Falou nada")
            if command.startswith('abrir'):
                self.open_things(command)

            elif "se apresente" in command:
                s.speak("Eu sou Wake. Sou uma inteligencia artificial programada pra destru")
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

            elif "desligar" in command or "encerrar atividades" in command:
                s.speak("Falou, falou. Até mais")
                sys.exit()

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
        name_list = [*assistent_names.values()]
        while True:
            try:
                with microphone as source:
                    name = assistent_names['name_1']
                    print(f"Diga '{name}' para iniciar")
                    recognizer.dynamic_energy_threshold = 1000
                    audio = recognizer.listen(source, timeout=45.0)
                    response = recognizer.recognize_google(audio, language='pt')

                    if response in name_list:
                        greetings = ["Olá. Como posso te ajudar?", "Pois não", "ás suas ordens"]
                        greeting = random.choice(greetings)
                        s.speak(greeting)
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
assistent_names = s.introduce()['names']
while True:
    response = s.listen(recognizer, microphone)
    command = s.hear(recognizer, microphone)

    if command == previous_response:
        s.speak("Você já disse isso, se tem certeza repita por favor.")
        previous_command = ""
        s.listen(recognizer, microphone, assistent_names)
        command = s.hear(recognizer, microphone)
    answer = conversation(command)  
    s.analyze(command, answer)
    previous_response = command