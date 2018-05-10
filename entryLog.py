import cv2
import numpy as np
import database
from tkinter import messagebox
from imutils.video import WebcamVideoStream
import datetime
import sys
import time


class EntryLog:

    def __init__(self):

        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read('trainer/trainer.yml')
        self.cascadePath = "haarcascade/haarcascade_frontalface_default.xml"
        self.faceCascade = cv2.CascadeClassifier(self.cascadePath)
        self.ops = sys.platform
        self.font = cv2.FONT_HERSHEY_DUPLEX
        self.d = database.Database().getAll()
        self.updated = False
        if self.ops == 'win32':
            # from imutils.video import WebcamVideoStream
            # self.cam = WebcamVideoStream(src=0).start()
            self.cam = cv2.VideoCapture(0)
        else:
            from imutils.video.pivideostream import PiVideoStream
            self.cam = PiVideoStream().start()
        self.ls = {}
        for doc in self.d:
            self.ls[doc['id']] = doc['name']
        self.name = 'unknown'
        self.idarr = []
        self.i = 0
        self.q = False
        self.counts = 0
        # params for ShiTomasi corner detection
        self.feature_params = dict(maxCorners=100,
                                   qualityLevel=0.3,
                                   minDistance=7,
                                   blockSize=7)
        # Parameters for lucas kanade optical flow
        self.lk_params = dict(winSize=(15, 15),
                              maxLevel=5,
                              criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

        # define movement threshodls
        self.max_head_movement = 20
        self.movement_threshold = 50
        if self.ops == 'win32':
            self.gesture_threshold = 150
        else:
            self.gesture_threshold = 75
        self.x = 0
        self.y = 0
        # find the face in the image
        self.face_found = False
        self.frame_num = 0

    def get_coords(self, p1):
        try:
            return int(p1[0][0][0]), int(p1[0][0][1])
        except:
            return int(p1[0][0]), int(p1[0][1])

    def attn(self):

        # if self.ops == 'win32':
        #     # from imutils.video import WebcamVideoStream
        #     # self.cam = WebcamVideoStream(src=0).start()
        #     self.cam = cv2.VideoCapture(0)
        # else:
        #     from imutils.video.pivideostream import PiVideoStream
        #     self.cam = PiVideoStream().start()
        # self.cam = WebcamVideoStream(src=0).start()
        while True:
            if self.q:
                break
            while True:
                if self.ops == 'win32':
                    ret, im = self.cam.read()
                else:
                    im = self.cam.read()
                self.gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                faces = self.faceCascade.detectMultiScale(self.gray, 1.2, 5)
                if self.updated:
                    if (datetime.datetime.now() - self.t).total_seconds() < 2:
                        cv2.putText(im, 'Welcome ' + self.name, (50, 50), self.font, 0.8, (0, 255, 0), 2)
                for (x, y, w, h) in faces:
                    cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
                    Id, conf = self.recognizer.predict(self.gray[y:y + h, x:x + w])
                    self.face_found = True
                    if cv2.waitKey(10) == ord('q'):
                        self.q = True
                        break
                    if (conf >= 50):
                        self.name = self.ls.get(Id)
                        self.id = Id
                        # print(self.name, Id, conf)
                        self.idarr.append(Id)

                    cv2.putText(im, str(self.name), (x, y + h), self.font, 1, (255, 255, 255))
                cv2.namedWindow("Entry")
                cv2.imshow("Entry", im)
                if cv2.waitKey(10) == ord('q'):
                    self.q = True
                    break
                if len(self.idarr) == 30:
                    self.counts = np.bincount(np.array(self.idarr))
                    break

            if self.q:
                break

            if self.face_found:
                face_center = x + w / 2, y + h / 3
                self.p0 = np.array([[face_center]], np.float32)

            # self.ls.get(np.argmax())
            if self.confirm():
                now = datetime.datetime.now()
                day = str(now.year) + '-' + str(now.month) + '-' + str(now.day)
                log = []
                d = database.Database().getlogbydate(day)
                # if not d:
                #     m = {'_id': day, 'logs': []}
                #     database.Database().pushEntryLog(m)
                #     log = []
                if d:
                    log = d['logs']
                # self.now = datetime.datetime.now()
                self.updated = True
                l = {'id': self.id, 'name': self.name, 'timestamp': now.strftime("%H:%M:%S.%f")}
                log.append(l)
                database.Database().updatelog(day, log, self.name)
                self.t = datetime.datetime.now()

        if self.ops == 'win32':
            self.cam.release()
        else:
            self.cam.stop()
        cv2.waitKey(1)
        cv2.destroyAllWindows()

    def confirm(self):
        self.idarr = []
        self.counts = 0
        if self.gesture():
            return True
        else:
            return False

    def gesture(self):
        gesture = False
        x_movement = 0
        y_movement = 0

        while True:

            if self.ops == 'win32':
                ret, frame = self.cam.read()

            else:
                frame = self.cam.read()
            old_gray = self.gray.copy()
            self.gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, self.gray, self.p0, None, **self.lk_params)
            cv2.circle(frame, self.get_coords(p1), 4, (0, 0, 255), -1)
            cv2.circle(frame, self.get_coords(self.p0), 4, (255, 0, 0))

            # get the xy coordinates for points p0 and p1
            a, b = self.get_coords(self.p0), self.get_coords(p1)
            x_movement += abs(a[0] - b[0])
            y_movement += abs(a[1] - b[1])

            if not gesture: cv2.putText(frame, 'detected:', (50, 50), self.font, 0.8, (0, 0, 0), 2)
            if not gesture: cv2.putText(frame, self.name, (180, 50), self.font, 0.8, (255, 0, 0), 2)
            # text = 'x_movement: ' + str(x_movement)
            text = 'nod to confirm'
            if not gesture: cv2.putText(frame, text, (50, 100), self.font, 0.8, (0, 255, 0), 2)
            # text = 'y_movement: ' + str(y_movement)
            text = 'shake to cancel'
            if not gesture: cv2.putText(frame, text, (50, 150), self.font, 0.8, (0, 0, 255), 2)

            if cv2.waitKey(10) == ord('q'):
                self.q = True
                break

            if x_movement > self.gesture_threshold:
                self.updated = False
                return False
            if y_movement > self.gesture_threshold:
                return True

            self.p0 = p1

            cv2.imshow("Entry", frame)
            cv2.waitKey(1)
