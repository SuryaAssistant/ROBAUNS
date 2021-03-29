#for serial communication Arduino-Raspberry Pi
import time
import serial

default_num = 10000

#x_encoder = 0
#enc_pos = 0

us_kiri_dpn = default_num
us_tengah_dpn = default_num
us_kanan_dpn = default_num

data = [us_kiri_dpn, us_tengah_dpn, us_kanan_dpn]

#---------------------------Read USBx Port---------------------------#
with open("/home/pi/RoboCov19UNS/usb_port_config.txt", "r", encoding = "utf-8") as h:
    data_port = list(map(int, h.readlines()))

    # pemisahan data:
    m = len(data_port)

    #detect and correction if data can't read
    #read data depan = m
    #non-read data depan = n
    n = 3 - m

    #print read data with their value
    for l in range(m):
        if data_port[l] != '':
            get_port[l] = int (data_port[l])
        #if datasplit_arduino[l] == '':
        #    data[l] = default_num

    #print non-read data with default_num
    #for h in range(j):
    #   data[h+k] = default_num

    #print(data)
    if n != 0:
        arduino_depan_port = get_port[1]

#---------------------------Operation Code---------------------------#
# depan
ser_depan = serial.Serial(
  
   port='/dev/ttyUSB{}'.format(arduino_depan_port),
   baudrate = 9600,
   parity=serial.PARITY_NONE,
   stopbits=serial.STOPBITS_ONE,
   bytesize=serial.EIGHTBITS,
   timeout=1
)

#counter=0

#encoder = 0

while 1:
    read_depan=ser_depan.readline()
    #print(read_depan)

    datasplit_depan = read_depan.decode('utf-8', 'ignore').strip('\r\n').strip().split(',')

    #print(datasplit_depan)
    # pemisahan data:
    k = len(datasplit_depan)
    
    #detect and correction if data can't read
    #read data = k
    #non-read data = j
    j = 3 - k
    
    #print read data with their value
    for i in range(k):
        if datasplit_depan[i] != '':
            data[i] = int (datasplit_depan[i])
        #if datasplit_arduino[i] == '':
        #    data[i] = default_num
    
    #print non-read data with default_num
    #for h in range(j):
    #   data[h+k] = default_num
    
    print(data)

    #save variable files (apabila data tidak kosong)--> dispaly
    if j != 0:
        f = open("data_serial_depan.txt","w")
        #f.write("%d \r\n" %data[0]) #x_enc
        #f.write("%d \r\n" %data[1]) #enc_pos
        
        #avoiding 0 value in ultrasonic sensor
        if(data[0] == 0) :
            data[0] = default_num
        f.write("%d \r\n" %data[0]) #us_kiri_dpn
        if(data[1] == 0) :
            data[1] = default_num
        f.write("%d \r\n" %data[1]) #us_tengah_dpn
        if(data[2] == 0) :
            data[2] = default_num
        f.write("%d \r\n" %data[2]) #us_kanan_dpn
        f.close()
