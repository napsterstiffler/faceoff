import cv2
import os
import numpy as np
from PIL import Image
import ftplib


class FaceTrainer:

    def __init__(self):
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.detector = cv2.CascadeClassifier("haarcascade/haarcascade_frontalface_default.xml")


    def getImagesAndLabels(self):
        # get the path of all the files in the folder
        imagePaths = [os.path.join('dataSet', f) for f in os.listdir('dataSet')]
        # create empth face list
        faceSamples = []
        # create empty ID list
        Ids = []
        # now looping through all the image paths and loading the Ids and the images
        for imagePath in imagePaths:
            # loading the image and converting it to gray scale
            pilImage = Image.open(imagePath).convert('L')
            # Now we are converting the PIL image into numpy array
            imageNp = np.array(pilImage, 'uint8')
            # getting the Id from the image
            Id = int(os.path.split(imagePath)[-1].split(".")[1])
            # extract the face from the training image sample
            faces = self.detector.detectMultiScale(imageNp)
            # If a face is there then append that in the list as well as Id of it
            for (x, y, w, h) in faces:
                faceSamples.append(imageNp[y:y + h, x:x + w])
                Ids.append(Id)
        #return faceSamples, Ids
        self.recognizer.train(faceSamples, np.array(Ids))
        self.recognizer.write('trainer/trainer.yml')


