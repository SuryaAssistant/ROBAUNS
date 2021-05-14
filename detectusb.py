import time
import serial

# detect arduino port posistion in raspberry pi
def usb_detect(port_number, pesan):    
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
        
    return decode_usb
