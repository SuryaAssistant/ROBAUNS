from __future__ import print_function
#for Videostream
import imutils
from imutils.video import VideoStream
from imutils.video import WebcamVideoStream
from pyzbar import pyzbar
import tkinter as tk 
#for numerical and other calculation
import argparse
import numpy as np
import datetime
#for OpenCV
import cv2
#for serial communication Arduino-Raspberry Pi
import serial
#for call other script in 'background'
import subprocess
from subprocess import Popen, PIPE
from time import sleep
import time

import os

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#------------------SERVO------------------#
servoPIN = 18
GPIO.setup(servoPIN, GPIO.OUT)
p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
p.start(0)
p.ChangeDutyCycle(0)

#---------------Encoder_pins---------------#

print("Loading...")
sleep(1.00)

print("Start")

#------------------------------Function------------------------------#
#Define gerak
def kanan():
    p_kanan=subprocess.Popen(["python3", "kontrol_motor_kanan.py"], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p_kanan.communicate()
    print(stdout)
    
def kiri():
    p_kiri=subprocess.Popen(["python3", "kontrol_motor_kiri.py"], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p_kiri.communicate()
    print(stdout)

def mundur():
    p_mundur=subprocess.Popen(["python3", "kontrol_motor_mundur.py"], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p_mundur.communicate()
    print(stdout)
    
def maju():
    p_maju=subprocess.Popen(["python3", "kontrol_motor_maju.py"], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p_maju.communicate()
    print(stdout)
    
def diam():
    p_diam=subprocess.Popen(["python3", "kontrol_motor_diam.py"], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p_diam.communicate()
    print(stdout)

#Define QR Code in junction
#_________________
k1 = 'J1 (QRCODE)'
k2 = 'J2 (QRCODE)'
k3 = 'J3 (QRCODE)'
k4 = 'J4 (QRCODE)'
k5 = 'J5 (QRCODE)'
k6 = 'J6 (QRCODE)'
k7 = 'J7 (QRCODE)'


QR = '___'
def QR_Code():
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--output", type=str, default="barcodes.csv",
            help="path to output CSV file containing barcodes")
    args = vars(ap.parse_args())
    # initialize the video stream and allow the camera sensor to warm up
    print("starting video stream...")

    vs = VideoStream(src=1).start()

    csv = open(args["output"], "w")
    found = set()
    global QR

# loop over the frames from the video stream
# BN for flaging Barcode
    BN = 0;
    while True:
        # grab the frame from the threaded video stream and resize it to
        # have a maximum width of 400 pixels
        frame = vs.read()
        frame = imutils.resize(frame, width=400)

        # find the barcodes in the frame and decode each of the barcodes
        barcodes = pyzbar.decode(frame)

        # loop over the detected barcodes
        for barcode in barcodes:
        # extract the bounding box location of the barcode and draw
        # the bounding box surrounding the barcode on the image
            (x, y, w, h) = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

            # the barcode data is a bytes object so if we want to draw it
            # on our output image we need to convert it to a string first
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type

            # draw the barcode data and barcode type on the image
            text = "{} ({})".format(barcodeData, barcodeType)
            QR = str(text)
            print (QR)
            
            cv2.putText(frame, text, (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            #All Posibilities of Detection
            if (QR) == (k1):
                        print ('QR = J1')
                        BN = 2;
                    # if the barcode text is currently not in our CSV file, write
            # the timestamp + barcode to disk and update the set
            if (QR) == (k2):
                        print ('QR = J2')
                        BN = 2;
            if (QR) == (k3):
                        print ('QR = J3')
                        BN = 2;
            if (QR) == (k4):
                        print ('QR = J4')
                        BN = 2;
            if (QR) == (k5):
                        print ('QR = J5')
                        BN = 2;
            if (QR) == (k6):
                        print ('QR = J6')
                        BN = 2;
            if (QR) == (k7):
                        print ('QR = J7')
                        BN = 2;
            if BN > 0:
                break
            if barcodeData not in found:
                csv.write("{},{}\n".format(datetime.datetime.now(),
                    barcodeData))
                csv.flush()
                found.add(barcodeData)

    # show the output frame
        cv2.imshow("Frame", frame)

    # if the `q` key was pressed, break from the loop
        if BN > 0:
                break

# close the output CSV file do a bit of cleanup
    print("cleaning up QR Caches")
    BN = 0;
    csv.close()
    cv2.destroyAllWindows()
    vs.stop()
#_________________

#Setting awal untuk GUI
master = tk.Tk()
master.title("GUI Robot_Anti-Covid")
master.geometry("600x150")

#status_button untuk pemilihan kamar
kamar1_state = True
kamar2_state = True
kamar3_state = True
kamar4_state = True
kamar5_state = True
kamar6_state = True
kamar7_state = True
kamar8_state = True
kamar9_state = True
kamar10_state = True
kamar11_state = True
manual_state = True

def kamar1():
    global kamar1_state
    if kamar1_state== True:
        #print ('menuju kamar A1')
        print ('Uji coba PS')
        PS()
        
def kamar2():
    global kamar2state
    if kamar2_state== True:
        #print ('menuju kamar A2')
        print ('Uji coba WDP')
        WDP()

def kamar3():
    global kamar3_state
    if kamar3_state== True:
        #print ('menuju kamar A3')
        print ('Uji coba PWDP')
        PWDP()
        
def kamar4():
    global kamar4_state
    if kamar4_state== True:
        #print ('menuju kamar A4')
        print ('Uji coba PA')
        PA()
      
def kamar5():
    global kamar5_state
    if kamar5_state== True:
        #print ('menuju kamar A5')
        print ('Uji coba PL')
        PL()

def kamar6():
    global kamar6_state
    if kamar6_state== True:
        #print ('menuju kamar A6')
        print ('Uji coba PR')
        PR()

def kamar7():
    global kamar7_state
    if kamar7_state== True:
        #print ('menuju kamar A6')
        print ('Uji coba Door')
        Door()

def kamar8():
    global kamar8_state
    if kamar8_state== True:
        print ('menuju kamar A8')

def kamar9():
    global kamar9_state
    if kamar9_state== True:
        print ('menuju kamar A9')

def kamar10():
    global kamar10_state
    if kamar10_state== True:
        print ('menuju kamar A10')

def kamar11():
    global kamar11_state
    if kamar11_state== True:
        #print ('menuju kamar A11')
        print ('Uji coba QR_Code')
        QR_Code()
        print (QR)
        
        
def manual():
    global manual_state
    if manual_state ==  True:
        print ('Program alih menjadi manual')
        kontrol_manual()


def setup ():
    #Flag Room:
    RK = 1;
    R1 = 0;
    R2 = 0;
    R3 = 0;
    R4 = 0;
    R5 = 0;
    R6 = 0;
    R7 = 0;
    R8 = 0;
    R9 = 0;
    R10 = 0;
    R11 = 0;
    print('System Ready')
    
def kontrol_manual():
    subprocess.call(["python3", "kontrol_motor_tanpa_qr.py"])


#Juction Codes
J1 = 'J1 (QRCODE)'
J2 = 'J2 (QRCODE)'
J3 = 'J3 (QRCODE)'
J4 = 'J4 (QRCODE)'
J5 = 'J5 (QRCODE)'
J6 = 'J6 (QRCODE)'
J7 = 'J7 (QRCODE)'

#Base Command
#___________
#Statment:
#PS: Start Program (only for RK start Point) V
#SPP: Steady and ready Position Program [harus survei dulu]
#SPLP: Steady and ready Position for Last sequence Program [harus survei dulu]
#WDP: Walk and Detection Program (make robot for move for certain distance) V
#PWDP: Pass the current Junction and continous WDP  V
#PA: Program to Across the Juntion (mirip dengan WDP, namun Lebih banyak junctionnya) V
#PL: Program to Turn Left V
#PR: Program to Turn Righ V
#Flag = Last Position of Robot (1 = on, 0 = off)
#D/Door = Program for evertime encounter door V
#MAEP: Model A Room Environment Program (kontrol manual) 
#MBEP: Model B Room Environment Program (kontrol manual)

US = 300;
def PS () :
    print ("Processing PS");
    global US
    time.sleep (0.05)
    maju()
    QR_Code()
    while True:
        if (QR) == (J1):
            print ('Code Match')
            kanan()
            US-=200; #perumpaan agar program berjalan sementara tanpa sensor US
        if US < 200: #US nilai jarak ultrasonic
            diam()
            time.sleep(0.001)
            IR()
            i = 0;
            US+=200; #perumpaan agar program berjalan sementara tanpa sensor US
            break
    print ('PS Selesai')

def WDP () :
    print ("Processing WDP");
    time.sleep (0.05)
    maju()
    QR_Code()
    while True:
        if (QR) == (J2):
            print ('Junction J2 Detected')
            break
        if (QR) == (J3):
            print ('Junction J3 Detected')
            break
        if (QR) == (J4):
            print ('Junction J4 Detected')
            break
        if (QR) == (J5):
            print ('Junction J5 Detected')
            break
        if (QR) == (J6):
            print ('Junction J6 Detected')
            break
    print ('WDP Selesai, robot berjalan melewati Juntion')

def PWDP () :
    print ("Processing PWDP");
    time.sleep (0.05)
    maju()
    QR_Code()
    while True:
        if (QR) == (J2):
            print ('Junction J2 Detected')
            break
        if (QR) == (J3):
            print ('Junction J3 Detected')
            break
        if (QR) == (J4):
            print ('Junction J4 Detected')
            break
        if (QR) == (J5):
            print ('Junction J5 Detected')
            break
        if (QR) == (J6):
            print ('Junction J6 Detected')
            break
    print ('PWDP Selesai, robot berjalan melewati Juntion')

def PA () :
    print ("Processing PA");
    time.sleep (0.05)
    maju()
    QR_Code()
    while True:
        if (QR) == (J2):
            print ('Junction J2 Detected')
            break
        if (QR) == (J3):
            print ('Junction J3 Detected')
            break
        if (QR) == (J4):
            print ('Junction J4 Detected')
            break
        if (QR) == (J5):
            print ('Junction J5 Detected')
            break
        if (QR) == (J6):
            print ('Junction J6 Detected')
            break
        if (QR) == (J7):
            print ('Junction J7 Detected')
            break
    print ('PA Selesai, robot berjalan menyebrang Juntion')

def PL () :
    print ("Processing PL");
    time.sleep (0.05)
    maju()
    QR_Code()
    while True:
        if (QR) == (J2):
            print ('Junction J2 Detected')
            kiri()
            break
        if (QR) == (J3):
            print ('Junction J3 Detected')
            kiri()
            break
        if (QR) == (J4):
            print ('Junction J4 Detected')
            kiri()
            break
        if (QR) == (J5):
            print ('Junction J5 Detected')
            kiri()
            break
        if (QR) == (J6):
            print ('Junction J6 Detected')
            kiri()
            break
        if (QR) == (J7):
            print ('Junction J7 Detected')
            kiri()
            break
    print ('PL Selesai, robot berbelok kiri pada Juntion')

def PR () :
    print ("Processing PR");
    time.sleep (0.05)
    maju()
    QR_Code()
    while True:
        if (QR) == (J2):
            print ('Junction J2 Detected')
            kanan()
            break
        if (QR) == (J3):
            print ('Junction J3 Detected')
            kanan()
            break
        if (QR) == (J4):
            print ('Junction J4 Detected')
            kanan()
            break
        if (QR) == (J5):
            print ('Junction J5 Detected')
            kanan()
            break
        if (QR) == (J6):
            print ('Junction J6 Detected')
            kanan()
            break
        if (QR) == (J7):
            print ('Junction J7 Detected')
            kanan()
            break
    print ('PR Selesai, robot berbelok kanan pada Juntion')

def Door ():
    maju()
    time.sleep(1)
    US = 100; #perumpaan agar program berjalan sementara tanpa sensor US
    while True:
        if US < 200:
            diam()
            IR()
            print ('membuka pintu')
            time.sleep(5)
            US = 300; #perumpaan agar program berjalan sementara tanpa sensor US
            break
    print ('Robot Berlajalan masuk')
    maju()
    time.sleep(7)
    diam()
    print ('Robot telah memasuki ruangan')
#_________________________
#Startup
setup ()


#Button Mapping GUI:
#__________________

Button1= tk.Button(master, text="Kamar A1", bg="gray", command= kamar1, height = 1, width = 7)
Button1.grid(row=0, column=0)

Button2= tk.Button(master, text="Kamar A2",bg="white", command= kamar2, height = 1, width = 7)
Button2.grid(row=1, column=0)

Button3= tk.Button(master, text="Kamar A3", bg="gray", command= kamar3, height = 1, width = 7)
Button3.grid(row=2, column=0)

Button4= tk.Button(master, text="Kamar A4",bg="white", command= kamar4, height = 1, width = 7)
Button4.grid(row=0, column=1)

Button5= tk.Button(master, text="Kamar A5", bg="gray", command= kamar5, height = 1, width = 7)
Button5.grid(row=1, column=1)

Button6= tk.Button(master, text="Kamar A6",bg="white", command= kamar6, height = 1, width = 7)
Button6.grid(row=2, column=1)

Button7= tk.Button(master, text="Kamar A7",bg="gray", command= kamar7, height = 1, width = 7)
Button7.grid(row=0, column=2)

Button8= tk.Button(master, text="Kamar A8",bg="white", command= kamar8, height = 1, width = 7)
Button8.grid(row=1, column=2)

Button9= tk.Button(master, text="Kamar A9",bg="gray", command= kamar9, height = 1, width = 7)
Button9.grid(row=2, column=2)

Button10= tk.Button(master, text="Kamar A10",bg="white", command= kamar10, height = 1, width = 7)
Button10.grid(row=0, column=3)

Button11= tk.Button(master, text="Kamar A11",bg="gray", command= kamar11, height = 1, width = 7)
Button11.grid(row=1, column=3)

Button12= tk.Button(master, text="Manual", bg="blue", command= manual, height = 1, width = 7)
Button12.grid(row=2, column=3)

Exitbutton = tk.Button(master, text="Exit",bg="red", command=master.destroy, height = 1, width = 7)
Exitbutton.grid(row=3, column=3)
master.mainloop()

#_________________

#Door ()
GPIO.cleanup()