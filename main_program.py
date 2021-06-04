#! /usr/bin/python3

#----------------------------------------------Import Library(s)----------------------------------------------#

from __future__ import print_function
import sys
import os
import subprocess
import time
import datetime
import RPi.GPIO as GPIO
import serial
import numpy as np
import cv2
import imutils

from imutils.video import VideoStream
from imutils.video import WebcamVideoStream

from protocol import *
from detectusb import *
from color import *

#------------------------------------------End of Import  Library(s)------------------------------------------#
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

print("Sedang Memuat...")
time.sleep(1.00)

print("Mulai")

# Create chace folder
# to save configuration and sensor data
cache_folder = "./cache"
isExist = os.path.exists(cache_folder)
if isExist == False:
    os. makedirs(cache_folder)

#-----------------------------------------------Serial Protocol-----------------------------------------------#
# default code
kode_motor_belakang = belakang_diam()
kode_motor_depan = depan_diam()
kode_kamera = kamera_diam()
#-------------------------------------------End of Serial Protocol-------------------------------------------#


def buka_pintu():
    subprocess.Popen(["python3", "./door/IR_Transmit.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
# send command to start or stop serial port
def set_usb(stop_or_start):
    if(stop_or_start == "stop"):
        stat = 0
    if(stop_or_start == "start"):
        stat = 1
    f_stop = open("./cache/stop_file.txt","w")
    f_stop.write("{} ".format(stat)) 
    f_stop.close()
#-------------------------------------------End of Local Function-------------------------------------------#

tab_status = 0

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
detected_usb = 0
max_port = 3

# message comand
cek = "check"
selesai = "done"

# set port number to prevent "unread USBx"
# if port number == USB99, this mean raspi can't recognize
# the arduino
arduino_main_port = 99
arduino_depan_port = 99
arduino_belakang_port = 99

times_usb = 0

# Start to detect USBPort
print("\nCek kelengkapan perangkat...\n")

for x in range(max_port):
    usb_name = usb_detect(x, cek)

    while True:

        if detected_usb < total_usb:

            if str(usb_name) == "main" or str(usb_name) == "depan" or str(usb_name) == "belakang":
                print ("USB{} berhasil dikenali".format(x))

                # send "end" message
                with serial.Serial("/dev/ttyUSB{}".format(x), 9600, timeout=1) as detect_USB:
                    time.sleep(0.25)

                    if detect_USB.isOpen():                    
                        end_cmd = ("{}\n".format(selesai))
                        time.sleep(3)
                        detect_USB.flushInput()
                        detect_USB.write(end_cmd.encode('utf-8'))
                        print ("\n-----Checking USB{} berhasil-----\n".format(x))
                        time.sleep(0.25)

                # determine usb port
                if usb_name == "main" :
                    arduino_main_port = x
                if usb_name == "depan" :
                    arduino_depan_port = x
                if usb_name =="belakang" :
                    arduino_belakang_port = x
                
                detected_usb += 1

                break

            else:
                if times_usb >= 10:
                    times_usb = 0
                    print ("\n-----Checking USB{} gagal-----\n".format(x))
                    break

                if times_usb < 10:
                    times_usb += 1
                    
                    # detect usb again
                    usb_name = usb_detect(x, cek)

        if detected_usb >= total_usb:

            break

# print the result
print("\narduino main port USB{}".format(arduino_main_port))
print("arduino sensor depan port USB{}".format(arduino_depan_port))
print("arduino sensor belakang port USB{}".format(arduino_belakang_port))

# save usb port to usb_port_config.txt
print("Menyimpan konfigurasi....")

f = open("./cache/usb_port_config.txt","w")
f.write("{} \r\n" .format(arduino_main_port)) #port_arduino_main
f.write("{} \r\n" .format(arduino_depan_port)) #port_arduino_depan
f.write("{} " .format(arduino_belakang_port)) #port arduino_belakang
f.close()

print("Konfigurasi berhasil disimpan")

# start serial port
set_usb("start")

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

#-----------------------------------------End Detect Arduino in USB-------------------------------------------#

status_robot = "diam"


#---------------------------Kode Awal---------------------------#
default_num = 10000

us_kiri_dpn = default_num
us_tengah_dpn = default_num
us_kanan_dpn = default_num

us_kiri_blk = default_num
us_tengah_blk = default_num
us_kanan_blk = default_num

width_camera_only = 700
height_camera_only = int((width_camera_only/1280)*720)


#data serial awal
data_depan = [us_kiri_dpn, us_tengah_dpn, us_kanan_dpn]
data_belakang = [us_kiri_blk, us_tengah_blk, us_kanan_blk]

#---------------------------Operation Code---------------------------#

# set counter_serial = 0 untuk reset counter pembacaan serial
counter_serial = 0

# pemanggilan serial
subprocess.Popen(["python3", "./serial_arduino_depan.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
subprocess.Popen(["python3", "./serial_arduino_belakang.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

try:
    # start video stream
    vs = WebcamVideoStream(src=0).start()
    #vs = cv2.VideoCapture(1)
    print("Mengaktifkan kamera ...")

    # waktu bagi kamera untuk melakukan "pemanasan"
    time.sleep(2.0)

    while(True):

        # Membaca kamera
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
        
        string_kode = command(kode_motor_belakang, kode_motor_depan, kode_kamera)
        send_string = ("{}\n".format(string_kode))
    
        ser_main.write(send_string.encode('utf-8'))
        
        #set to default
        kode_motor_depan = depan_diam()
        kode_kamera = kamera_diam()

        # panggil serial setiap counter = 5
        if counter_serial == 5:            
            # read stored variable value in data_serial_depan.txt
            with open("./cache/data_serial_depan.txt", "r",encoding="utf-8") as g:
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
                            
            with open("./cache/data_serial_belakang.txt", "r", encoding = "utf-8") as h:
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

        # fungsi autostop
        # jika  robot mendeteksi benda
        if status_robot == "maju":
            if us_tengah_dpn <= 50 :
                kode_motor_belakang = belakang_diam()
                status_robot = "diam"
            
        if status_robot == "mundur":
            if us_tengah_blk <= 50 :
                kode_motor_belakang = belakang_diam()
                status_robot = "diam"

        font = cv2.FONT_HERSHEY_SIMPLEX

        # show indicator
        # WARNING INDICATOR
        if us_kiri_dpn <= 50 and us_kiri_dpn > 30:
            cv2.rectangle((camera_only_frame), (0,0), (30,30), color_warning(), -1)
        if us_tengah_dpn <= 50 and us_tengah_dpn > 30:
            cv2.rectangle((camera_only_frame), (int(width_camera_only/2)-15,0), (int(width_camera_only/2)+15,30), color_warning(), -1)
        if us_kanan_dpn <= 50 and us_kanan_dpn > 30:
            cv2.rectangle((camera_only_frame), (width_camera_only-30,0), (width_camera_only,30), color_warning(), -1)

        if us_kiri_blk <= 50 and us_kiri_blk > 30:
            cv2.rectangle((camera_only_frame), (0,height_camera_only), (30,height_camera_only-30), color_warning(), -1)
        if us_tengah_blk <= 50 and us_tengah_blk > 30:
            cv2.rectangle((camera_only_frame), (int(width_camera_only/2)-15,height_camera_only), (int(width_camera_only/2)+15, height_camera_only-30), color_warning(), -1)
        if us_kanan_blk <= 50 and us_kanan_blk > 30:
            cv2.rectangle((camera_only_frame), (width_camera_only-30,height_camera_only), (width_camera_only, height_camera_only-30), color_warning(), -1)

        # DANGER INDICATOR
        if us_kiri_dpn <= 30:
            cv2.rectangle((camera_only_frame), (0,0), (30,30), color_danger(), -1)
        if us_tengah_dpn <= 30:
            cv2.rectangle((camera_only_frame), (int(width_camera_only/2)-15,0), (int(width_camera_only/2)+15,30), color_danger(), -1)
        if us_kanan_dpn <= 30:
            cv2.rectangle((camera_only_frame), (width_camera_only-30,0), (width_camera_only,30), color_danger(), -1)

        if us_kiri_blk <= 30:
            cv2.rectangle((camera_only_frame), (0, height_camera_only), (30,height_camera_only-30), color_danger(), -1)
        if us_tengah_blk <= 30:
            cv2.rectangle((camera_only_frame), (int(width_camera_only/2)-15,height_camera_only), (int(width_camera_only/2)+15, height_camera_only-30), color_danger(), -1)
        if us_kanan_blk <= 30:
            cv2.rectangle((camera_only_frame), (width_camera_only-30,height_camera_only), (width_camera_only, height_camera_only-30), color_danger(), -1)

        # info tab
        if tab_status == 1:
            cv2.putText(camera_only_frame,'W ~ Maju',(10,height_camera_only-130), font, 0.6,(255,255,255),1,cv2.LINE_AA)
            cv2.putText(camera_only_frame,'S ~ Mundur',(10,height_camera_only - 110), font, 0.6,(255,255,255),1,cv2.LINE_AA)
            cv2.putText(camera_only_frame,'A ~ Belok kiri',(10,height_camera_only - 90), font, 0.6,(255,255,255),1,cv2.LINE_AA)
            cv2.putText(camera_only_frame,'D ~ Belok kanan',(10, height_camera_only - 70), font, 0.6,(255,255,255),1,cv2.LINE_AA)
            cv2.putText(camera_only_frame,'O ~ Kamera kiri',(10, height_camera_only - 50), font, 0.6,(255,255,255),1,cv2.LINE_AA)
            cv2.putText(camera_only_frame,'P ~ Kamera kanan',(10, height_camera_only - 30), font, 0.6,(255,255,255),1,cv2.LINE_AA)
            cv2.putText(camera_only_frame,'Q ~ Exit',(10, height_camera_only - 10), font, 0.6,(255,255,255),1,cv2.LINE_AA)

            cv2.putText(camera_only_frame,'M ~ Buka pintu',(width_camera_only-155, height_camera_only-30), font, 0.6,(255,255,255),1,cv2.LINE_AA)

        if tab_status == 0:
            cv2.putText(camera_only_frame,'T ~ Info tab', (10, height_camera_only - 50), font, 0.6, (255,255,255), 1, cv2.LINE_AA)

        cv2.putText(camera_only_frame,'{}'.format(datetime.datetime.now()),(width_camera_only - 222, height_camera_only -10), font, 0.6,(255,255,255),1,cv2.LINE_AA)

        cv2.putText(camera_only_frame,'{}'.format(string_kode),(width_camera_only-70, 30), font, 0.4,(255,255,255),1,cv2.LINE_AA)

        # show serial data
        cv2.putText(camera_only_frame,'{}'.format(data_depan),(10, 20), font, 0.6,(255,255,255),1,cv2.LINE_AA)
        cv2.putText(camera_only_frame,'{}'.format(data_belakang),(10, 50), font, 0.6,(255,255,255),1,cv2.LINE_AA)

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
            kode_motor_belakang = belakang_maju()
            status_robot = "maju"
            #print("UP")
        elif key == ord("s") or key == 65634 or key == 84:
            kode_motor_belakang = belakang_mundur()
            status_robot = "mundur"
            #print("DOWN")
        elif key == ord("d") or key == 65363 or key == 83:
            kode_motor_depan = depan_kanan()
            #print("RIGHT")
        elif key == ord("a") or key == 65361 or key == 81:
            kode_motor_depan = depan_kiri()
            #print("LEFT")        
        elif key == ord("x") or key == ord(" "):
            kode_motor_belakang = belakang_diam()
            status_robot = "diam"
            
        #-----------kamera--------------------
        elif key == ord("o"):
            kode_kamera = kamera_kiri()  
        elif key == ord("p"):
            kode_kamera = kamera_kanan()
        elif key == ord("1"):
            kode_kamera = kamera_tengah()
        elif key == ord("0"):
            kode_kamera = kamera_diam()
        #-----------end of kamera---------------
            
        elif key == ord("m"): #buka pintu
            buka_pintu()

        elif key == ord("q"):
            stop_string = force_stop()
            ser_main.write(stop_string.encode('utf-8'))
            # stop serial port
            set_usb("stop")
            print("\n -------Serial port dinonaktifkan-------")
            break
    
        #---------------TAB INFO----------------
        elif key == ord("t"):
            tab_status += 1
            if tab_status == 2:
                tab_status = 0

        else:
            kode_motor_belakang = belakang_diam()
            kode_motor_depan = depan_diam()
            kode_kamera = kamera_diam()

    cv2.destroyAllWindows()
    vs.stop()
    sys.exit()

except:
    stop_string = force_stop()
    ser_main.write(stop_string.encode('utf-8'))

    # stop serial port
    set_usb("stop")
    ser_main.close()

    print("\nTerjadi Error")
    print("Menutup Paksa Aplikasi ...")

    cv2.destroyAllWindows()
    vs.stop()
    sys.exit()
