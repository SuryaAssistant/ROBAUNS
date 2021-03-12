#! /usr/bin/python3

#----------------------------------------------Import Library(s)----------------------------------------------#

from __future__ import print_function
#for Videostream
import imutils
from imutils.video import VideoStream
from imutils.video import WebcamVideoStream
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
#for call other script in 'background'
import subprocess
from subprocess import Popen, PIPE
#get time
import datetime

#------------------------------------------End of Import  Library(s)------------------------------------------#

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


print("Loading...")
sleep(1.00)

print("Start")


#-----------------------------------------------Serial Protocol-----------------------------------------------#

# kode status perintah raspi
# 10 = motor belakang maju
# 20 = motor belakang mundur
# 30 = motor belakang diam

# 40 = motor depan kanan
# 50 = motor depan kiri
# 60 = motor depan diam

# 70 = kamera ke kanan 30 derajat
# 80 = kamera ke kiri 30 derajat
# 90 = kamera ke tengah
# 100 = kamera diam

# default code
kode_motor_belakang = 30
kode_motor_depan = 60
kode_kamera = 100

#-------------------------------------------End of Serial Protocol-------------------------------------------#

#-----------------------------------------------Local Function-----------------------------------------------#

def belakang_maju():
    kode_motor_belakang = 10

def belakang_mundur():
    kode_motor_belakang = 20

def belakang_diam():
    kode_motor_belakang = 30

def depan_kanan():
    kode_motor_depan = 40

def depan_kiri():
    kode_motor_depan = 50

def depan_diam():
    kode_motor_depan = 60

def kamera_kanan():
    kode_kamera = 70

def kamera_kiri():
    kode_kamera = 80

def kamera_tengah():
    kode_kamera = 90

def kamera_diam():
    kode_kamera = 100

def buka_pintu():
    subprocess.Popen(["python3", "/home/pi/RoboCov19UNS/IR_Transmit.py"], stdout=PIPE, stderr=PIPE)

#-------------------------------------------End of Local Function-------------------------------------------#

status_robot = "diam"

#---------------------------Kode Awal---------------------------#

ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", type=str, default="barcodes.csv",
    help="path to output CSV file containing barcodes")
args = vars(ap.parse_args())

# start video stream
vs = WebcamVideoStream(src=0).start()
#vs = cv2.VideoCapture(1)
print("Mengaktifkan kamera ...")

# waktu bagi kamera untuk melakukan "pemanasan"
sleep(2.0)

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

#encoder_dpn = 0

width_camera_only = 700
height_camera_only = int((width_camera_only/1280)*720)

width_camera_status = 600

width_camera_copy = 800
height_camera_copy = int((width_camera_copy/1280)*720)

#data serial awal
data_depan = [0, 0, default_num, default_num, default_num]
data_belakang = [default_num, default_num, default_num]
data_main = [kode_motor_belakang, kode_motor_depan, kode_kamera]


#---------------------------Operation Code---------------------------#

# set counter_serial = 0 untuk reset counter pembacaan serial
counter_serial = 0


# pemanggilan serial
subprocess.Popen(["python3", "/home/pi/RoboCov19UNS/serial_arduino_depan.py"], stdout=PIPE, stderr=PIPE)
subprocess.Popen(["python3", "/home/pi/RoboCov19UNS/serial_arduino_belakang.py"], stdout=PIPE, stderr=PIPE)
subprocess.Popen(["python3", "/home/pi/RoboCov19UNS/serial_arduino_main.py"], stdout=PIPE, stderr=PIPE)

while(True):

    # Membaca kamera
    # mengambil frame
    frame = vs.read() #gambar asli
    
    # resize for real frame (detection)
    frame = imutils.resize(frame, width=600)
    
    # resize from real
    # for camera_copy (800p)
    frame_copy = imutils.resize(frame, width = width_camera_copy)
    #for camera_only (7000)
    camera_only_frame = imutils.resize(frame, width = width_camera_only)


    # panggil serial setiap counter = 5
    if counter_serial == 5:            
        # read stored variable value in data_serial_depan.txt
        with open("/home/pi/RoboCov19UNS/data_serial_depan.txt", "r",encoding="utf-8") as g:
            data_serial_depan = list(map(int, g.readlines()))
            # pemisahan data:
            k = len(data_serial_depan)

            #detect and correction if data can't read
            #read data depan = k
            #non-read data depan = j
            j = 5 - k

            #print read data with their value
            for i in range(k):
                if data_serial_depan[i] != '':
                    data_depan[i] = int (data_serial_depan[i])
                #if datasplit_arduino[i] == '':
                #    data[i] = default_num

            #print non-read data with default_num
            #for h in range(j):
            #   data[h+k] = default_num

            #print(data)
            if j != 0:
                x_enc = data_depan[0]
                enc_pos = data_depan[1]
                us_kiri_dpn = data_depan[2]
                us_tengah_dpn = data_depan[3]
                us_kanan_dpn = data_depan[4]
                        
        with open("/home/pi/RoboCov19UNS/data_serial_belakang.txt", "r", encoding = "utf-8") as h:
            data_serial_belakang = list(map(int, h.readlines()))
        
            # pemisahan data:
            m = len(data_serial_belakang)

            #detect and correction if data can't read
            #read data depan = m
            #non-read data depan = n
            n = 5 - m

            #print read data with their value
            for l in range(m):
                if data_serial_belakang[l] != '':
                    data_belakang[l] = int (data_serial_belakang[l])
                #if datasplit_arduino[l] == '':
                #    data[l] = default_num

            #print non-read data with default_num
            #for h in range(j):
            #   data[h+k] = default_num

            #print(data)
            if n != 0:
                us_kiri_blk = data_belakang[0]
                us_tengah_blk = data_belakang[1]
                us_kanan_blk = data_belakang[2]
        
        # save command to control motor and servo via serial 
        # save file and send to arduino main using main_serial
        f = open("data_serial_main.txt","w")
        f.write("%d \r\n" %kode_motor_belakang)
        f.write("%d \r\n" %kode_motor_depan)
        f.write("%d \r\n" %kode_kamera)
        f.close()

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
        

        # fungsi autostop
        # jika  robot mendeteksi benda
        if status_robot == "maju":
            if us_tengah_dpn <= 50 :
                belakang_mundur()
                status_robot = "diam"
            
        if status_robot == "mundur":
            if us_tengah_blk <= 50 :
                belakang_diam()
                status_robot = "diam"
        
        # reset counter
        counter_serial = 0

    # status_us_depan
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.rectangle(frame_copy,(0, 0),(300, 10),us_d_kiri,20)
    cv2.rectangle(frame_copy,(500, 0),(800, 10),us_d_kanan,20)
    cv2.rectangle(frame_copy,(400-150, 0),(400+150, 20),us_d_tengah,30)
    cv2.putText(frame_copy,'{}'.format(us_kiri_dpn),(50,15), font, 0.6,(255,255,255),2,cv2.LINE_AA)
    cv2.putText(frame_copy,'{}'.format(us_tengah_dpn),(385,15), font, 0.6,(255,255,255),2,cv2.LINE_AA)
    cv2.putText(frame_copy,'{}'.format(us_kanan_dpn),(700,15), font, 0.6,(255,255,255),2,cv2.LINE_AA)

    # status_us_belakang
    cv2.rectangle(frame_copy,(0, height_camera_copy-10),(300, height_camera_copy),us_b_kiri,20)
    cv2.rectangle(frame_copy,(500, height_camera_copy-10),(800, height_camera_copy),us_b_kanan,20)
    cv2.rectangle(frame_copy,(400-150, height_camera_copy-20),(400+150, height_camera_copy),us_b_tengah,30)
    cv2.putText(frame_copy,'{}'.format(us_kiri_blk),(50,height_camera_copy-5), font, 0.6,(255,255,255),2,cv2.LINE_AA)
    cv2.putText(frame_copy,'{}'.format(us_tengah_blk),(385,height_camera_copy-15), font, 0.6,(255,255,255),2,cv2.LINE_AA)
    cv2.putText(frame_copy,'{}'.format(us_kanan_blk),(700,height_camera_copy-5), font, 0.6,(255,255,255),2,cv2.LINE_AA)
    
    cv2.putText(frame_copy,'Robot {}'.format(status_robot),(10,50), font, 0.6,(255,255,255),1,cv2.LINE_AA)
    #cv2.putText(frame_copy,'Encoder {}'.format(encoder_dpn),(10,70), font, 0.6,(255,255,255),1,cv2.LINE_AA)
    
    # info tab
    cv2.putText(camera_only_frame,'W ~ Maju',(10,height_camera_only-150), font, 0.6,(255,255,255),1,cv2.LINE_AA)
    cv2.putText(camera_only_frame,'S ~ Mundur',(10,height_camera_only - 130), font, 0.6,(255,255,255),1,cv2.LINE_AA)
    cv2.putText(camera_only_frame,'A ~ Belok kiri',(10,height_camera_only - 110), font, 0.6,(255,255,255),1,cv2.LINE_AA)
    cv2.putText(camera_only_frame,'D ~ Belok kanan',(10, height_camera_only - 90), font, 0.6,(255,255,255),1,cv2.LINE_AA)
    cv2.putText(camera_only_frame,'X ~ Berhenti',(10, height_camera_only - 70), font, 0.6,(255,255,255),1,cv2.LINE_AA)
    cv2.putText(camera_only_frame,'O ~ Kamera kiri',(10, height_camera_only - 50), font, 0.6,(255,255,255),1,cv2.LINE_AA)
    cv2.putText(camera_only_frame,'P ~ Kamera kanan',(10, height_camera_only - 30), font, 0.6,(255,255,255),1,cv2.LINE_AA)
    cv2.putText(camera_only_frame,'Q ~ Exit',(10, height_camera_only -10), font, 0.6,(255,255,255),1,cv2.LINE_AA)

    cv2.putText(camera_only_frame,'M ~ Buka pintu',(width_camera_only-155, height_camera_only-30), font, 0.6,(255,255,255),1,cv2.LINE_AA)
    cv2.putText(camera_only_frame,'{}'.format(datetime.datetime.now()),(width_camera_only - 222, height_camera_only -10), font, 0.6,(255,255,255),1,cv2.LINE_AA)

    cv2.putText(frame_copy,'{}'.format(counter_serial),(775,50), font, 0.5,(255,255,255),1,cv2.LINE_AA)

    # show image
    # Frame asli
    #cv2.imshow("Frame", frame)
    #cv2.imshow("Copy", frame_copy)
    
    # hanya tangkapan kamera
    cv2.imshow("Kamera", camera_only_frame)
    
    # Pengecilan 2x dari "Frame asli" (width=400)
    status_frame = imutils.resize(frame_copy, width=width_camera_status)
    #cv2.imshow("Status", status_frame)
    
    # menambah counter
    counter_serial = counter_serial+1

    # baca keyboard
    key = cv2.waitKey(1) & 0xFF
    if key == ord("w"):
        belakang_maju()
        status_robot = "maju"
    if key == ord("s"):
        belakang_mundur()
        status_robot = "mundur"
    if key == ord("d"):
        depan_kanan()                        
    if key == ord("a"):
        depan_kiri()
    if key == ord("x"):
        belakang_diam()
        status_robot = "diam"

    if key == ord("o"):
        kamera_kiri()
        
    if key == ord("p"):
        kamera_kanan()
        
    if key == ord("m"): #buka pintu
        buka_pintu()
                
    if key == ord("q"):
        break

print("Menutup Aplikasi ...")
cv2.destroyAllWindows()
vs.stop()

#subprocess.Popen(["pkill", "python3"], stdout=PIPE, stderr=PIPE)
