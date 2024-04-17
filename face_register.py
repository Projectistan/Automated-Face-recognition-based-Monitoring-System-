import sys
import cv2
import time
import os
import numpy as np
import urllib.request
import tkinter as tk


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(BASE_DIR, "dataset")

def alert():
    popup = tk.Tk()
    popup.wm_title("!")
    label = tk.Label(popup, text="User Created Succesfully")
    label.pack(side="top", fill="x", pady=10)
    B1 = tk.Button(popup, text="OK", command = popup.destroy)
    B1.pack()
    popup.mainloop()

def createUser(name):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    image_dir = os.path.join(BASE_DIR, "dataset")

    image_folder = os.path.join(image_dir, name)
    folder_create = os.mkdir(image_folder)

    save_folder = os.path.join(image_folder, name)
    alert()

   # python = sys.executable
    #os.execl(python, python, *sys.argv)


def capture(name1):
    name = name1
    cap = cv2.VideoCapture(0)

    face_count = 0
    i=0
    while True:
        i=i+1


        ret, frame = cap.read()

        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if frame is not None:
            if i > 30:
                i=0
                face_count += 1
                #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                file_path = image_dir+'/'+name+'/user'+str(face_count)+'.jpg'
                cv2.imwrite(file_path,frame)

            cv2.putText(frame, str(face_count), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('netik', frame)
        if cv2.waitKey(20)  & 0xFF == ord('q'):
            break

    #cap.release()
    cv2.destroyAllWindows()



