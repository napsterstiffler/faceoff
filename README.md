# FaceOff

Platforms:
Windows
Raspberry Pi Model 3B (will be pretty laggy on any other model)


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
    
Usage: run start.py by using the command "python start.py"
    
    
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
