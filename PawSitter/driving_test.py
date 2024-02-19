import RPi.GPIO as GPIO          
from time import sleep
import firebase_admin
from firebase_admin import db, credentials

cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred, {"databaseURL": "https://pawsitter-c4dc0-default-rtdb.firebaseio.com/"})

ref = db.reference("/")

inA1 = 24 #27 #23
inA2 = 23 #22 #24
enA = 25 #17 #25

inB1 = 22 #27 #23
inB2 = 27 #22 #24
enB = 17 #17 #25

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(inA1,GPIO.OUT)
GPIO.setup(inA2,GPIO.OUT)
GPIO.setup(enA,GPIO.OUT)

GPIO.setup(inB1,GPIO.OUT)
GPIO.setup(inB2,GPIO.OUT)
GPIO.setup(enB,GPIO.OUT)

pA=GPIO.PWM(enA,100)
pA.start(0)
pB=GPIO.PWM(enB,100)
pB.start(0)

def forward():
    GPIO.output(inA1,GPIO.HIGH)
    GPIO.output(inA2,GPIO.LOW)
    pA.ChangeDutyCycle(50)
    GPIO.output(inB1,GPIO.HIGH)
    GPIO.output(inB2,GPIO.LOW)
    pB.ChangeDutyCycle(50)

def backward():
    GPIO.output(inA1,GPIO.LOW)
    GPIO.output(inA2,GPIO.HIGH)
    GPIO.output(inB1,GPIO.LOW)
    GPIO.output(inB2,GPIO.HIGH)
    

def stop():
    GPIO.output(inA1,GPIO.LOW)
    GPIO.output(inA2,GPIO.LOW)
    GPIO.output(inB1,GPIO.LOW)
    GPIO.output(inB2,GPIO.LOW)

# while True:
#     user = db.reference("Remote").get()
#     forward_b = user['forward']
#     backward_b = user['backward']
#     left_b = user['left']
#     right_b = user['right']
#     
#     drive = forward_b+backward_b+left_b+right_b
#     #print(drive)
# 
#     if(drive=='1000'):
#         forward()
#     elif(drive=='0100'):
#         backward()
#     else:
#         stop()


forward()
sleep(5)
backward()
sleep(5)
stop()
