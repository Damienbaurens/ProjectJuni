#!/usr/bin/python3

#Importations
import rospy
from std_msgs.msg import Int16MultiArray

#fonction à mettre au dessus du main
def ImagePosPublisher(deltaX,deltaY):

    rate = rospy.Rate(2) #on communique à une fréquence max de 2 Hz pour pas surcharger le réseau
    pub = rospy.Publisher('touchScreenPos', Int16MultiArray, queue_size =1) #de ligne 11 à 15 : publication en elle même
    pos = Int16MultiArray()
    pos.data = [deltaX,deltaY]
    rospy.loginfo(pos.data)
    pub.publish(pos)
    rate.sleep()

#Initialisation de la node : doit être appelé dans le main, avant de lancer les boucles
rospy.init_node("ImageReco", anonymous = True)

import cv2
import numpy as np
import os 

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);

font = cv2.FONT_HERSHEY_SIMPLEX


id = 0

names = ['None', 'Kevin', 'Damien', 'Eloi','Inconnu','Theodore', 'Hugo','Mehdi'] 

# Initialise et commence la capture video
cam = cv2.VideoCapture(0)
cam.set(3, 640) # profondeur
cam.set(4, 480) # hauteur

# Defini le minimum de la taille de la fenetre pour reconnaitre le visage
minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)

x_fenetre = 320
y_fenetre = 240
while True:

    ret, img =cam.read()
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale( 
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (int(minW), int(minH)),
       )

    for(x,y,w,h) in faces:

        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

        #Calcul ecart entre millieu rectangle et milieu de la fenetre
        x_rectangle = (x+x+w)/2
        y_rectangle = (y+y+h)/2        
        ecart_x = print("ecartx",x_rectangle - 320)
        ecart_y = print("ecarty",y_rectangle - 240)

        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
            #Defini le pourcentage de reconnaissance mais ici on ne l'utilise pas
        if (confidence < 100):
            id = names[id]
            confidence = "  {0}%".format(round(100 - confidence))
        else:
            id = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))
        
        cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
        #cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
    
    cv2.imshow('camera',img) 

    k = cv2.waitKey(10) & 0xff 
    if k == 27:
        break


print("\n [INFO] Fin du programme")
cam.release()
cv2.destroyAllWindows()
