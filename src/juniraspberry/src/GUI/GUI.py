#!/usr/bin/python3
#la ligne 1 sert à indiquer l'emplacement de l'interpréteur qu'on utilise.
# Attention : Utilisez bien Python3, la librairie PIL n'est plus supportée par Python 2.
# Importation --------------------------------------------------------------------------------------------------
#GUI
from tkinter import *
#Ouverture et traitement d'image simple
from PIL import Image, ImageTk
#chemins de fichiers
from pathlib import Path
#librairies Ros
import rospy
from std_msgs.msg import Int16MultiArray, Bool, String, Int16
#----------------------------------------------------------------------------------------------------------------
#Variables globales qui rendent compte de l'état du robot
awake = False   #awake= False : robot en phase de veille (les 3 points)
busy = True     #busy : état d'occupation du robot
holdOn = False  #click maintenu
order = False

#blinkLoop : Lorsque l'on clique sur un oeil ça crée un 2e Blink en parallèle donc on en garde un seul
blinkLoop=0

def wakeUpAnimation1():
    global awake
    global busy
    if awake == False :
        busy=True
        awake=True
        swapFace(IrisL, Step1L, IrisR, Step1R, IrisM, Step1M)
        root.after(500, wakeUpAnimation2)
    else :
        pass
def wakeUpAnimation2():
    swapFace(Step1L, Step2L, Step1R, Step2R, Step1M, Step2M)
    root.after(500, wakeUpAnimation3)
def wakeUpAnimation3():
    swapFace(Step2L, Step3L, Step2R, Step3R, Step2M, normalMouth)
    root.after(500, wakeUpAnimation4)
def wakeUpAnimation4():
    swapFace(Step3L, Step4L, Step3R, Step4R, normalMouth, normalMouth)
    root.after(500, wakeUpAnimation5)
def wakeUpAnimation5():
    swapFace(Step4L, Step5L, Step4R, Step5R, normalMouth, normalMouth)
    root.after(500, wakeUpAnimation6)
def wakeUpAnimation6():
    swapFace(Step5L, openEyeL, Step5R, openEyeR, normalMouth, normalMouth)
    root.after(500, wakeUpAnimation7)
def wakeUpAnimation7():
    show(Step6L)
    show(Step6R)
    root.after(500, wakeUpAnimation8)
def wakeUpAnimation8():
    swap(Step6L, IrisL)
    swap(Step6R, IrisR)
    root.after(500, sayHello)

def sayHello():
    global busy
    busy=True
    hide(IrisL)
    hide(IrisR)
    swapFace(openEyeL, funnyEyeL, openEyeR, funnyEyeR, normalMouth, happyMouth)
    root.after(2000, waitingState)

def blink():
    global busy
    global awake
    global blinkLoop
    if (awake==True) and (busy==False):
        busy=True
        awake = True
        blinkLoop=0
        hide(IrisL)
        hide(IrisR)
        swapFace(openEyeL, closedEyeL, openEyeR, closedEyeR, normalMouth, normalMouth)
        root.after(200, waitingState)

#All frames back to normal face
def waitingState():
    global busy
    global awake
    global blinkLoop
    busy=False
    awake=True
    blinkLoop+=1
    for i in allAssets:
        hide(i)
    show(IrisL)
    show(IrisR)
    show(openEyeL)
    show(openEyeR)
    show(normalMouth)
    if (blinkLoop==1):
        root.after(8000, blink)

def sleepAnimation1():
    global awake
    global busy
    if awake == True:
        busy=True
        awake=False
        swap(IrisL, Step6L)
        swap(IrisR, Step6R)
        hide(happyMouth)
        root.after(500, sleepAnimation2)
    else:
        pass
def sleepAnimation2():
    hide(Step6L)
    hide(Step6R)
    root.after(500, sleepAnimation3)
def sleepAnimation3():
    swapFace(openEyeL, Step5L, openEyeR, Step5R, normalMouth, normalMouth)
    root.after(500, sleepAnimation4)
def sleepAnimation4():
    swapFace(Step5L, Step4L, Step5R, Step4R, normalMouth, normalMouth)
    root.after(500, sleepAnimation5)
def sleepAnimation5():
    swapFace(Step4L, Step3L, Step4R, Step3R, normalMouth, normalMouth)
    root.after(500, sleepAnimation6)
def sleepAnimation6():
    swapFace(Step3L, Step2L, Step3R, Step2R, normalMouth, Step2M)
    root.after(500, sleepAnimation7)
def sleepAnimation7():
    swapFace(Step2L, Step1L, Step2R, Step1R, Step2M, Step1M)
    root.after(500, sleepAnimation8)
def sleepAnimation8():
    swapFace(Step1L, IrisL, Step1R, IrisR, Step1M, IrisM)

def hide(frame):
    face.itemconfig(frame, state=HIDDEN)

def show(frame):
    face.itemconfig(frame, state=NORMAL)

def swap(frame1, frame2):

    hide(frame1)
    show(frame2)

def swapFace(EyeL1, EyeL2, EyeR1, EyeR2, Mouth1, Mouth2):

    swap(EyeL1, EyeL2)
    swap(EyeR1, EyeR2)
    swap(Mouth1, Mouth2)

def hurtEyeLeft():
    global awake
    global busy
    if (awake == True) and (busy==False):
        busy=True
        awake=True
        hide(IrisL)
        hide(IrisR)
        swapFace(openEyeL, deadEyeL, openEyeR, closedEyeR, normalMouth, weirdMouth)
        infoPublish(1)
        root.after(1000, waitingState)
    else:
        pass

def hurtEyeRight():
    global awake
    global busy
    if (awake == True) and (busy==False):
        busy=True
        awake=True
        hide(IrisL)
        hide(IrisR)
        swapFace(openEyeL, closedEyeL, openEyeR, deadEyeR, normalMouth, weirdMouth)
        infoPublish(2)
        root.after(1000, waitingState)
    else:
        pass

class MouseControl:
    def __init__(self, canvas):
        self.canvas = canvas
        self.holdOn = 0
        self.rate = rospy.Rate(10)
        self.canvas.bind('<Button-1>', self.TestClickedEye)
        self.canvas.bind('<ButtonRelease-1>', self.button_released)
        self.canvas.bind('<B1-Motion>', self.moved)

    def button_released(self, event):
        x, y = event.x, event.y
        self.holdOn = 0
        pos = Int16MultiArray()
        pub = rospy.Publisher('touchScreenPos', Int16MultiArray, queue_size =1)
        pos.data = [x,y,self.holdOn]
        rospy.loginfo(pos.data)
        pub.publish(pos)

        global awake
        if awake == False:
            infoPublish(3)
            root.after(100,wakeUpAnimation1)

        self.rate.sleep()

    def touchScreenEventHandler(self, event):
        x, y = event.x, event.y
        self.holdOn = 1
        pos = Int16MultiArray()
        pub = rospy.Publisher('touchScreenPos', Int16MultiArray, queue_size =1)
        pos.data = [x,y,self.holdOn]
        rospy.loginfo(pos.data)
        pub.publish(pos)
        self.rate.sleep()

    def TestClickedEye(self, event):
        if (105<=event.x<=295) and (25<=event.y<=215):
            #print('single mouse click event on LeftEye at ({}, {})'.format(event.x, event.y))
            root.after(100, hurtEyeLeft)
        elif (505<=event.x<=695) and (25<=event.y<=215):
            #print('single mouse click event on RightEye at ({}, {})'.format(event.x, event.y))
            root.after(100, hurtEyeRight)

        self.touchScreenEventHandler(event)



    def moved(self, event):
        self.TestClickedEye(event)
        #print('mouse position is at ({:03}. {:03})'.format(event.x, event.y), end='\r')
        return


def wakeUpcallback(wakeData):
    rospy.loginfo(wakeData.data)
    global awake

    if (wakeData.data == True)and(awake==False) :
        root.after(100,wakeUpAnimation1)

    if (wakeData.data == False)and(awake==True):
        root.after(100,sleepAnimation1)

def speakcallback(speakData):
    rospy.loginfo(speakData.data)
    global order
    order = speakData.data
    if order == True:
        root.after(100,speakAnimation1)

def speakAnimation1():
    swap(normalMouth, happyMouth)
    root.after(200, speakcallback)
def speakAnimation2():
    global order
    if order == False:
        root.after(100,waitingState)
    swap(happyMouth, normalMouth)
    root.after(200, speakAnimation1)


def wakeUpListener():
    rospy.Subscriber("wakeUpCall",Bool, wakeUpcallback)

def speakingListener():
    rospy.Subscriber("speakCall",Bool, speakcallback)

def infoPublish(status):
    pub = rospy.Publisher('infoCall', Int16, queue_size =1)
    info = Int16()
    info.data = status
    rospy.loginfo(info.data)
    pub.publish(info)

#Setup Canvas
root = Tk()
root.attributes('-zoomed', True)
root['bg'] = 'black'
face = Canvas(width = 800, height = 480, bg = 'black')
rospy.init_node("TouchScreen", anonymous = True)
wakeUpListener()
speakingListener()
mouse = MouseControl(face)
face.place(x=0, y=0)

#Assets for Juni's opening
Step1=ImageTk.PhotoImage(Image.open('/home/pi/Juni/ProjectJuni-Tkinter/src/juniraspberry/src/GUI/Elements_Interface/Robot_opening/assets/Step1.png'))
Step2=ImageTk.PhotoImage(Image.open('/home/pi/Juni/ProjectJuni-Tkinter/src/juniraspberry/src/GUI/Elements_Interface/Robot_opening/assets/Step2.png'))
Step3=ImageTk.PhotoImage(Image.open('/home/pi/Juni/ProjectJuni-Tkinter/src/juniraspberry/src/GUI/Elements_Interface/Robot_opening/assets/Step3.png'))
Step4=ImageTk.PhotoImage(Image.open('/home/pi/Juni/ProjectJuni-Tkinter/src/juniraspberry/src/GUI/Elements_Interface/Robot_opening/assets/Step4.png'))
Step5=ImageTk.PhotoImage(Image.open('/home/pi/Juni/ProjectJuni-Tkinter/src/juniraspberry/src/GUI/Elements_Interface/Robot_opening/assets/Step5.png'))
Step6=ImageTk.PhotoImage(Image.open('/home/pi/Juni/ProjectJuni-Tkinter/src/juniraspberry/src/GUI/Elements_Interface/Robot_opening/assets/Step6.png'))

Step1L = face.create_image(200, 120, image = Step1, state = HIDDEN)
Step2L = face.create_image(200, 120, image = Step2, state = HIDDEN)
Step3L = face.create_image(200, 120, image = Step3, state = HIDDEN)
Step4L = face.create_image(200, 120, image = Step4, state = HIDDEN)
Step5L = face.create_image(200, 120, image = Step5, state = HIDDEN)
Step6L = face.create_image(200, 120, image = Step6, state = HIDDEN)

Step1R = face.create_image(600, 120, image = Step1, state = HIDDEN)
Step2R = face.create_image(600, 120, image = Step2, state = HIDDEN)
Step3R = face.create_image(600, 120, image = Step3, state = HIDDEN)
Step4R = face.create_image(600, 120, image = Step4, state = HIDDEN)
Step5R = face.create_image(600, 120, image = Step5, state = HIDDEN)
Step6R = face.create_image(600, 120, image = Step6, state = HIDDEN)

Step1M = face.create_image(400, 360, image = Step1, state = HIDDEN)
Step2M = face.create_image(400, 360, image = Step2, state = HIDDEN)

#Useful assets for Juni's face

Iris=ImageTk.PhotoImage(Image.open('/home/pi/Juni/ProjectJuni-Tkinter/src/juniraspberry/src/GUI/Elements_Interface/Robot_Faces/Iris.png'))

funnyEye=ImageTk.PhotoImage(Image.open('/home/pi/Juni/ProjectJuni-Tkinter/src/juniraspberry/src/GUI/Elements_Interface/Robot_Faces/funnyEye.png'))
deadEye=ImageTk.PhotoImage(Image.open('/home/pi/Juni/ProjectJuni-Tkinter/src/juniraspberry/src/GUI/Elements_Interface/Robot_Faces/deadEye.png'))
openEye=ImageTk.PhotoImage(Image.open('/home/pi/Juni/ProjectJuni-Tkinter/src/juniraspberry/src/GUI/Elements_Interface/Robot_Faces/openEye.png'))
sadEye=ImageTk.PhotoImage(Image.open('/home/pi/Juni/ProjectJuni-Tkinter/src/juniraspberry/src/GUI/Elements_Interface/Robot_Faces/sadEye.png'))
closedEye=ImageTk.PhotoImage(Image.open('/home/pi/Juni/ProjectJuni-Tkinter/src/juniraspberry/src/GUI/Elements_Interface/Robot_Faces/closedEye.png'))

normalM=ImageTk.PhotoImage(Image.open('/home/pi/Juni/ProjectJuni-Tkinter/src/juniraspberry/src/GUI/Elements_Interface/Robot_Faces/normalMouth2.png'))
happyM=ImageTk.PhotoImage(Image.open('/home/pi/Juni/ProjectJuni-Tkinter/src/juniraspberry/src/GUI/Elements_Interface/Robot_Faces/speakMouth.png'))
weirdM=ImageTk.PhotoImage(Image.open('/home/pi/Juni/ProjectJuni-Tkinter/src/juniraspberry/src/GUI/Elements_Interface/Robot_Faces/weirdMouth.png'))

funnyEyeL = face.create_image(200, 120, image = funnyEye, state = HIDDEN)
deadEyeL = face.create_image(200, 120, image = deadEye, state = HIDDEN)
openEyeL = face.create_image(200, 120, image = openEye, state = HIDDEN)
sadEyeL = face.create_image(200, 120, image = sadEye, state = HIDDEN)
closedEyeL = face.create_image(200, 120, image = closedEye, state = HIDDEN)

funnyEyeR = face.create_image(600, 120, image = funnyEye, state = HIDDEN)
deadEyeR = face.create_image(600, 120, image = deadEye, state = HIDDEN)
openEyeR = face.create_image(600, 120, image = openEye, state = HIDDEN)
sadEyeR = face.create_image(600, 120, image = sadEye, state = HIDDEN)
closedEyeR = face.create_image(600, 120, image = closedEye, state = HIDDEN)

normalMouth = face.create_image(400, 360, image = normalM, state = HIDDEN)
happyMouth = face.create_image(400, 360, image = happyM, state = HIDDEN)
weirdMouth = face.create_image(400, 360, image = weirdM, state = HIDDEN)

IrisL = face.create_image(200, 120, image = Iris, state = NORMAL)
IrisR = face.create_image(600, 120, image = Iris, state = NORMAL)
IrisM = face.create_image(400, 360, image = Iris, state = NORMAL)

allAssets = [IrisL, IrisR, IrisM, normalMouth, happyMouth, weirdMouth, funnyEyeR,
             deadEyeR, openEyeR, sadEyeR, closedEyeR, funnyEyeL, deadEyeL, openEyeL, sadEyeL, closedEyeL]

#Test zone
#button1 = Button(root, text = "WakeUp", command=wakeUpAnimation1)
#button2 = Button(root, text = "GoSleep", command=sleepAnimation1)
#button3 = Button(root, text = "Speak", command=lancer_assistant)



#Compil
face.pack()
#button1.pack()
#button2.pack()
#button3.pack()



root.mainloop()