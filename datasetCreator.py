from tkinter import *
from tkinter import messagebox
import tkinter as tk
import cv2
import re
import database
import fontawesome as fa
import base64
from PIL import Image


class DatasetCreator():

    def __init__(self):
        self.ro = Tk()
        self.ro.minsize(320, 200)
        if sys.platform == 'win32':
            self.ro.wm_iconbitmap('camera.ico')
        self.ro.title("Add Face")
        Label(self.ro, text="Enter Id: ").grid(row=0, padx=15, pady=25)
        Label(self.ro, text="Enter Name: ").grid(row=1, padx=15, pady=25)
        self.Id = tk.Entry(self.ro)
        self.Name = tk.Entry(self.ro)
        self.btn = tk.Button(self.ro, text="Submit", command=self.on_button)
        self.Id.grid(row=0, column=1)
        self.Name.grid(row=1, column=1)
        self.btn.grid(row=2, columnspan=2)

    def on_button(self):
        a = self.validate()
        if a == True:
            self.makedata(self.Id.get(), self.Name.get())
        else:
            messagebox._show("Error!", "Id: " + self.Id.get() + " already exists in Database")

    def validate(self):
        d = database.Database().getAll()
        flg = 0
        for doc in d:
            if str(doc['id']) == str(self.Id.get()):
                flg = 1
        if flg == 0:
            return True
        else:
            return False

    def makedata(self, Id, Name):
        cam = cv2.VideoCapture(0)
        detector = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')

        sampleNum = 0
        while (True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                # incrementing sample number
                sampleNum = sampleNum + 1
                # saving the captured face in the dataset folder
                cv2.imwrite("dataSet/User." + Id + '.' + str(sampleNum) + ".png", gray[y:y + h, x:x + w])
                if sampleNum == 10:
                    cv2.imwrite("dataSet/dp." + Id + ".png", img[y:y + h, x:x + w])

                cv2.imshow('frame', img)
            # wait for 100 miliseconds

            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # break if the sample number is more than 20
            elif sampleNum > 100:
                with open("dataSet/dp." + Id + ".png", "rb") as image_file:
                    b64 = base64.b64encode(image_file.read())
                # with open("imageToSave.png", "wb") as fh:
                #     fh.write(base64.decodebytes(b64))
                messagebox._show("Success!", Id + " added successfully")
                break
        cam.release()
        m = {'id': int(Id), 'name': Name, 'image': b64}
        database.Database().pushRECORD(m)
        cv2.destroyAllWindows()
        self.ro.destroy()



# Id = input('enter your id')
