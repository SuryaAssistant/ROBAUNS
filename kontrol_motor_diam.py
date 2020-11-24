import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

mtr_dpn_en_r = 20
mtr_dpn_en_l = 26

mtr_blkg_en_r = 16
mtr_blkg_en_l = 19

GPIO.setup(mtr_dpn_en_r , GPIO.OUT) #EN_R
GPIO.setup(mtr_dpn_en_l , GPIO.OUT) #EN_L

# Set pin awal "LOW"
GPIO.setup(mtr_dpn_en_r , GPIO.LOW) #EN_R
GPIO.setup(mtr_dpn_en_l , GPIO.LOW) #EN_L

#------------------------------------------
GPIO.setup(mtr_blkg_en_r , GPIO.OUT) #EN_R
GPIO.setup(mtr_blkg_en_l , GPIO.OUT) #EN_L

# Set pin awal "LOW"
GPIO.setup(mtr_blkg_en_r , GPIO.LOW) #EN_R
GPIO.setup(mtr_blkg_en_l , GPIO.LOW) #EN_L


GPIO.output(mtr_blkg_en_r , GPIO.LOW)  
GPIO.output(mtr_blkg_en_l , GPIO.LOW)
GPIO.output(mtr_dpn_en_r , GPIO.LOW)  
GPIO.output(mtr_dpn_en_l , GPIO.LOW)
print ("Berhenti")
