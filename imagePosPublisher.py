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