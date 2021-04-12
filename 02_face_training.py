import cv2
import numpy as np
from PIL import Image
import os

# Chemin pour la base de donnée
path = 'dataset'

recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml");

# fonction qui obtient les images et les étiquettes
def getImagesAndLabels(path):

    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
    faceSamples=[]
    ids = []

    for imagePath in imagePaths:

        PIL_img = Image.open(imagePath).convert('L') # converti en image de gris
        img_numpy = np.array(PIL_img,'uint8')

        id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces = detector.detectMultiScale(img_numpy)

        for (x,y,w,h) in faces:
            faceSamples.append(img_numpy[y:y+h,x:x+w])
            ids.append(id)

    return faceSamples,ids

print ("\n [INFO] Entrainement du model. Cela va prendre quelques instants...")
faces,ids = getImagesAndLabels(path)
recognizer.train(faces, np.array(ids))

# Sauvegarde le model dans trainer/trainer.yml
recognizer.write('trainer/trainer.yml') 

print("\n [INFO] {0} visage entrainé. Fin du programme.".format(len(np.unique(ids))))
