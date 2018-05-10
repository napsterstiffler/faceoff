import cv2
import numpy as np
import sys
import imutils

facePath = "../../haarcascade/haarcascade_frontalface_default.xml"
smilePath = "../../haarcascade/haarcascade_smile.xml"
faceCascade = cv2.CascadeClassifier(facePath)
smileCascade = cv2.CascadeClassifier(smilePath)

if sys.platform == 'win32':
    from imutils.video import WebcamVideoStream
    cap = WebcamVideoStream(src=0).start()
else:
    from imutils.video.pivideostream import PiVideoStream
    cap = PiVideoStream().start()
# cap = cv2.VideoCapture(0)


sF = 1.05

while True:

    # ret, frame = cap.read()  # Capture frame-by-frame
    frame = cap.read()
    img = frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=sF,
        minNeighbors=8,
        minSize=(55, 55),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    # ---- Draw a rectangle around the faces

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]

        smile = smileCascade.detectMultiScale(
            roi_gray,
            scaleFactor=1.7,
            minNeighbors=22,
            minSize=(25, 25),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        # Set region of interest for smiles
        for (x, y, w, h) in smile:
            cv2.rectangle(roi_color, (x, y), (x + w, y + h), (255, 0, 0), 1)
            # print "!!!!!!!!!!!!!!!!!"
            font = cv2.FONT_HERSHEY_COMPLEX
            cv2.putText(frame, ':-)', (x, y + h), font, 1, (255, 255, 0))
    # cv2.cv.Flip(frame, None, 1)

    cv2.imshow('Smile Detector', frame)
    c = cv2.waitKey(7) % 0x100
    if c == 27:
        break

cap.stop()
cv2.destroyAllWindows()
