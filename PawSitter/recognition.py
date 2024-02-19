import cv2
import numpy as np
from picamera import PiCamera
from picamera.array import PiRGBArray
import time
import firebase_admin
from firebase_admin import db, credentials

# Create firebase datebase
cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred, {"databaseURL": "https://pawsitter-c4dc0-default-rtdb.firebaseio.com/"})

# creating reference to root node
ref = db.reference("/")


path = '/home/guwantha/project/Cat and Dog recognizer/captured/pic.jpg'
animal = None

thres = 0.6 # Threshold to detect object

# PiCamera
cap = PiCamera(framerate = 10)
time.sleep(2)
cap.resolution = (640,480)
rawCapture = PiRGBArray(cap, size=cap.resolution)
start = time.time()

classNames = []
classFile = 'coco.names'    # 17 - Cat, 18 - Dog
with open(classFile,'rt') as f:
    classNames = [line.rstrip() for line in f]


configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = 'frozen_inference_graph.pb'

net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)


for frame in (cap.capture_continuous(rawCapture, format="bgr", use_video_port=True)):
    img = frame.array.copy()
    classIds, confs, bbox = net.detect(img,confThreshold=thres)
    print(classIds)
    color = (0,255,0)
    thickness = 2
    #cv2.rectangle(img, (20,40),(100, 200), color, thickness)
    if len(classIds) != 0:
        for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
            animalID = classId - 1
            #print(box)
            #cv2.rectangle(img, (box[0], box[3]), (box[2], box[3]), color=(0, 255, 0), thickness=2)
            cv2.rectangle(img,box,color,thickness)
            #cv2.putText(img,classNames[animalID],(box[0]+10,box[1]+30), cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)


    cv2.imshow('Output',img)
    
    for classId in classIds:
        if classId == 17:
           cv2.imwrite(path, img) 
           animal = 'Cat'
           print('Cat')
           db.reference("Pawsitter/").update({"animal":animal})
           
        elif classId == 18:
            cv2.imwrite(path, img)
            animal = 'Dog'
            print('Dog')
            db.reference("Pawsitter/").update({"animal":animal})
        
            

    if cv2.waitKey(20) & 0xFF==ord('d'):
        break
    rawCapture.truncate(0)

# cap.release()
cv2.destroyAllWindows()
