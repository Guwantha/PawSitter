import RPi.GPIO as GPIO          
from time import sleep

in1 = 27 #27 #24
in2 = 22 #22 #23
en = 17 #17 #25

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)

p=GPIO.PWM(en,100)
p.start(0)
#GPIO.output(en,GPIO.HIGH)
GPIO.output(in1,GPIO.HIGH)
GPIO.output(in2,GPIO.LOW)

print('running')
p.ChangeDutyCycle(25)
sleep(5)
p.ChangeDutyCycle(100)
sleep(5)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.HIGH)
sleep(5)


GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)

print('Stopped')
GPIO.output(en, GPIO.LOW)

GPIO.cleanup()