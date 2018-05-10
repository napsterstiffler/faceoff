from tkinter import *
from tkinter import messagebox
import os
import datasetCreator
import numpy as np
import faceTrainer
import detector
import entryLog
import time
import database
import json
import ViewUsers
import ymloperations


class Gui:

    def __init__(self):
        self.root = Tk()
        self.root.title("FaceOff")
        self.root.geometry('350x450')
        if sys.platform == 'win32':
            self.root.wm_iconbitmap('icon2.ico')
            btn1 = Button(self.root, text="Add Face", bg="Green", fg="White", padx=5, pady=5, command=self.addnewdata)
            btn1.grid(column=0, row=3, pady=10)
            btn2 = Button(self.root, text="Train Model", bg="Red", fg="White", command=self.facetrainer, padx=5, pady=5)
            btn2.grid(column=0, row=4)



        self.lbl = Label(self.root, text="Face Off", font=("TkHeadingFont", 20))
        self.lbl.grid(column=0, row=0, pady=20, padx=120)

        self.lbl1 = Label(self.root, text="Face Detection", fg="RED", pady=10)
        self.lbl1.grid(column=0, row=1)


        btn3 = Button(self.root, text="Face Recognition", bg="Blue", fg="White", command=self.facedetector, padx=5,
                      pady=5)
        btn3.grid(column=0, row=5, pady=10)

        btn4 = Button(self.root, text="Entry Log", bg="Orange", fg="White", command=self.entrylog, padx=5,
                      pady=5)
        btn4.grid(column=0, row=7, pady=10)

        btn5 = Button(self.root, text="View Users", bg="purple", fg="White", command=self.viewuser, padx=5,
                      pady=5)
        btn5.grid(column=0, row=8, pady=10)

        if sys.platform == 'win32':
            Button(self.root, text="upload model", bg="yellow", fg="Black", command=self.ymlmanip, padx=5,
                        pady=5).grid(column=0, row=9, pady=10)
        else:
            Button(self.root, text="download model", bg="yellow", fg="Black", command=self.ymlmanip, padx=5,
                        pady=5).grid(column=0, row=9, pady=10)




        self.root.mainloop()

    def addnewdata(self):
        n1 = datasetCreator
        n1.DatasetCreator()

    def ymlmanip(self):
        if sys.platform == 'win32':
            ymloperations.Ymloperations().upload()
            messagebox._show("Success!", "Model uploaded successfully")
        else:
            ymloperations.Ymloperations().download()
            messagebox._show("Success!", "Model downloaded successfully")


    def facetrainer(self):
        n2 = faceTrainer
        n2.FaceTrainer()
        n2.FaceTrainer().getImagesAndLabels()
        messagebox._show("Success!", "Model trained successfully")

    def facedetector(self):
        self.root.destroy()
        n3 = detector
        n3.Detector()
        n3.Detector().recognize()

    def entrylog(self):
        n5 = entryLog
        n5.EntryLog().attn()

    def viewuser(self):
        ViewUsers.ViewUsers().disp(self.root)







