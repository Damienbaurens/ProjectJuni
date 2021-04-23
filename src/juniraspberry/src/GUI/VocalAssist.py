#!/usr/bin/python3
import speech_recognition as sr
import pyttsx3 as ttx
import pywhatkit
import datetime

import time
from pixels import Pixels, pixels
from alexa_led_pattern import AlexaLedPattern
from google_home_led_pattern import GoogleHomeLedPattern

import rospy
from std_msgs.msg import Bool, Int16

awake = False
LedOn=False
pixels.pattern = GoogleHomeLedPattern(show=pixels.show)
pixels.off()

def ActivateLeds(LedOn):

    if LedOn==True:
        pixels.wakeup()
        time.sleep(3)
        pixels.think()
        time.sleep(3)
        pixels.speak()
        time.sleep(6)
        pixels.off()
        time.sleep(3)

    else :
        LedOn=False
        pixels.off()
        time.sleep(1)

def wakeUpPublish(status):
    pub = rospy.Publisher('wakeUpCall', Bool, queue_size =1)
    wake = Bool()
    wake.data = status
    rospy.loginfo(wake.data)
    pub.publish(wake)

def speakingPublish(status):
    pub = rospy.Publisher('speakCall', Bool, queue_size =1)
    speak = Bool()
    speak.data = status
    rospy.loginfo(speak.data)
    pub.publish(speak)

def infoListener():
    rospy.Subscriber("infoCall",Int16, infocallBack)

def infocallBack(infoData):
    rospy.loginfo(infoData.data)

    if (infoData.data == 1):
        parler('Aïe ! Mon oeil !')

    if (infoData.data == 2):
        parler('Jai mal !')

    if (infoData.data == 3):
        global awake
        awake=True
        lancer_assistant()

def parler(text):
    engine.say(text)
    engine.runAndWait()

def ecouter():
    try:
        with sr.Microphone() as source:
            print("parlez maintenant")
            voix=listener.listen(source)
            command = ""
            command=listener.recognize_google(voix,language='fr-FR')
            command.lower()
    except:
        pass
    return command

def lancer_assistant():
    global awake
    command=ecouter()
    if (awake==True):
        print(command)
        if 'heure' in command:
            ActivateLeds(True)
            speakingPublish(True)
            heure=datetime.datetime.now().strftime('%H:%M')
            parler('il est actuellement'+heure)
            speakingPublish(False)
            ActivateLeds(False)
            lancer_assistant()

        elif ('Bonjour') in command or ('bonjour')in command:
            ActivateLeds(True)
            speakingPublish(True)
            parler('Bonjour ! Comment ça va?')
            speakingPublish(False)
            ActivateLeds(False)
            lancer_assistant()

        elif 'listen' in command:
            ActivateLeds(True)
            speakingPublish(True)
            parler('Issèn est une école du groupe Junia')
            speakingPublish(False)
            ActivateLeds(False)
            lancer_assistant()

        elif 'david good enough' in command:
            ActivateLeds(True)
            speakingPublish(True)
            parler('Cé pas si mal ...')
            speakingPublish(False)
            ActivateLeds(False)
            lancer_assistant()

        elif 'au revoir' in command:
            ActivateLeds(True)
            speakingPublish(True)
            parler('Au revoir !')
            speakingPublish(False)
            wakeUpPublish(False)
            awake = False
            ActivateLeds(False)
            lancer_assistant()


        else:
            lancer_assistant()

    else:
        if 'Johnny' in command:
            ActivateLeds(True)
            wakeUpPublish(True)
            parler ('Salut tout le monde')
            awake = True
            ActivateLeds(False)
            lancer_assistant()
        else:
            lancer_assistant()

listener=sr.Recognizer()
engine=ttx.init()
voice=engine.getProperty('voices')
engine.setProperty('voice','french')
rospy.init_node("Microphone", anonymous = True)
infoListener()
wakeUpPublish(True)
wakeUpPublish(False)
lancer_assistant()