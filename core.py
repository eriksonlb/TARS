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
from sound import *
import json
from google_trans_new import google_translator

from helpers.data import assistent_data
from helpers import clean_dialogues
from features.news import get_news
from voice import reproduce
from frontal import get_response

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
        while True:
            try:
                with microphone as source:
                    speak_sound()
                    print("Fale agora...")
                    recognizer.adjust_for_ambient_noise(source, 1)
                    recognizer.dynamic_energy_threshold = True
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
        reproduce(text)

    def name(self):
        name_1_text = "Maravilha, vamos lá então. Qual será meu nome?"
        name_2_text = "Poderia repetir mais uma vez?"
        name_3_text = "Preciso ouvir mais uma vez para assimilar."
        validator = 0
        while True:
            print('name1:')
            s.speak(name_1_text) if validator == 0 else None
            name_1 = s.hear(self.recognizer, self.microphone)
            if name_1 != None:
                validator = 0
                while True:   
                    s.speak(name_1) if validator == 0 else None
                    print('\nname2:') 
                    self.speak(name_2_text) if validator == 0 else None                        
                    name_2 = self.hear(self.recognizer, self.microphone)
                    if name_2 != None:  
                        validator = 0
                        while True:
                            s.speak(name_2) if validator == 0 else None
                            print('\nname3')    
                            self.speak(name_3_text) if validator == 0 else None                
                            name_3 = self.hear(self.recognizer, self.microphone)
                            if name_3 != None:
                                s.speak(name_3) if validator == 0 else None
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
        with open("data/assistent_personality.json", "r", encoding="utf8") as json_file:
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
                

                # s.speak(introduce_text)
                # s.speak(information_text)
                s.speak(configuration_text)
                while True:
                    try:
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
                                        with open("data/assistent_personality.json", "w", encoding="utf8") as json_file:
                                            json.dump(all_names, json_file, ensure_ascii=False)
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
                    except:
                        s.speak("Falou algo?")    

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
    def get_time(self):
        today = date.today()
        now = datetime.now()
        fuso_horario = timezone('America/Sao_Paulo')
        return {'hoje': today, 'agora': now, 'fuso': fuso_horario}


    def get_weather(self):
        translator = google_translator()

        home = 'Campinas, São Paulo'
        owm = pyowm.OWM(OPENWEATHER)
        observation = owm.weather_at_place(home)
        detail = observation.get_weather()
        temp = detail.get_temperature('celsius')
        temp = int(temp['temp'])
        status = detail.get_detailed_status()
        status = translator.translate(status, lang_tgt="pt")

        return [temp, status]

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
            

    # Checks the first word in the command to determine if it's a search word
    def use_search_words(self, command):
        s.speak("Bom. achei isso aqui")
        webbrowser.open("https://www.google.com/search?q={}".format(command))

    # Analyzes the command
    def analyze(self, response_data, command):
        tag = response_data['tag']
        response = response_data['response']
        try:
            if tag == "facebook":
                s.speak(response)
                webbrowser.open("https://www.facebook.com")
            

            elif tag == "youtube":
                s.speak(response)
                webbrowser.open("https://www.youtube.com")

            elif tag == "apresentacao":
                s.speak(response)
                

            elif tag == "horas" or tag == "hoje" or tag == "ontem" or tag == "amanhã" or tag == "ano":
                mounths = {
                    "january": "janeiro",
                    "february": "fevereiro",
                    "march": "março",
                    "april": "abril",
                    "may": "maio",
                    "june": "junho",
                    "july": "julho",
                    "august": "agosto",
                    "september": "setembro",
                    "october": "outubro",
                    "november": "novembro",
                    "december": "dezembro"
                }
                days = {
                    "monday": "segunda",
                    "tuesday": "terça",
                    "wednesday": "quarta",
                    "thursday": "quinta",
                    "friday": "sexta",
                    "saturday": "sabádo",
                    "sunday": "domingo"
                }

                time_info = self.get_time()
                today = time_info['hoje']
                now = time_info['agora']
                if tag == "horas":
                    period = " da noite" if now.strftime("%p") == "PM" else ""
                    s.speak(response.format(now.strftime('%I'), now.strftime('%M'), period))

                elif tag == "hoje":
                    mounth = mounths[(today.strftime("%B")).lower()]
                    day = days[(today.strftime("%A")).lower()]
                    s.speak(response.format(day, int(today.strftime("%d")), mounth))
                elif tag == "ontem":
                    yesterday = today - timedelta(days=1)
                    mounth = mounths[(yesterday.strftime("%B")).lower()]
                    day = days[(yesterday.strftime("%A")).lower()]
                    s.speak(response.format(day, int(yesterday.strftime("%d")), mounth))

                elif tag == "amanhã":
                    tomorrow = today + timedelta(days=1)
                    mounth = mounths[(tomorrow.strftime("%B")).lower()]
                    day = days[(tomorrow.strftime("%A")).lower()]
                    s.speak(response.format(day, int(tomorrow.strftime("%d")), mounth))

                elif tag == "ano":
                    current_year = today.year
                    s.speak(response.format(current_year))

                    if current_year % 4 == 0:
                        days_in_current_year = 366

                    else:
                        days_in_current_year = 365
                    date_intent = today - timedelta(days=days_in_current_year)


            ###########################################################

            elif tag == "smart":
                s.speak("Você já comprou alguma dessas coisas pelo menos?")

            elif tag == "emoções":
                s.speak(response)
            
            elif tag == "clima":
                clima = self.get_weather()
                s.speak(response.format(clima[0], clima[1]))

            elif tag == "apresentacao":
                s.speak(response)

            elif "quanto é" in command:
                self.what_is_checker(command)

            elif tag == "notícias":
                news = get_news('campinas')
                s.speak(response)
                for n in news:
                    sleep(1)
                    s.speak(n)
            elif tag == "despedida":
                s.speak(response)
                end_sound()
                sys.exit()
                
            elif SEARCH_WORDS.get(command.split(' ')[0]) == command.split(' ')[0]:
                self.use_search_words(command)

            elif tag == "não entendeu" and "sair" not in command:
                s.speak(response)

            elif tag == "computador":
                s.speak(response)
                com = 'shutdown -s'
                os.system(com)

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
                    print(f"\n\n\nDiga '{name}' para iniciar")                    
                    recognizer.dynamic_energy_threshold = 2900
                    audio = recognizer.listen(source, timeout=10.0)
                    response = recognizer.recognize_google(audio, language='pt')
                    for name in name_list:
                        if name in response.lower():
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


    def dialogue(self):
        dial = True
        while dial:
            previous_response = ""
            command = s.hear(recognizer, microphone)
            # command = 'que dia foi ontem'
            # answer = conversation(command)  
            answer = get_response(command)
            s.analyze(answer, command)
            previous_response = command
            # asking = [
            #     'precisa de mais alguma coisa?',
            #     'certo, quê mais?',
            #     'deseja mais algo?',
            #     'mais alguma coisa?'

            # ]
            answer = [
                'certo. qualquer coisa só chamar',
                'precisando estou á disposição',
                'qualquer coisa, é só falar',
                'Tudo bem. estou sempre a disposição'
            ]
            if 'sair' in command:
                s.speak(random.choice(answer))
                dial = False
                break

clean_dialogues
s = Shane()
weather = s.get_weather()
ipdb.set_trace()
# start_sound()
# s.start_conversation_log()
# assistent_names = s.introduce()['names']
# while True:
#     response = s.listen(recognizer, microphone)
#     s.dialogue()
# clean_dialogues