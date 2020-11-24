from __future__ import print_function
#for Videostream
import imutils
from imutils.video import VideoStream
from imutils.video import WebcamVideoStream
from pyzbar import pyzbar
#for Tkinder GUI
from tkinter import * 
from tkinter.ttk import *
import tkinter
import tkinter as tk
from tkinter import Tk, Text, TOP, BOTH, X, N, NE, NW, W, E, SE, SW, S, LEFT, RIGHT, CENTER, PhotoImage
import PIL
import PIL.ImageTk
import PIL.Image
from PIL import Image, ImageTk
from tkinter.ttk import Frame, Label, Style
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
# looping siklus counter timing encoder
counter_loop_encoder = 0

#Setting QR  Code Detection
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
    """
    """
    vs = VideoStream(src=1).start() #konfigurasi Raaspi Ifan
    #vs = VideoStream(src=1).start() #Konfigurasi Raspi Fandi
    """
    """
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

#Definisi awal, Setting, dan fungsi GUI
#_______________

ruang_kontrol_state = True
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
force_close_state = True

def ruang_kontrol():
    global ruang_kontrol_state
    if ruang_kontrol_state== True:
        print("menuju ruang kendali")
        
def force_close():
    global force_close_state
    if force_close_state== True:
        print("Force Close Program")

def kamar1():
    global kamar1_state
    global variabel_tujuan
    global variabel_cpoint 
    if kamar1_state== True:
        print ('menuju kamar A1')
        variabel_tujuan = Point_dua
        if variabel_cpoint == Point_satu:
            RK()
            print("last checkpoint ", variabel_cpoint)
        
    

def kamar2():
    global kamar2_state
    if kamar2_state== True:
        print ('menuju kamar A2')
        

def kamar3():
    global kamar3_state
    if kamar3_state== True:
        print ('menuju kamar A3')
        
        
def kamar4():
    global kamar4_state
    if kamar4_state== True:
        print ('menuju kamar A4')
        
      
def kamar5():
    global kamar5_state
    if kamar5_state== True:
        print ('menuju kamar A5')
        

def kamar6():
    global kamar6_state
    if kamar6_state== True:
        print ('menuju kamar A6')
        

def kamar7():
    global kamar7_state
    if kamar7_state== True:
        print ('menuju kamar A6')
        

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
        print ('menuju kamar A11')
        
        
        
def manual():
    global manual_state
    if manual_state ==  True:
        print ('Program alih menjadi manual')
        kontrol_manual()
#_______________

def setup ():
    print('Setting Up System')
    #program apa saja yang perlu dijalankan sebelum memulai program utama
    #os.system ("sudo pigpiod")
    #Flag Room:
    #RK
    global Point_satu
    Point_satu = "1"
    #R1
    global Point_dua
    Point_dua = "2"
    #R2
    global Point_tiga
    Point_tiga = "3"
    #R3
    global Point_empat
    Point_empat = "4"
    #R4
    global Point_lima
    Point_lima = "5"
    #R5
    global Point_enam
    Point_enam = "6"
    #R6
    global Point_tujuh
    Point_tujuh = "7"
    #R7
    global Point_delapan
    Point_delapan = "8"
    #R8
    global Point_sembilan
    Point_sembilan = "9"
    #R9
    global Point_sepuluh
    Point_sepuluh = "10"
    #R10
    global Point_sebelas
    Point_sebelas = "11"
    #R11
    global Point_duabelas
    Point_duabelas = "12"
    
    # variabel_tujuan berisi lokasi yang akan ditujuan
    global variabel_tujuan
    variabel_tujuan = Point_satu

    # variabel_cpoint berisi lokasi sekarang robot (checkpoint)
    global variabel_cpoint
    variabel_cpoint = Point_satu
    
#Logic Program______________________

def RK():
    global variabel_tujuan
    global variabel_cpoint    
    if variabel_tujuan == variabel_cpoint:
        print("robot sudah ditempat tujuan")
        """"""
        variabel_cpoint = variabel_tujuan
    
    if variabel_tujuan == Point_dua:
        print("Dari RK menuju R1")
        """"""
        variabel_cpoint = variabel_tujuan
    
    if variabel_tujuan == Point_tiga:
        print("Dari RK menuju R2")
        """"""
        variabel_cpoint = variabel_tujuan
    
    if variabel_tujuan == Point_empat:
        print("Dari RK menuju R3")
        """"""
        variabel_cpoint = variabel_tujuan
    
    if variabel_tujuan == Point_lima:
        print("Dari RK menuju R4")
        """"""
        variabel_cpoint = variabel_tujuan
    
    if variabel_tujuan == Point_enam:
        print("Dari RK menuju R5")
        """"""
        variabel_cpoint = variabel_tujuan
    
    if variabel_tujuan == Point_tujuh:
        print("Dari RK menuju R7")
        """"""
        variabel_cpoint = variabel_tujuan
    
    if variabel_tujuan == Point_delapan:
        print("Dari RK menuju R7")
        """"""
        variabel_cpoint = variabel_tujuan
    
    if variabel_tujuan == Point_sembilan:
        print("Dari RK menuju R8")
        """"""
        variabel_cpoint = variabel_tujuan
    
    if variabel_tujuan == Point_sepuluh:
        print("Dari RK menuju R9")
        """"""
        variabel_cpoint = variabel_tujuan
    
    if variabel_tujuan == Point_sebelas:
        print("Dari RK menuju R10")
        """"""
        variabel_cpoint = variabel_tujuan
    
    if variabel_tujuan == Point_duabelas:
        print("Dari RK menuju R11")
        """"""
        variabel_cpoint = variabel_tujuan
    

def R1():
    global variabel_tujuan
    global variabel_cpoint    
    if variabel_tujuan == Point_satu:
        print("Dari R1 menuju RK")
        """"""
        variabel_cpoint = variabel_tujuan
    
    if variabel_tujuan == variabel_cpoint:
        print("robot sudah ditempat tujuan")
        """"""
        variabel_cpoint = variabel_tujuan
    
    if variabel_tujuan == Point_tiga:
        print("Dari R1 menuju R2")
        """"""
        variabel_cpoint = variabel_tujuan
    
    if variabel_tujuan == Point_empat:
        print("Dari R1 menuju R3")
        """"""
        variabel_cpoint = variabel_tujuan
    
    if variabel_tujuan == Point_lima:
        print("Dari R1 menuju R4")
        """"""
        variabel_cpoint = variabel_tujuan
    
    if variabel_tujuan == Point_enam:
        print("Dari R1 menuju R5")
        """"""
        variabel_cpoint = variabel_tujuan
    
    if variabel_tujuan == Point_tujuh:
        print("Dari R1 menuju R7")
        """"""
        variabel_cpoint = variabel_tujuan
    
    if variabel_tujuan == Point_delapan:
        print("Dari R1 menuju R7")
        """"""
        variabel_cpoint = variabel_tujuan
    
    if variabel_tujuan == Point_sembilan:
        print("Dari R1 menuju R8")
        """"""
        variabel_cpoint = variabel_tujuan
    
    if variabel_tujuan == Point_sepuluh:
        print("Dari R1 menuju R9")
        """"""
        variabel_cpoint = variabel_tujuan
    
    if variabel_tujuan == Point_sebelas:
        print("Dari R1 menuju R10")
        """"""
        variabel_cpoint = variabel_tujuan
    
    if variabel_tujuan == Point_duabelas:
        print("Dari R1 menuju R11")
        """"""
        variabel_cpoint = variabel_tujuan

def R2():
    global variabel_tujuan
    global variabel_cpoint    
    if variabel_tujuan == Point_satu:
        print("Dari R2 menuju RK")
        """"""
        variabel_cpoint = variabel_tujuan
    
    if variabel_tujuan == Point_dua:
        print("Dari R2 menuju R1")
        """"""
        variabel_cpoint = variabel_tujuan
    ########################################################baru sampai sini
    if variabel_tujuan == Point_tiga:
        print("robot sudah ditempat tujuan")
        """"""
        variabel_cpoint = variabel_tujuan
    
    if variabel_tujuan == Point_empat:
        print("Dari R1 menuju R3")
        """"""
        variabel_cpoint = variabel_tujuan
    
    if variabel_tujuan == Point_lima:
        print("Dari R1 menuju R4")
        """"""
        variabel_cpoint = variabel_tujuan
    
    if variabel_tujuan == Point_enam:
        print("Dari R1 menuju R5")
        """"""
        variabel_cpoint = variabel_tujuan
    
    if variabel_tujuan == Point_tujuh:
        print("Dari R1 menuju R7")
        """"""
        variabel_cpoint = variabel_tujuan
    
    if variabel_tujuan == Point_delapan:
        print("Dari R1 menuju R7")
        """"""
        variabel_cpoint = variabel_tujuan
    
    if variabel_tujuan == Point_sembilan:
        print("Dari R1 menuju R8")
        """"""
        variabel_cpoint = variabel_tujuan
    
    if variabel_tujuan == Point_sepuluh:
        print("Dari R1 menuju R9")
        """"""
        variabel_cpoint = variabel_tujuan
    
    if variabel_tujuan == Point_sebelas:
        print("Dari R1 menuju R10")
        """"""
        variabel_cpoint = variabel_tujuan
    
    if variabel_tujuan == Point_duabelas:
        print("Dari R1 menuju R11")
        """"""
        variabel_cpoint = variabel_tujuan


#Memanggil kontrol manual
    #_____________________
def kontrol_manual():
    kontrol_manual=subprocess.Popen(["python3", "kontrol_motor_tanpa_qr.py"], stdout=PIPE, stderr=PIPE)
    stdout, stderr = kontrol_manual.communicate()
    print(stdout)

def diam():
    p_diam=subprocess.Popen(["python3", "kontrol_motor_diam.py"], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p_diam.communicate()
    print(stdout)
    
#______________________

#GUI
#___________________________
class App:
    def __init__(self, master, video_source=1):
        self.master = master
        self.master.geometry("450x600")
        self.frame = tk.Frame(self.master)
        self.master.title("Robot Covid-19 GUI")
        self.video_source = video_source

        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)

        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(master, width = 400, height = 400)
        self.canvas.pack()

        # Buttons in Main GUI
        self.auto_button=tkinter.Button(master, text="Autonomus", width=50, command=lambda: self.new_window(Win2))
        self.auto_button.pack(anchor=tkinter.CENTER, expand=True)
        self.manual_button=tkinter.Button(master, text="Manual", width=50, command=lambda: self.new_window(Win3))
        self.manual_button.pack(anchor=tkinter.CENTER, expand=True)
        self.exit_button=tkinter.Button(master, text="Exit", width=50, command=lambda: self.master.destroy())
        self.exit_button.pack(anchor=tkinter.CENTER, expand=True)
 
        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()
 
        self.master.mainloop()
 
    def create_button(self, text, _class):
        "Button that creates a new window"
        tk.Button(
            self.frame, text=text,
            command=lambda: self.new_window(_class)).pack(side=LEFT, padx=5, pady=5)

    def create_button_1(self, text, _class):
        "Button that creates a new window"
        tk.Button(
            self.frame, text=text,
            command=lambda: self.new_window(_class),bg="green").grid(row=1, column=2, padx=5, pady=5)
    
    def new_window(self, _class):
        self.win = tk.Toplevel(self.master)
        _class(self.win)

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
            self.master.after(self.delay, self.update)
  
class MyVideoCapture:
    def __init__(self, video_source=1):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)
        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
    
    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)
      # Release the video source when the object is destroyed
    def __del__(self):
         if self.vid.isOpened():
             self.vid.release()

class Win2(App):
    global logo, logodev
    def __init__(self, master):
        self.master = master
        self.master.title("Autonomus Mode")
        self.master.geometry("420x400")
        logo = Image.open("Logo_UNS_1.png")
        logodev = ImageTk.PhotoImage(logo)
        self.canvas = tkinter.Canvas(master, width = 100, height = 100)
        self.canvas.grid(row=0, column=0, padx=0, pady=0)
        self.autonomus_panel()
    
    def autonomus_panel(self):
        "A frame with a button to quit the window"
        self.frame = tk.Frame(self.master)#, bg="blue")
        self.logodev = ImageTk.PhotoImage(Image.open("Logo_UNS_1.png"))
        self.canvas.create_image(0,0, anchor=NW, image=self.logodev)
        self.canvas.image = self.logodev
        
        self.Button1= tk.Button(self.frame, text="Kamar A1", bg="gray", command= kamar1, height = 1, width = 7)
        self.Button1.grid(row=0, column=0, padx=5, pady=5)

        self.Button2= tk.Button(self.frame, text="Kamar A2",bg="white", command= kamar2, height = 1, width = 7)
        self.Button2.grid(row=1, column=0, padx=5, pady=5)

        self.Button3= tk.Button(self.frame, text="Kamar A3", bg="gray", command= kamar3, height = 1, width = 7)
        self.Button3.grid(row=2, column=0, padx=5, pady=5)

        self.Button4= tk.Button(self.frame, text="Kamar A4",bg="white", command= kamar4, height = 1, width = 7)
        self.Button4.grid(row=3, column=0, padx=5, pady=5)

        self.Button5= tk.Button(self.frame, text="Kamar A5", bg="gray", command= kamar5, height = 1, width = 7)
        self.Button5.grid(row=4, column=0, padx=5, pady=5)

        self.Button6= tk.Button(self.frame, text="Kamar A6",bg="white", command= kamar6, height = 1, width = 7)
        self.Button6.grid(row=5, column=0, padx=5, pady=5)

        self.Button7= tk.Button(self.frame, text="Kamar A7",bg="gray", command= kamar7, height = 1, width = 7)
        self.Button7.grid(row=0, column=1, padx=5, pady=5)

        self.Button8= tk.Button(self.frame, text="Kamar A8",bg="white", command= kamar8, height = 1, width = 7)
        self.Button8.grid(row=1, column=1, padx=5, pady=5)

        self.Button9= tk.Button(self.frame, text="Kamar A9",bg="gray", command= kamar9, height = 1, width = 7)
        self.Button9.grid(row=2, column=1, padx=5, pady=5)

        self.Button10= tk.Button(self.frame, text="Kamar A10",bg="white", command= kamar10, height = 1, width = 7)
        self.Button10.grid(row=3, column=1, padx=5, pady=5)

        self.Button11= tk.Button(self.frame, text="Kamar A11",bg="gray", command= kamar11, height = 1, width = 7)
        self.Button11.grid(row=4, column=1, padx=5, pady=5)
        
        self.Button12= tk.Button(self.frame, text="Ruang Kendali",bg="white", command= ruang_kontrol, height = 1, width = 9)
        self.Button12.grid(row=5, column=1, padx=5, pady=5)
        
        self.quit_button= tk.Button(self.frame, text=f"Quit From Autonomus Mode", command= self.close_window)
        self.quit_button.grid(row=0, column=2, padx=5, pady=5)
        
        self.force_close= tk.Button(self.frame, text=f"Force Close", command= force_close)
        self.force_close.grid(row=2, column=2, padx=5, pady=5)
        
        self.create_button_1("Open Manual Mode", Win3)
        self.frame.grid()

    def close_window(self):
        self.master.destroy()


class Win3(App):
    def __init__(self, master):
        self.master = master
        self.master.title("Manual Mode")
        self.master.geometry("400x100+200+200")
        self.manual_panel()

    def manual_panel(self):
        self.frame = tk.Frame(self.master, bg="green")
        self.label = tk.Label(
            self.frame, text="THIS WILL TRIGGER MANUAL CONTROL")
        self.label.pack()
        self.quit = tk.Button(
            self.frame, text=f"Lunch Manual Mode",
            command= kontrol_manual)
        self.quit.pack()
        self.frame.pack()

    def close_window(self):
        self.master.destroy()

#________________________

def IR ():
    #GPIO for the IR transmitter: 22
    #os.system ("sudo pigpiod")
    from ircodec.command import CommandSet
    controller = CommandSet.load('Ardoor.json')
    time.sleep (0.002)
    controller.emit('Trigger')
    print ('Wave send')


#Juction Codes
J1 = 'J1'
J2 = 'J2'
J3 = 'J3'
J4 = 'J4'
J5 = 'J5'
J6 = 'J6'
J7 = 'J7'

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

#_________________________
#Startup
setup()
App(tkinter.Tk())




#Door ()
GPIO.cleanup()