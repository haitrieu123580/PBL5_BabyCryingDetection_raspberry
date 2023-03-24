import RPi.GPIO as GPIO 
import time 
class AlphaBot(object):
  
 
    def __init__(self,in1=13,in2=12,ena=6,in3=21,in4=20,enb=26):
 
        self.IN1 = in1
 
        self.IN2 = in2
 
        self.ENA = ena
 
 
 
        GPIO.setmode(GPIO.BCM)
 
        GPIO.setwarnings(False)
 
        GPIO.setup(self.IN1,GPIO.OUT)
 
        GPIO.setup(self.IN2,GPIO.OUT)

 
        GPIO.setup(self.ENA,GPIO.OUT)
 
        self.stop()
 
        self.PWMA = GPIO.PWM(self.ENA,100)
  
        self.PWMA.start(10)

 
 
    def backward(self):
 
        GPIO.output(self.IN1,GPIO.HIGH)
 
        GPIO.output(self.IN2,GPIO.LOW)
 
 
    def stop(self):
 
        GPIO.output(self.IN1,GPIO.LOW)
 
        GPIO.output(self.IN2,GPIO.LOW)
 
        print('stop')

 
    def forward(self):
        while True:
            GPIO.output(self.IN1,GPIO.LOW)
    
            GPIO.output(self.IN2,GPIO.HIGH)
    
            print('go')
            print()
            time.sleep(5)
            
            self.stop()
            time.sleep(1)
            
    def setPWMA(self,value):
 
        self.PWMA.ChangeDutyCycle(value)
  
 
       
 

