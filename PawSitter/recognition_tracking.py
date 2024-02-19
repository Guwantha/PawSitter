import cv2
import numpy as np
from picamera import PiCamera
from picamera.array import PiRGBArray
import time
# import firebase_admin
# from firebase_admin import db, credentials
# 
# # Create firebase datebase
# cred = credentials.Certificate("credentials.json")
# firebase_admin.initialize_app(cred, {"databaseURL": "https://pawsitter-c4dc0-default-rtdb.firebaseio.com/"})
# 
# # creating reference to root node
# ref = db.reference("/")


path = '/home/guwantha/project/Cat and Dog recognizer/captured/pic.jpg'
animal = None

thres = 0.6 # Threshold to detect object

# PiCamera
cap = PiCamera(framerate = 60)
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

def turn(p1,c1):
    error = int(c1-p1)
    if error>0:
        #turn right
        print(error)
        pass
    elif error<0:
        #trun left
        print(error)
        pass
    else:
        #go forward
        pass

for frame in (cap.capture_continuous(rawCapture, format="bgr", use_video_port=True)):
    img = frame.array.copy()
    classIds, confs, bbox = net.detect(img,confThreshold=thres)
    print(classIds)
    
    color = (0,255,0)
    thickness = 2
    
    cv2.rectangle(img, (180,140),(440, 340), color, thickness)
    cv2.line(img, (320,0),(320,480), (255,0,0), 2)
    cv2.line(img, (0,240),(640,240), (255,0,0), 2)
    c1 = int(640/2)
    c2 = int(480/2)
    cv2.circle(img, (c1,c2), 5, (255,255,255), cv2.FILLED)
    
    if len(classIds) != 0:
        for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
            animalID = classId - 1
            print(box)
            cv2.rectangle(img,box,color,thickness)
            p1 = int(box[2]/2)+box[0]
            p2 = int(box[3]/2)+box[1]
            center = (p1,p2)
            print(center)
            cv2.circle(img, center, 5, (255,0,255), cv2.FILLED)

    cv2.imshow('Output',img)
    
    for classId in classIds:
        if classId == 17:
           cv2.imwrite(path, img) 
           animal = 'Cat'
           print('Cat')
           turn(p1,c1)
           #db.reference("Pawsitter/").update({"animal":animal})
           
        elif classId == 18:
            cv2.imwrite(path, img)
            animal = 'Dog'
            print('Dog')
            turn(p1,c1)
            #db.reference("Pawsitter/").update({"animal":animal})
        
            

    if cv2.waitKey(20) & 0xFF==ord('d'):
        break
    rawCapture.truncate(0)

# cap.release()
cv2.destroyAllWindows()
