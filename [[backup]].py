from __future__ import print_function
#for Videostream
import imutils
from imutils.video import VideoStream
#for QR library
from pyzbar import pyzbar
#for timing and delay
from time import sleep
import time
#for I/O pins
import RPi.GPIO as GPIO
#for numerical and other calculation
import numpy as np
import argparse
#for OpenCV
import cv2
#for serial communication Arduino-Raspberry Pi
import serial
import subprocess
from subprocess import Popen, PIPE


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#-----------------------------Pin Config-----------------------------#

#------------------SERVO------------------#

servoPIN = 18
GPIO.setup(servoPIN, GPIO.OUT)
p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
p.start(0)
p.ChangeDutyCycle(0)

#--------------Motor Belakang--------------#

mtr_blkg_en_r = 16
mtr_blkg_en_l = 19

GPIO.setup(mtr_blkg_en_r , GPIO.OUT) #EN_R
GPIO.setup(mtr_blkg_en_l , GPIO.OUT) #EN_L

# Set pin awal "LOW"
GPIO.setup(mtr_blkg_en_r , GPIO.LOW) #EN_R
GPIO.setup(mtr_blkg_en_l , GPIO.LOW) #EN_L

#---------------Motor Depan_---------------#

mtr_dpn_en_r = 20
mtr_dpn_en_l = 26

GPIO.setup(mtr_dpn_en_r , GPIO.OUT) #EN_R
GPIO.setup(mtr_dpn_en_l , GPIO.OUT) #EN_L

# Set pin awal "LOW"
GPIO.setup(mtr_dpn_en_r , GPIO.LOW) #EN_R
GPIO.setup(mtr_dpn_en_l , GPIO.LOW) #EN_L

#---------------Encoder_pins---------------#

print("Loading...")
sleep(1.00)

print("Start")

#------------------------------Function------------------------------#
flag_encoder_kanan = 0
flag_encoder_kiri = 0

# looping siklus counter timing encoder
counter_loop_encoder = 0

def kanan():
    GPIO.output(mtr_dpn_en_r , GPIO.LOW)  
    GPIO.output(mtr_dpn_en_l , GPIO.HIGH) 
    print ("kanan")
    flag_encoder_kanan = 1
    sleep(0.25)
    GPIO.output(mtr_dpn_en_r , GPIO.LOW)  
    GPIO.output(mtr_dpn_en_l , GPIO.LOW)
    
def kiri():
    GPIO.output(mtr_dpn_en_r , GPIO.HIGH)  
    GPIO.output(mtr_dpn_en_l , GPIO.LOW) 
    print ("kiri")
    flag_encoder_kiri = 1
    sleep(0.25)
    GPIO.output(mtr_dpn_en_r , GPIO.LOW)  
    GPIO.output(mtr_dpn_en_l , GPIO.LOW)

def mundur():
    GPIO.output(mtr_blkg_en_r , GPIO.HIGH)  
    GPIO.output(mtr_blkg_en_l , GPIO.LOW) 
    print ("mundur")
    sleep(0.05)
    
def maju():
    p_maju=subprocess.Popen(["python3", "/home/pi/Robot_19/kontrol_motor_maju.py"], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p_maju.communicate()
    print(stdout)
    
def diam():
    GPIO.output(mtr_blkg_en_r , GPIO.LOW)  
    GPIO.output(mtr_blkg_en_l , GPIO.LOW)
    GPIO.output(mtr_dpn_en_r , GPIO.LOW)  
    GPIO.output(mtr_dpn_en_l , GPIO.LOW)
    print ("Berhenti")

def buka_pintu():
    from ircodec.command import CommandSet
    controller = CommandSet.load('Ardoor.json')
    time.sleep (1)
    controller.emit('Trigger')
    print ('Sinyal terkirim')

#---------------------------Kode Awal---------------------------#

ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", type=str, default="barcodes.csv",
    help="path to output CSV file containing barcodes")
args = vars(ap.parse_args())

# start video stream
vs = VideoStream(src=1).start()

print("[INFO] starting video stream...")

# waktu bagi kamera untuk melakukan "pemanasan"
sleep(2.0)

status_jalan = "diam"

# warna
aman = (0, 255, 0)
bahaya = (0, 0, 255)
peringatan = (0, 255, 255)

us_d_tengah = aman
us_d_kanan = aman
us_d_kiri = aman

us_b_tengah = aman
us_b_kanan = aman
us_b_kiri = aman

default_num = 10000

us_kiri_dpn = default_num
us_tengah_dpn = default_num
us_kanan_dpn = default_num

us_kiri_blk = default_num
us_tengah_blk = default_num
us_kanan_blk = default_num

width_status_frame = 400
height_status_frame = 300
#---------------------------Operation Code---------------------------#

# mengitung waktu untuk membaca serial arduino
counter_us_dpn = 0
while(True):
    
    # Membaca kamera
    # mengambil frame
    frame = vs.read()
    camera_only_frame = imutils.resize(frame, width = 600)
    
    # resize
    frame = imutils.resize(frame, width=800)
        
    # Membaca us sensor dan status
    if counter_us_dpn == 25:
        # depan
        ser_depan = serial.Serial('/dev/ttyUSB1',9600)
        
        # belakang
        ser_belakang = serial.Serial('/dev/ttyUSB0',9600)
        
        read_depan=ser_depan.readline()
        read_belakang = ser_belakang.readline()
        
        datasplit_depan = read_depan.decode('utf-8', 'ignore').strip('\r\n').strip().split(',')
        datasplit_belakang = read_belakang.decode('utf-8', 'ignore').strip('\r\n').strip().split(',')

        # pemisahan data:
        # banyak data (harusnya 3, tapi terkadang hanya 2 atau 1)
        # us_depan
        if len(datasplit_depan) == 3:
            if datasplit_depan[0] != '':
                us_kiri_dpn = int(datasplit_depan[0])
            if datasplit_depan[0] == '':
                us_kiri_dpn = default_num
            if datasplit_depan[1] !='':
                us_tengah_dpn = int(datasplit_depan[1])
            if datasplit_depan[1] =='':
                us_tengah_dpn = default_num
            if datasplit_depan[2] !='':
                us_kanan_dpn = int(datasplit_depan[2])
            if datasplit_depan[2] == '':
                us_kanan_dpn = default_num
                
        if len(datasplit_depan) == 2:
            if datasplit_depan[0] != '':
                us_kiri_dpn = int(datasplit_depan[0])
            if datasplit_depan[0] == '':
                us_kiri_dpn = default_num
            if datasplit_depan[1] !='':
                us_tengah_dpn = int(datasplit_depan[1])
            if datasplit_depan[1] =='':
                us_tengah_dpn = default_num
        
        if len(datasplit_depan) == 1:
            if datasplit_depan[0] != '':
                us_kiri_dpn = int(datasplit_depan[0])
            if datasplit_depan[0] == '':
                us_kiri_dpn = default_num
                
        if len(datasplit_depan) == 0:
            us_kiri_dpn = default_num
            us_tengah_dpn = default_num
            us_kanan_dpn = default_num

        # us_belakang
        if len(datasplit_belakang) == 3:
            if datasplit_belakang[0] != '':
                us_kiri_blk = int(datasplit_belakang[0])
            if datasplit_belakang[0] == '':
                us_kiri_blk = default_num
            if datasplit_belakang[1] !='':
                us_tengah_blk = int(datasplit_belakang[1])
            if datasplit_belakang[1] =='':
                us_tengah_blk = default_num
            if datasplit_belakang[2] !='':
                us_kanan_blk = int(datasplit_belakang[2])
            if datasplit_belakang[2] == '':
                us_kanan_blk = default_num
                
        if len(datasplit_belakang) == 2:
            if datasplit_belakang[0] != '':
                us_kiri_blk = int(datasplit_belakang[0])
            if datasplit_belakang[0] == '':
                us_kiri_blk = default_num
            if datasplit_belakang[1] !='':
                us_tengah_blk = int(datasplit_belakang[1])
            if datasplit_belakang[1] =='':
                us_tengah_blk = default_num
        
        if len(datasplit_belakang) == 1:
            if datasplit_belakang[0] != '':
                us_kiri_blk = int(datasplit_belakang[0])
            if datasplit_belakang[0] == '':
                us_kiri_blk = default_num
                
        if len(datasplit_belakang) == 0:
            us_kiri_blk = default_num
            us_tengah_blk = default_num
            us_kanan_blk = default_num
            
            
        # Kondisi di layar
        # us_depan
        if us_tengah_dpn <= 50:
            us_d_tengah = bahaya
        if us_tengah_dpn > 50:
            us_d_tengah = aman
        if us_kanan_dpn <= 30:
            us_d_kanan = bahaya
        if us_kanan_dpn > 30:
            us_d_kanan = aman
        if us_kiri_dpn <=30:
            us_d_kiri = bahaya
        if us_kiri_dpn > 30:
            us_d_kiri = aman

        # us_belakang
        if us_tengah_blk <= 50:
            us_b_tengah = bahaya
        if us_tengah_blk > 50:
            us_b_tengah = aman
        if us_kanan_blk <= 30:
            us_b_kanan = bahaya
        if us_kanan_blk > 30:
            us_b_kanan = aman
        if us_kiri_blk <=30:
            us_b_kiri = bahaya
        if us_kiri_blk > 30:
            us_b_kiri = aman
            
            
        if us_tengah_dpn <= 50:
        #or us_tengah_blk <= 50
            diam()
            status_jalan = "berhenti"

        # reset counter
        counter_us_dpn = 0

    # status_us_depan
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.rectangle(frame,(0, 0),(300, 10),us_d_kiri,20)
    cv2.rectangle(frame,(500, 0),(800, 10),us_d_kanan,20)
    cv2.rectangle(frame,(400-150, 0),(400+150, 20),us_d_tengah,30)
    cv2.putText(frame,'{}'.format(us_kiri_dpn),(50,15), font, 0.6,(255,255,255),2,cv2.LINE_AA)
    cv2.putText(frame,'{}'.format(us_tengah_dpn),(385,15), font, 0.6,(255,255,255),2,cv2.LINE_AA)
    cv2.putText(frame,'{}'.format(us_kanan_dpn),(700,15), font, 0.6,(255,255,255),2,cv2.LINE_AA)

    # status_us_belakang
    cv2.rectangle(frame,(0, 590),(300, 600),us_b_kiri,20)
    cv2.rectangle(frame,(500, 590),(800, 600),us_b_kanan,20)
    cv2.rectangle(frame,(400-150, 580),(400+150, 600),us_b_tengah,30)
    cv2.putText(frame,'{}'.format(us_kiri_blk),(50,595), font, 0.6,(255,255,255),2,cv2.LINE_AA)
    cv2.putText(frame,'{}'.format(us_tengah_blk),(385,585), font, 0.6,(255,255,255),2,cv2.LINE_AA)
    cv2.putText(frame,'{}'.format(us_kanan_blk),(700,595), font, 0.6,(255,255,255),2,cv2.LINE_AA)
    
    cv2.putText(frame,'Robot {}'.format(status_jalan),(10,50), font, 0.6,(255,255,255),1,cv2.LINE_AA)
    
    # info tab
    cv2.putText(camera_only_frame,'W ~ maju',(10,600-150), font, 0.6,(255,255,255),1,cv2.LINE_AA)
    cv2.putText(camera_only_frame,'S ~ mundur',(10,600 - 130), font, 0.6,(255,255,255),1,cv2.LINE_AA)
    cv2.putText(camera_only_frame,'A ~ belok kiri',(10,600 - 110), font, 0.6,(255,255,255),1,cv2.LINE_AA)
    cv2.putText(camera_only_frame,'D ~ belok kanan',(10, 600 - 90), font, 0.6,(255,255,255),1,cv2.LINE_AA)
    cv2.putText(camera_only_frame,'X ~ berhenti',(10, 600 - 70), font, 0.6,(255,255,255),1,cv2.LINE_AA)
    cv2.putText(camera_only_frame,'O ~ kamera kiri',(10, 600 - 50), font, 0.6,(255,255,255),1,cv2.LINE_AA)
    cv2.putText(camera_only_frame,'P ~ kamera kanan',(10, 600 - 30), font, 0.6,(255,255,255),1,cv2.LINE_AA)

    cv2.putText(frame,'{}'.format(counter_us_dpn),(775,50), font, 0.5,(255,255,255),1,cv2.LINE_AA)

    # show image
    # Frame asli
    #cv2.imshow("Frame", frame)
    
    # hanya tangkapan kamera
    cv2.imshow("Kamera", camera_only_frame)
    
    # Pengecilan 2x dari "Frame asli"
    status_frame = imutils.resize(frame, width=width_status_frame)
    cv2.imshow("Status", status_frame)
    
    # menambah counter
    counter_us_dpn = counter_us_dpn+1

    key = cv2.waitKey(1) & 0xFF
    if key == ord("w"):
        maju()
        status_jalan = "maju"
    if key == ord("s"):
        mundur()
        status_jalan = "mundur"
    if key == ord("d"):
        kanan()                        
    if key == ord("a"):
        kiri()
    if key == ord("x"):
        diam()
        status_jalan = "berhenti"

    if key == ord("o"):
        p.ChangeDutyCycle(5)
        time.sleep(0.05)
        p.ChangeDutyCycle(0)
        
    if key == ord("p"):
        p.ChangeDutyCycle(10)
        time.sleep(0.05)
        p.ChangeDutyCycle(0)
        
    if key == ord("m"): #buka pintu
        #buka_pintu()
        p=subprocess.Popen(["python3", "/home/pi/Robot_19/IR_Transmit.py"], stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate()
        print(stdout)
                
    if key == ord("q"):
        break

print("[INFO] cleaning up...")
cv2.destroyAllWindows()
vs.stop()

