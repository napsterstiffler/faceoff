from tkinter import *
from tkinter import messagebox
import tkinter as tk
import cv2
import re
import database
import fontawesome as fa
import base64
from PIL import Image , ImageTk


class ViewUsers():

    def __init__(self):
        self.d = database.Database().getAll()



    def disp(self, root):
        i = 0
        # ar = {}
        self.roo = Toplevel(root)
        self.roo.grid_columnconfigure(0, weight=1)
        self.roo.minsize(300, 500)
        self.roo.title("User Faces")
        for doc in self.d:
            Label(self.roo, text=doc['id']).grid(row=i, column=0, padx=15, pady=25)
            Label(self.roo, text=doc['name']).grid(row=i, column=1, padx=15, pady=25)
            im = PhotoImage(data=doc['image'])
            im = im.subsample(4,4)
            # ar[i] = im
            # Label(self.roo, image=im).grid(row=i, column=2)
            lab = Label(self.roo, image=im)
            lab.image = im
            lab.grid(row=i, column=2)

            i = i+1


        self.roo.mainloop()

# vu=ViewUsers().disp()