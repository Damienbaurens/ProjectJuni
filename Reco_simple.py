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

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)


while True:
    # Read the frame
    _, img = cap.read()
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Detect the faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    # Draw the rectangle around each face
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
    # Display
    cv2.imshow('img', img)
    # Stop if escape key is pressed
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
    
# Release the VideoCapture object
cap.release()
