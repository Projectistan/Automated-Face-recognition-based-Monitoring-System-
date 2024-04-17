
from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os


def encodings(processvar1):

	process = processvar1
	process.set("Changed")


	# grab the paths to the input images in our dataset
	process.set("[INFO] quantifying faces...")
	imagePaths = list(paths.list_images("dataset"))

	# initialize the list of known encodings and known names
	knownEncodings = []
	knownNames = []


	for (i, imagePath) in enumerate(imagePaths):
		# extract the person name from the image path
		process.set("[INFO] processing image {}/{}".format(i + 1,
																  len(imagePaths)))
		name = imagePath.split(os.path.sep)[-2]

		image = cv2.imread(imagePath)
		rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

		boxes = face_recognition.face_locations(rgb,model="hog")


		encodings = face_recognition.face_encodings(rgb, boxes)

		for encoding in encodings:

			knownEncodings.append(encoding)
			knownNames.append(name)

	process.set("[INFO] serializing encodings...")
	process.set("Co")
	data = {"encodings": knownEncodings, "names": knownNames}
	f = open("encodings.pickle", "wb")
	f.write(pickle.dumps(data))
	f.close()
	process.set("Completed Successfully")