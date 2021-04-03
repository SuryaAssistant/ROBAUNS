#! /usr/bin/python3

#----------------------------------------------Import Library(s)----------------------------------------------#

from __future__ import print_function
import sys
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

import serial

#------------------------------------------End of Import  Library(s)------------------------------------------#
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

print("Sedang Memuat...")
sleep(1.00)

print("Mulai")

#-----------------------------------------------Serial Protocol-----------------------------------------------#
# kode status perintah raspi

# 1 = motor belakang maju
# 2 = motor belakang mundur
# 3 = motor belakang diam

# 4 = motor depan kanan
# 5 = motor depan kiri
# 6 = motor depan diam

# 11 = kamera ke kanan x derajat
# 10 = kamera ke kiri x derajat
# 12 = kamera ke tengah
# 13 = kamera diam

# default code
kode_motor_belakang = 3
kode_motor_depan = 6
kode_kamera = 13
#-------------------------------------------End of Serial Protocol-------------------------------------------#


#-----------------------------------------------Local Function-----------------------------------------------#
def belakang_maju():
    global kode_motor_belakang
    kode_motor_belakang = 1

def belakang_mundur():
    global kode_motor_belakang
    kode_motor_belakang = 2

def belakang_diam():
    global kode_motor_belakang
    kode_motor_belakang = 3

def depan_kanan():
    global kode_motor_depan
    kode_motor_depan = 4

def depan_kiri():
    global kode_motor_depan
    kode_motor_depan = 5

def depan_diam():
    global kode_motor_depan
    kode_motor_depan = 6

def kamera_kanan():
    global kode_kamera
    kode_kamera = 11

def kamera_kiri():
    global kode_kamera
    kode_kamera = 10

def kamera_tengah():
    global kode_kamera
    kode_kamera = 12

def kamera_diam():
    global kode_kamera
    kode_kamera = 13

def buka_pintu():
    subprocess.Popen(["python3", "/home/pi/RoboCov19UNS/IR_Transmit.py"], stdout=PIPE, stderr=PIPE)

# detect arduino port posistion in raspberry pi
def detect_usb(port_number, pesan):
    global decode_usb
    
    with serial.Serial("/dev/ttyUSB{}".format(port_number), 9600, timeout=1) as detect_USB:
        time.sleep(0.25) #wait serial to open
        print("Check USB{}".format(detect_USB.port))

        if detect_USB.isOpen():
            print("{} terkoneksi!".format(detect_USB.port))
            
            check_port_cmd = pesan
            check_cmd = ("{}\n".format(check_port_cmd))
            time.sleep(3)
            detect_USB.flushInput()
            detect_USB.write(check_cmd.encode('utf-8'))
        
            while detect_USB.inWaiting()==0: pass
            if detect_USB.inWaiting():
                answer=detect_USB.readline()
                decode_usb = answer.decode('utf-8').rstrip()
                detect_USB.flushInput()
        else:
            print("{} tidak terhubung!".format(detect_USB.port))
            
# send command to start or stop serial port
def set_usb(stop_or_start):
    if(stop_or_start == "stop"):
        stat = 0
    if(stop_or_start == "start"):
        stat = 1
    f_stop = open("stop_file.txt","w")
    f_stop.write("{} ".format(stat)) 
    f_stop.close()
#-------------------------------------------End of Local Function-------------------------------------------#


#-------------------------------------------Detect Arduino in USB-------------------------------------------#
#
# Simple explanation of how it works
#
#                      ---------------------                           ---------------
#                      |   Raspberry Pi    |                           |   Arduino   |
#                      ---------------------                           ---------------
#                                           
# Step 1 (Checking):       Send "check"           ----USBx---->        
# Step 2           :                                                    Get "check"
# Step 3 (ACK)     :                              <---ANSWER---  Send "main"/"depan"/"belakang"
# Step 4           :       Get "main"
# Step 5           :   Arduino main on USBx
# Step 6 (Finish)  :      Send "done"             ----DONE---->           
# Step 7           :                                                    Get "done"
#


# number of Arduino that connect to Raspberry Pi
total_usb = 3

# message comand
cek = "check"
selesai = "done"

port_0 = 0
port_1 = 0
port_2 = 0

# default reply from Arduino
code_usb= ["default","default","default"]

# set port number to prevent "unread USBx"
# if port number == USB4, this mean raspi can't recognize
# the arduino
arduino_main_port = 4
arduino_depan_port = 4
arduino_belakang_port = 4

times_usb = 0
# detect USBPort
print("\nCek kelengkapan perangkat...\n")
for x in range(total_usb):
    detect_usb(x, cek)

    while True:
        if str(decode_usb) == "main" or str(decode_usb) == "depan" or str(decode_usb) == "belakang":
            print ("USB{} berhasil dikenali".format(x))

            # send "end" message
            with serial.Serial("/dev/ttyUSB{}".format(x), 9600, timeout=1) as detect_USB:
                time.sleep(0.25)

                if detect_USB.isOpen():                    
                    check_port_cmd = "done"
                    check_cmd = ("{}\n".format(check_port_cmd))
                    time.sleep(3)
                    detect_USB.flushInput()
                    detect_USB.write(check_cmd.encode('utf-8'))
                    print ("\n-----Checking USB{} berhasil-----\n".format(x))
                    time.sleep(0.25)

            code_usb = decode_usb

            # determine usb port
            if code_usb == "main" :
                arduino_main_port = x
            if code_usb == "depan" :
                arduino_depan_port = x
            if code_usb =="belakang" :
                arduino_belakang_port = x
                
            # set port status
            if x == 0:
                port_0 = 1
            if x == 1:
                port_1 = 1
            if x == 2:
                port_2 = 1
                
            break

        else:
            detect_usb(x, cek)
            times_usb += 1
            if times_usb == 5:
                times_usb = 0
                print ("\n-----Checking USB{} gagal-----\n".format(x))
                break
            
# if there are two arduino detected
if arduino_main_port == 4:
    if port_0 == 1 and port_1 == 1:
        arduino_main_port = 2
    elif port_0 == 1 and port_2 == 1:
        arduino_main_port = 1
    elif port_1 == 1 and port_2 == 1:
        arduino_main_port = 0
        
if arduino_depan_port == 4:
    if port_0 == 1 and port_1 == 1:
        arduino_depan_port = 2
    elif port_0 == 1 and port_2 == 1:
        arduino_depan_port = 1
    elif port_1 == 1 and port_2 == 1:
        arduino_depan_port = 0
    
if arduino_belakang_port == 4:
    if port_0 == 1 and port_1 == 1:
        arduino_belakang_port = 2
    elif port_0 == 1 and port_2 == 1:
        arduino_belakang_port = 1
    elif port_1 == 1 and port_2 == 1:
        arduino_belakang_port = 0

# print the result
print("\narduino main port USB{}".format(arduino_main_port))
print("arduino sensor depan port USB{}".format(arduino_depan_port))
print("arduino sensor belakang port USB{}".format(arduino_belakang_port))

# save usb port to usb_port_config.txt
print("Menyimpan konfigurasi")

f = open("usb_port_config.txt","w")
f.write("%d \r\n" %arduino_main_port) #port_arduino_main
f.write("%d \r\n" %arduino_depan_port) #port_arduino_depan
f.write("%d \r\n" %arduino_belakang_port) #port arduino_belakang
f.close()

print("Konfigurasi berhasil disimpan")

# start serial port
set_usb("start")

#-----------------------------------------End Detect Arduino in USB-------------------------------------------#

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


#data serial awal
data_depan = [0, 0, default_num, default_num, default_num]
data_belakang = [default_num, default_num, default_num]

#---------------------------Operation Code---------------------------#

# set counter_serial = 0 untuk reset counter pembacaan serial
counter_serial = 0

# pemanggilan serial
subprocess.Popen(["python3", "/home/pi/RoboCov19UNS/serial_arduino_depan.py"], stdout=PIPE, stderr=PIPE)
subprocess.Popen(["python3", "/home/pi/RoboCov19UNS/serial_arduino_belakang.py"], stdout=PIPE, stderr=PIPE)

# send and receive data to main arduino
ser_main = serial.Serial(
   port='/dev/ttyUSB{}'.format(arduino_main_port),
   baudrate = 9600,
   parity=serial.PARITY_NONE,
   stopbits=serial.STOPBITS_ONE,
   bytesize=serial.EIGHTBITS,
   timeout=1
)
ser_main.flush()

while(True):

    # Membaca kamera
    # mengambil frame
    frame = vs.read() #gambar asli
    
    # resize the camera read to make processing faster
    frame = imutils.resize(frame, width=600)
    
    # resize processed frame into big scale
    camera_only_frame = imutils.resize(frame, width = width_camera_only)


    # Send kontrol command code to Arduino
    # Format --> example: "11413"
    #        1             1               4          13
    # [active_status] [back_motor] [steering_motor] [camera]
    # 
    # if active_status == 1, Arduino execute command code
    # if active_status == 0, Arduino ignore the other command. It used when the robot accidently disconnected
    #  
    kode_enkripsi = 10000+(kode_motor_belakang*1000)+(kode_motor_depan*100)+(kode_kamera)
    string_kode = str(kode_enkripsi)
    send_string = ("{}\n".format(string_kode))
    ser_main.write(send_string.encode('utf-8'))
    
    #set to default
    kode_motor_depan = 6
    kode_kamera = 13
    
    #print(send_string.encode('utf-8'))


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
            j = 3 - k

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
            us_kiri_dpn = data_depan[0]
            us_tengah_dpn = data_depan[1]
            us_kanan_dpn = data_depan[2]
                        
        with open("/home/pi/RoboCov19UNS/data_serial_belakang.txt", "r", encoding = "utf-8") as h:
            data_serial_belakang = list(map(int, h.readlines()))
            # pemisahan data:
            m = len(data_serial_belakang)

            #detectq and correction if data can't read
            #read data depan = m
            #non-read data depan = n
            n = 3 - m

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
            us_kiri_blk = data_belakang[0]
            us_tengah_blk = data_belakang[1]
            us_kanan_blk = data_belakang[2]
        
        # reset counter
        counter_serial = 0
        
    # menambah counter
    counter_serial += 1

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
            belakang_diam()
            status_robot = "diam"
        
    if status_robot == "mundur":
        if us_tengah_blk <= 50 :
            belakang_diam()
            status_robot = "diam"

    font = cv2.FONT_HERSHEY_SIMPLEX

    # info tab
    cv2.putText(camera_only_frame,'W ~ Maju',(10,height_camera_only-130), font, 0.6,(255,255,255),1,cv2.LINE_AA)
    cv2.putText(camera_only_frame,'S ~ Mundur',(10,height_camera_only - 110), font, 0.6,(255,255,255),1,cv2.LINE_AA)
    cv2.putText(camera_only_frame,'A ~ Belok kiri',(10,height_camera_only - 90), font, 0.6,(255,255,255),1,cv2.LINE_AA)
    cv2.putText(camera_only_frame,'D ~ Belok kanan',(10, height_camera_only - 70), font, 0.6,(255,255,255),1,cv2.LINE_AA)
    cv2.putText(camera_only_frame,'O ~ Kamera kiri',(10, height_camera_only - 50), font, 0.6,(255,255,255),1,cv2.LINE_AA)
    cv2.putText(camera_only_frame,'P ~ Kamera kanan',(10, height_camera_only - 30), font, 0.6,(255,255,255),1,cv2.LINE_AA)
    cv2.putText(camera_only_frame,'Q ~ Exit',(10, height_camera_only - 10), font, 0.6,(255,255,255),1,cv2.LINE_AA)

    cv2.putText(camera_only_frame,'M ~ Buka pintu',(width_camera_only-155, height_camera_only-30), font, 0.6,(255,255,255),1,cv2.LINE_AA)
    cv2.putText(camera_only_frame,'{}'.format(datetime.datetime.now()),(width_camera_only - 222, height_camera_only -10), font, 0.6,(255,255,255),1,cv2.LINE_AA)

    cv2.putText(camera_only_frame,'{}'.format(string_kode),(width_camera_only-70, 30), font, 0.4,(255,255,255),1,cv2.LINE_AA)

    # show image
    # Frame asli
    #cv2.imshow("Frame Asli", frame)
    
    # hanya tangkapan kamera
    cv2.imshow("Kamera_view", camera_only_frame)

    # baca keyboard
    # when use raspi, use cv2.waitKey(1) instead of cv2.waitKeyEx(1)
    key = cv2.waitKey(1) & 0xFF

    # if the 'q' key is pressed, stop the loop
    # key up = 65362 --> 'R' 82
    # key down = 65634 --> 'T' 84
    # key right = 65363 --> 'S' 83
    # key left = 65361 --> 'Q' 81
        
    if key == ord("w") or key == 65362 or key == 82:
        belakang_maju()
        status_robot = "maju"
        #print("UP")
    elif key == ord("s") or key == 65634 or key == 84:
        belakang_mundur()
        status_robot = "mundur"
        #print("DOWN")
    elif key == ord("d") or key == 65363 or key == 83:
        depan_kanan()
        #print("RIGHT")
    elif key == ord("a") or key == 65361 or key == 81:
        depan_kiri()
        #print("LEFT")        
    elif key == ord("x") or key == ord(" "):
        belakang_diam()
        status_robot = "diam"
        
    #-----------kamera--------------------
    elif key == ord("o"):
        kamera_kiri()  
    elif key == ord("p"):
        kamera_kanan()
    elif key == ord("1"):
        kamera_tengah()
    elif key == ord("0"):
        kamera_diam()
    #-----------end of kamera---------------
        
    elif key == ord("m"): #buka pintu
        buka_pintu()
    elif key == ord("q"):
        # stop serial port
        set_usb("stop")
        ser_main.close()
        print("\n -------Serial port dinonaktifkan-------")
        break
 
    else:
        belakang_diam()
        depan_diam()
        kamera_diam()

print("Menutup Aplikasi ...")

cv2.destroyAllWindows()
vs.stop()
sys.exit()
