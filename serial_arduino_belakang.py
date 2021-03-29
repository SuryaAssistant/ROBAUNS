#for serial communication Arduino-Raspberry Pi
import time
import serial

default_num = 10000

#x_encoder = 0
#enc_pos = 0

us_kiri_blk = default_num
us_tengah_blk = default_num
us_kanan_blk = default_num

data = [us_kiri_blk, us_tengah_blk, us_kanan_blk]

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
        arduino_belakang_port = get_port[2]


#---------------------------Operation Code---------------------------#
# belakang
ser_belakang = serial.Serial(
  
    port='/dev/ttyUSB{}'.format(arduino_belakang_port),
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

counter=0

while True:
    read_belakang = ser_belakang.readline()
    #print(read_belakang)

    datasplit_belakang = read_belakang.decode('utf-8', 'ignore').strip('\r\n').strip().split(',')

    #print(datasplit_belakang)
    # pemisahan data:
    k = len(datasplit_belakang)
    
    #detect and correction if data can't read
    #read data = k
    #non-read data = j
    j = 3 - k
    
    #print read data with their value
    for i in range(k):
        if datasplit_belakang[i] != '':
            data[i] = int (datasplit_belakang[i])
        #if datasplit_arduino[i] == '':
        #    data[i] = default_num
    
    #print non-read data with default_num
    #for h in range(j):
    #   data[h+k] = default_num
    
    print(data)

    #save variable files (apabila data tidak kosong)--> dispaly
    if j != 0:
        f = open("data_serial_belakang.txt","w")
        #avoiding 0 value in ultrasonic sensor
        if(data[0] == 0) :
            data[0] = default_num
        f.write("%d \r\n" %data[0]) #us_kiri_blk
        if(data[1] == 0) :
            data[1] = default_num
        f.write("%d \r\n" %data[1]) #us_tengah_blk
        if(data[2] == 0) :
            data[2] = default_num
        f.write("%d \r\n" %data[2]) #us_kanan_blk
        f.close()
