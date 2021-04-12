import cv2
import os

cam = cv2.VideoCapture(0)
cam.set(3, 640) # profondeur
cam.set(4, 480) # hauteur

face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

face_id = input('\n Entrez l ID de l utilisateur et appuyer sur <return> ==>  ')

print("\n [INFO] Initialisation de la capture. Regardez la camera et attendez...")

# Initialisation du compteur pour les échantillons de photos
count = 0

while(True):

    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:

        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
        count += 1

        # Sauvegarde les images dans le dossier dataset
        cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])

        cv2.imshow('image', img)

    k = cv2.waitKey(100) & 0xff 
    if k == 27:
        break
    elif count >= 30: # Prend 30 photos et stop la video
         break

print("\n [INFO] Fin du programme")
cam.release()
cv2.destroyAllWindows()
