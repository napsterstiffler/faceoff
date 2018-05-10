import numpy as np
# import argparse
import time
import cv2
from imutils.video import VideoStream


# load the input image from disk
# image = cv2.imread('images/doggo.jpeg')
vs = VideoStream(src=0).start()

# load the class labels from disk
rows = open('synset_words.txt').read().strip().split("\n")
classes = [r[r.find(" ") + 1:].split(",")[0] for r in rows]




while True:
	image = vs.read()
	blob = cv2.dnn.blobFromImage(image, 1, (224, 224), (104, 117, 123))


	net = cv2.dnn.readNetFromCaffe('bvlc_googlenet.prototxt', 'bvlc_googlenet.caffemodel')

	# set the blob as input to the network and perform a forward-pass to
	# obtain our output classification
	net.setInput(blob)
	start = time.time()
	preds = net.forward()
	end = time.time()
	print("[INFO] classification took {:.5} seconds".format(end - start))

	# sort the indexes of the probabilities in descending order (higher
	# probabilitiy first) and grab the top-5 predictions
	idxs = np.argsort(preds[0])[::-1][:5]

	# loop over the top-5 predictions and display them
	for (i, idx) in enumerate(idxs):
		# draw the top prediction on the input image
		if i == 0:
			text = "Prediction: {}, {:.2f}%".format(classes[idx], preds[0][idx] * 100)
			cv2.putText(image, text, (5, 25),  cv2.FONT_HERSHEY_SIMPLEX,
				0.7, (0, 0, 255), 2)

	# display the predicted label + associated probability to the
	# console	
		print("[INFO] {}. label: {}, probability: {:.5}".format(i + 1, classes[idx], preds[0][idx]))

	# display the output image
	cv2.imshow("Image", image)
	key = cv2.waitKey(1) & 0xFF

	if key == ord("q"):
		break

cv2.destroyAllWindows()
vs.stop()