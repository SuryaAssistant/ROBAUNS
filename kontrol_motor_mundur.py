import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

mtr_blkg_en_r = 16
mtr_blkg_en_l = 19

GPIO.setup(mtr_blkg_en_r , GPIO.OUT) #EN_R
GPIO.setup(mtr_blkg_en_l , GPIO.OUT) #EN_L

# Set pin awal "LOW"
GPIO.setup(mtr_blkg_en_r , GPIO.LOW) #EN_R
GPIO.setup(mtr_blkg_en_l , GPIO.LOW) #EN_L


GPIO.output(mtr_blkg_en_r , GPIO.HIGH)  
GPIO.output(mtr_blkg_en_l , GPIO.LOW) 
print ("mundur")
sleep(0.05)
