import cv2
import numpy as np
import database


from imutils.video import FPS
import argparse
import imutils
import Gui
import sys


class Detector:

    def recognize(self):

        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read('trainer/trainer.yml')
        cascadePath = "haarcascade/haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(cascadePath)
        if sys.platform == 'win32':
            from imutils.video import WebcamVideoStream
            cap = WebcamVideoStream(src=0).start()
        else:
            from imutils.video.pivideostream import PiVideoStream
            cap = PiVideoStream().start()
        font = cv2.FONT_HERSHEY_COMPLEX
        d = database.Database().getAll()
        ls = {}
        for doc in d:
            ls[doc['id']] = doc['name']
        name = 'unknown'

        while True:
            im = cap.read()
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, 1.2, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
                Id, conf = recognizer.predict(gray[y:y + h, x:x + w])
                if sys.platform == 'win32':
                    if (conf <= 70):
                        name = ls.get(Id)
                        print(name, Id, conf)
                    else:
                        name = "who?"
                else:
                    if (conf >= 50):
                        name = ls.get(Id)
                        print(name, Id, conf)
                    else:
                        name = "who?"

                cv2.putText(im, str(name), (x, y + h), font, 1, (255, 255, 255))
            cv2.imshow('im', im)
            if cv2.waitKey(10) == ord('q'):
                break
        cap.stop()
        cv2.destroyAllWindows()
        Gui.Gui()


# n = Detector().recognize()
