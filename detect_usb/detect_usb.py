# This program used to detect which one is an
# arduino used as main, front us sensor, and back us sensor
#
#
# Created by : Fandi Adinata

import time
import serial

# number of Arduino that connect to Raspberry Pi
total_usb = 3

port_0 = 0
port_1 = 0
port_2 = 0

# default reply from Arduino
code_usb= ["default","default","default"]

arduino_main_port = 4
arduino_depan_port = 4
arduino_belakang_port = 4

# detect Arduino port posistion in Raspberry Pi
def detect_usb(port_number):
    global decode_usb
    
    with serial.Serial("/dev/ttyUSB{}".format(port_number), 9600, timeout=1) as detect_USB:
        time.sleep(0.5) #wait serial to open
        print("Check USB{}".format(detect_USB.port))

        if detect_USB.isOpen():
            print("{} terkoneksi!".format(detect_USB.port))
            check_port_cmd = "check"
            check_cmd = ("{}\n".format(check_port_cmd))
            time.sleep(1)
            detect_USB.flushInput()
            detect_USB.write(check_cmd.encode('utf-8'))
        
            while detect_USB.inWaiting()==0: pass
            if detect_USB.inWaiting():
                answer=detect_USB.readline()
                decode_usb = answer.decode('utf-8').rstrip()
                detect_USB.flushInput()
        else:
            print("{} tidak terhubung!".format(detect_USB.port))


times_usb = 0

# detect USBPort 
for x in range(total_usb):
    detect_usb(x)

    while True:
        if str(decode_usb) == "main" or str(decode_usb) == "depan" or str(decode_usb) == "belakang":
            print ("USB{} dikenali".format(x))
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
            detect_usb(x)
            times_usb += 1
            if times_usb == 5:
                times_usb = 0
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

print("Konfigurasi port USB disimpan")
