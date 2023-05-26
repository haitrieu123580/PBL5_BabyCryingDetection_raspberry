import RPi.GPIO as GPIO
import time


class AlphaBot(object):

    def __init__(self, in1=13, in2=12, ena=6, in3=21, in4=20, enb=26):

        self.IN1 = in1

        self.IN2 = in2

        self.ENA = ena

        GPIO.setmode(GPIO.BCM)

        GPIO.setwarnings(False)

        GPIO.setup(self.IN1, GPIO.OUT)

        GPIO.setup(self.IN2, GPIO.OUT)

        GPIO.setup(self.ENA, GPIO.OUT)

    # Hàm điều khiển motor DC

    def swing(self, duration=5):
        self.PWMA = GPIO.PWM(self.ENA, 100)

        self.PWMA.start(15)
        # Thực hiện xoay motor trong 5 giây
        while True:
            
            print('swing')
            GPIO.output(self.IN1,GPIO.LOW)

            GPIO.output(self.IN2,GPIO.HIGH)
            time.sleep(5)
            # Tắt motor
            GPIO.output(self.IN1,GPIO.LOW)
    
            GPIO.output(self.IN2,GPIO.LOW)
            print('stop')
            break



  
 
       
 

