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

#tkinter
from tkinter import *
from PIL import Image
from PIL import ImageTk


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

print("Loading...")
sleep(1.00)

print("Start")

#------------------------------Function------------------------------#
      
def kanan():
    print ("kanan")
    
def kiri():
    print ("kiri")

def mundur():
    print ("mundur")
    
def maju():
    print ("maju")
    
def diam():
    print ("Berhenti")
    
#---------------------------Kode Awal---------------------------#

ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", type=str, default="barcodes.csv",
    help="path to output CSV file containing barcodes")
args = vars(ap.parse_args())

# start video stream
vs = VideoStream(1).start()

print("[INFO] starting video stream...")

sleep(2.0)

#---------------------------Operation Code---------------------------#

while(True):
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
        if barcodeData == 'J1':
            print('Found')

    # show image
    cv2.imshow("Frame", frame)
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