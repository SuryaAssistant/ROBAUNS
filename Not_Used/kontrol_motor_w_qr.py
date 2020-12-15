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
import math
#for datetime for US sensorw
import datetime
#for OpenCV
import cv2

#sizing map
skala = 1/100 # 1 pixel = 30cm

panjang_asli =74400
lebar_asli =24000

panjang_map = panjang_asli*skala
lebar_map = lebar_asli*skala

panjang_map = np.round(panjang_map).astype("int")
lebar_map = np.round(lebar_map).astype("int")

# initial position on screen
x_robot = (10/100)*panjang_map
y_robot = (20/100)*lebar_map

x_robot = np.round(x_robot).astype("int")
y_robot = np.round(y_robot).astype("int")

# setting sudut
sudut_putar = 0


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#-----------------------------Pin Config-----------------------------#

#--------------Motor Belakang--------------#

mtr_blkg_en_r = 16
mtr_blkg_en_l = 19
putih_blk = 17
kuning_blk = 27

GPIO.setup(mtr_blkg_en_r , GPIO.OUT) #EN_R
GPIO.setup(mtr_blkg_en_l , GPIO.OUT) #EN_L
GPIO.setup(putih_blk , GPIO.OUT)
GPIO.setup(kuning_blk, GPIO.OUT)

# Set pin awal "LOW"
GPIO.setup(mtr_blkg_en_r , GPIO.LOW) #EN_R
GPIO.setup(mtr_blkg_en_l , GPIO.LOW) #EN_L
GPIO.setup(putih_blk , GPIO.LOW)
GPIO.setup(kuning_blk, GPIO.LOW)
#---------------Motor Depan_---------------#

mtr_dpn_en_r = 20
mtr_dpn_en_l = 26

GPIO.setup(mtr_dpn_en_r , GPIO.OUT) #EN_R
GPIO.setup(mtr_dpn_en_l , GPIO.OUT) #EN_L

# Set pin awal "LOW"
GPIO.setup(mtr_dpn_en_r , GPIO.LOW) #EN_R
GPIO.setup(mtr_dpn_en_l , GPIO.LOW) #EN_L

#------------Sensor Ultrasonik-------------#

us_depan_TRIGGER = 13
us_depan_ECHO = 6

print("Loading...")
sleep(1.00)

print("Start")

#------------------------------Function------------------------------#

# def us_depan():
#     GPIO.setup(us_depan_TRIGGER, GPIO.OUT)
#     GPIO.setup(us_depan_ECHO, GPIO.IN)
#     
#     GPIO.output(us_depan_TRIGGER, GPIO.LOW)
#     
#     GPIO.output(us_depan_TRIGGER, GPIO.HIGH)
#     sleep(0.00001)
# 
#     GPIO.output(us_depan_TRIGGER, GPIO.LOW)
# 
#     pulse_start_time = 0
#     pulse_end_time = 0
#     pulse_duration = 0
# 
#     while GPIO.input(us_depan_ECHO)==0:
#         pulse_start_time = time.time()
#         
#     while GPIO.input(us_depan_ECHO)==1:
#         pulse_end_time = time.time()
# 
#     pulse_duration = pulse_end_time - pulse_start_time
#     distance = round(pulse_duration * 17150, 2)
#     print("Jarak_depan:",distance,"cm")
      
def kanan():
    GPIO.output(mtr_dpn_en_r , GPIO.LOW)  
    GPIO.output(mtr_dpn_en_l , GPIO.HIGH) 
    print ("kanan")
    sleep(0.25)
    GPIO.output(mtr_dpn_en_r , GPIO.LOW)  
    GPIO.output(mtr_dpn_en_l , GPIO.LOW)
    
def kiri():
    GPIO.output(mtr_dpn_en_r , GPIO.HIGH)  
    GPIO.output(mtr_dpn_en_l , GPIO.LOW) 
    print ("kiri")
    sleep(0.25)
    GPIO.output(mtr_dpn_en_r , GPIO.LOW)  
    GPIO.output(mtr_dpn_en_l , GPIO.LOW)

def mundur():
    GPIO.setup(putih_blk , GPIO.LOW)
    GPIO.setup(kuning_blk, GPIO.HIGH)
    GPIO.output(mtr_blkg_en_r , GPIO.HIGH)  
    GPIO.output(mtr_blkg_en_l , GPIO.LOW) 
    print ("mundur")
    sleep(0.5)
    
#    GPIO.output(mtr_blkg_en_r , GPIO.LOW)  
#    GPIO.output(mtr_blkg_en_l , GPIO.LOW)
    
def maju():
    GPIO.setup(putih_blk , GPIO.HIGH)
    GPIO.setup(kuning_blk, GPIO.LOW)
    GPIO.output(mtr_blkg_en_r , GPIO.LOW)  
    GPIO.output(mtr_blkg_en_l , GPIO.HIGH) 
    print ("maju")
    sleep(0.5)
#    GPIO.output(mtr_blkg_en_r , GPIO.LOW)  
#    GPIO.output(mtr_blkg_en_l , GPIO.LOW)
    
def diam():
    GPIO.output(mtr_blkg_en_r , GPIO.LOW)  
    GPIO.output(mtr_blkg_en_l , GPIO.LOW)
    GPIO.output(mtr_dpn_en_r , GPIO.LOW)  
    GPIO.output(mtr_dpn_en_l , GPIO.LOW)
    print ("Berhenti")
    
#---------------------------Kode Awal---------------------------#

ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", type=str, default="barcodes.csv",
    help="path to output CSV file containing barcodes")
args = vars(ap.parse_args())

# start video stream
vs = VideoStream(1).start()

print("[INFO] starting video stream...")

# waktu bagi kamera untuk melakukan "pemanasan"
sleep(2.0)

#---------------------------Operation Code---------------------------#

while(True):
    # Gambar Denah
    
    # Create a black image
    img = np.zeros((panjang_map,panjang_map,3), np.uint8)
    # Draw a box 
    cv2.rectangle(img,(0,0),(panjang_map,lebar_map),(255,0,0),3)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img,'Denah Ruangan',(10,20), font, 0.5,(255,255,255),2,cv2.LINE_AA)
    # Robot icon position
    cv2.rectangle(img,(x_robot, y_robot),(x_robot+5, y_robot+5),(255,0,0),2)
    # Angle box
    cv2.rectangle(img,(0,lebar_map),(150,lebar_map+150),(0,255,0),3)
    cv2.putText(img,'Arah',(10,lebar_map+20), font, 0.5,(255,255,255),2,cv2.LINE_AA)
    cv2.putText(img,"Sudut Motor {}".format(sudut_putar), (10, lebar_map+40),font, 0.5, (255,255,255), 2, cv2.LINE_AA)

    #map
    
    cv2.rectangle(img,(np.round(0*skala).astype("int"),lebar_map),(np.round(4800*skala).astype("int"),np.round(7200*skala).astype("int")),(0,255,0),3)

    # Membaca kamera
    # mengambil frame
    frame = vs.read()

    # resize
    frame = imutils.resize(frame, width=400)

    # find the barcodes in the frame and decode each of the barcodes
    barcodes = pyzbar.decode(frame)

    # loop over the detected barcodes
    
    for barcode in barcodes:
        # extract the bounding box location of the barcode and draw
        # the bounding box surrounding the barcode on the image
        (x, y, w, h) = barcode.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # the barcode data is a bytes object so if we want to draw it
        # on our output image we need to convert it to a string first
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type
        # draw the barcode data and barcode type on the image
        text = "{} ({})".format(barcodeData, barcodeType)
        cv2.putText(frame, text, (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        # if the barcode text is currently not in our CSV file, write
        # the timestamp + barcode to disk and update the set
        # print posisi
        cv2.putText(frame, "Pos: ({0}, {1})".format(x, y), (x, y + h + 30),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        if barcodeData == 'A':
        #    if x > 205:
        #        kanan()
        #        maju()
        #    if x < 195:
        #        kiri()
        #        maju()
        #    if 195 <= x and x <=205:
        #        diam()
            print('Found')

    # show image
    cv2.imshow("Frame", frame)
    cv2.imshow("Map", img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("w"):
        maju()
    if key == ord("s"):
        mundur()
    if key == ord("d"):
        kanan()
    if key == ord("a"):
        kiri()
    if key == ord("x"):
        diam()
    if key == ord("q"):
        break

print("[INFO] cleaning up...")
cv2.destroyAllWindows()
vs.stop()