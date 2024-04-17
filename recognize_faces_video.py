# USAGE
# python recognize_faces_video.py --encodings encodings.pickle
# python recognize_faces_video.py --encodings encodings.pickle --output output/jurassic_park_trailer_output.avi --display 0

# import the necessary packages
import sys

import face_recognition
from imutils.video import VideoStream, FPS
#import face_recognition
import argparse
import imutils
import pickle
import time
import cv2
import os
import json
import datetime
# construct the argument parser and parse the arguments

def startRecognition():


	store = '['
	# folder creation
	if not os.path.exists('known'):
		print("New directory created")
		os.makedirs('known')
	if not os.path.exists('Unknown'):
		os.makedirs('Unknown')
	if not os.path.exists('logJson'):
		os.makedirs('logJson')

	# load the known faces and embeddings
	print("[INFO] loading encodings...")
	data = pickle.loads(open("encodings.pickle", "rb").read())

	BASE_DIR = os.path.dirname(os.path.abspath(__file__))
	log_dir = os.path.join(BASE_DIR, "logJson")

	# initialize the video stream
	print("[INFO] starting video stream...")
	vs = VideoStream(src=0).start()
	writer = None
	time.sleep(2.0)
	fps = FPS().start()
	f = 1
	# loop over frames
	ktemp = []
	utemp = []
	while True:

		frame = vs.read()
		f=f+1

		# convert the input frame from BGR to RGB then resize it to have
		# a width of 750px (to speedup processing)
		rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		rgb = imutils.resize(frame, width=750)
		r = frame.shape[1] / float(rgb.shape[1])

		# detect the (x, y)-coordinates of the bounding boxes
		# corresponding to each face in the input frame, then compute
		# the facial embeddings for each face
		boxes = face_recognition.face_locations(rgb,
												model="hog")
		encodings = face_recognition.face_encodings(rgb, boxes)
		names = []

		# loop over the facial embeddings
		for encoding in encodings:
			# attempt to match each face in the input image to our known
			# encodings
			matches = face_recognition.compare_faces(data["encodings"],
													 encoding)
			name = "Unknown"

			# check to see if we have found a match
			if True in matches:
				# find the indexes of all matched faces then initialize a
				# dictionary to count the total number of times each face
				# was matched
				matchedIdxs = [i for (i, b) in enumerate(matches) if b]
				counts = {}
				print(matchedIdxs)
				# loop over the matched indexes and maintain a count for
				# each recognized face face
				for i in matchedIdxs:
					name = data["names"][i]
					counts[name] = counts.get(name, 0) + 1

				# determine the recognized face with the largest number
				# of votes (note: in the event of an unlikely tie Python
				# will select first entry in the dictionary)
				name = max(counts, key=counts.get)

			# update the list of names
			names.append(name)

		# loop over the recognized faces
		for ((top, right, bottom, left), name) in zip(boxes, names):
			# rescale the face coordinates
			top = int(top * r)
			right = int(right * r)
			bottom = int(bottom * r)
			left = int(left * r)

			# draw the predicted face name on the image
			cv2.rectangle(frame, (left, top), (right, bottom),
						  (0, 255, 0), 2)
			y = top - 15 if top - 15 > 15 else top + 15
			cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
						0.75, (0, 255, 0), 2)

			if name != "Unknown":
				if name not in ktemp:
					ktemp.append(name)
					file_path = 'known/' + str(name) + '.jpg'
					cv2.imwrite(file_path, frame)
				store += '{"name" : "' + name + '", "datetime" : "' + str(time.time()) + '"},'
			# fp.write("name:" + name + ':' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + '\n')
			else:
				#print(os.getcwd())
				if(f>4):
					f=1
					file_path = 'Unknown/' + name + '_' + time.strftime('%H-%M-%S', time.localtime())  + '.jpg'
					cv2.imwrite(file_path, frame)
				store += '{"name" : "' + name + '", "datetime" : "' + str(time.time()) + '"},'


		# check to see if we are supposed to display the output frame to
		# the screen
		if 1> 0:
			cv2.imshow("Frame", frame)
			key = cv2.waitKey(1) & 0xFF

			# if the q key was pressed, break from the loop
			if key == ord("q"):
				break

	store += ']'
	fps.stop()

	RAW_FILE = datetime.date.today().strftime("%d-%m-%y")

	if not os.path.exists('logJson/'+RAW_FILE + '.json'):
		# print("New directory created")
		fp = open('logJson/'+RAW_FILE + '.json', 'w+')
		fp.write(store.split(',]')[0] + ']')
		fp.close()
	else:
		with open('logJson/'+RAW_FILE + '.json', 'a') as fp:
			fp.write(store.split(',]')[0] + ']')
		fp.close()

		with open('logJson/'+RAW_FILE + '.json', 'r') as fp:
			line = fp.read()
		# print(line)

		with open('logJson/'+RAW_FILE + '.json', 'w') as f:
			f.write(line.replace('][', ','))

		f.close()
		fp.close()

	print("Elasped time: {:.2f}".format(fps.elapsed()))
	print("Approx. FPS: {:.2f}".format(fps.fps()))
	# do a bit of cleanup
	cv2.destroyAllWindows()
	vs.stop()

	# check to see if the video writer point needs to be released
	if writer is not None:
		writer.release()

	python = sys.executable
	os.execl(python, python, *sys.argv)
