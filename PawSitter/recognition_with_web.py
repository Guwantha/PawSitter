import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray
import time
#from server.py import request

path = '/home/guwantha/project/Cat and Dog recognizer/captured/pic.jpg'

thres = 0.6 # Threshold to detect object

# Webcam
#cap = cv2.VideoCapture(0)
#cap.set(3,1280)
#cap.set(4,720)
#cap.set(10,70)

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

from http.server import BaseHTTPRequestHandler, HTTPServer
import subprocess

request = None

class RequestHandler_httpd(BaseHTTPRequestHandler):
  def do_GET(self):
    global request
    messagetosend = bytes('PawSitter',"utf")
    self.send_response(200)
    self.send_header('Content-Type', 'text/plain')
    self.send_header('Content-Length', len(messagetosend))
    self.end_headers()
    self.wfile.write(messagetosend)
    request = self.requestline
    request = request[5 : int(len(request)-9)]
    print(request)
    if request == 'cat':
        print('Cat')
        #exec(open('recognition.py').read())
    if request == 'dog':
        print('Dog')
    return


server_address_httpd = ('192.168.43.155',8080)
httpd = HTTPServer(server_address_httpd, RequestHandler_httpd)
print('Starting server')
httpd.serve_forever()
GPIO.cleanup()


for frame, i in zip(cap.capture_continuous(rawCapture, format="bgr", use_video_port=True), range(400)):
    img = frame.array
    classIds, confs, bbox = net.detect(img,confThreshold=thres)
    print(classIds)

    if len(classIds) != 0:
        for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
            animalID = classId - 1
            # cv2.rectangle(frame,box,color=(0,255,0),thickness=2)
            # cv2.putText(img,classNames[animalID],(box[0]+10,box[1]+30), cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)


    cv2.imshow('Output',img)
    
    for classId in classIds:
        if classId == 17:
           cv2.imwrite(path, img) 
           #exec(open('predict_animal.py').read())
           print('Cat')

        elif classId == 18:
            cv2.imwrite(path, img)
            #exec(open('predict_animal.py').read())
            print('Dog')

    if cv2.waitKey(20) & 0xFF==ord('d'):
        break
    rawCapture.truncate(0)

# cap.release()
cv2.destroyAllWindows()
