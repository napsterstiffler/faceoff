# FaceOff

Platforms:
1. Windows
2. Raspberry Pi Model 3B (will be pretty laggy on any other model)


Features: 
1. Create face dataset by cropping face images from webcam feed. 
2. Upload user's id and name to online mongo database.
3. Train model using face dataset
4. Recognize face using LPBH
5. Entrylog operations:
    a. Recognize face in multiple frames
    b. Analyze recognized face frames and display the Aggregate id (for more accuracy)
    c. Ask user to confirm by nodding or cancel by shaking head
    d. Perform motion analysis and predict if head movement is nod or shake. 
    e. If shake, cancel. If nod, add user timestamp in mongo database of the document for that day. 
    
Usage: 
1. Create free account on https://mlab.com/home and create a database named "faceoff" (you can give it a different name
    but you will have to edit the database.py file and replace "faceoff" with your name)
2. Create a user in your database and give it a unique password
3. Create 2 collections in your databased named "faces" and "entrylog"
4. Install all required packages in python 3.6
5. Clone this project on your computer/raspberry pi
6. Open conf/pass.yml and replace the <> with your mlab URI (Enter your user's username and password in the URI)
7. Run project using "python start.py" in console
8. First click on "Add Face" to add as many faces as you want. Then click on "Train Model". You can now use all other buttons. 
    
    
Requirements:
1. Python 3.6
2. OpenCV 3
3. imutils
4. tkinter
5. numpy


Experimenting:
1. Adding basic emotion analysis as a decorative feature (Smile detection has been added but it is pretty inaccurate)
2. Using OpenCV's deep learning face detection to improve accuracy



Details:
This is part of my Project for Master's Degree in Advanced IT. The application was made to work with Raspberrypi so it works with very low resource computers. I'm continuously trying to increase performance. Threading has been implemented to significantly improve fps of camera even on the Raspberrypi. Since simple LPBH algorithm is used I had to add a few more tricks to try and improve accuracy (like adding a method to take a couple of recognized ids in a list and then perform operations on the list to get the most common id). 
This project is in active development. 
