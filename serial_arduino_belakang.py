#for serial communication Arduino-Raspberry Pi
import time
import serial

default_num = 10000

us_kiri_blk = default_num
us_tengah_blk = default_num
us_kanan_blk = default_num

#---------------------------Operation Code---------------------------#
# belakang
ser_belakang = serial.Serial(
  
   port='/dev/ttyUSB1',
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

    # banyak data (harusnya 3, tapi terkadang hanya 2 atau 1)

    # us_belakang
    if len(datasplit_belakang) == 3:
        if datasplit_belakang[0] != '':
            us_kiri_blk = int(datasplit_belakang[0])
        if datasplit_belakang[0] == '':
            us_kiri_blk = default_num
        if datasplit_belakang[1] !='':
            us_tengah_blk = int(datasplit_belakang[1])
        if datasplit_belakang[1] =='':
            us_tengah_blk = default_num
        if datasplit_belakang[2] !='':
            us_kanan_blk = int(datasplit_belakang[2])
        if datasplit_belakang[2] == '':
            us_kanan_blk = default_num
        
    if len(datasplit_belakang) == 2:
        if datasplit_belakang[0] != '':
            us_kiri_blk = int(datasplit_belakang[0])
        if datasplit_belakang[0] == '':
            us_kiri_blk = default_num
        if datasplit_belakang[1] !='':
            us_tengah_blk = int(datasplit_belakang[1])
        if datasplit_belakang[1] =='':
            us_tengah_blk = default_num
        us_kanan_blk = default_num

    if len(datasplit_belakang) == 1:
        if datasplit_belakang[0] != '':
            us_kiri_blk = int(datasplit_belakang[0])
        if datasplit_belakang[0] == '':
            us_kiri_blk = default_num
        us_tengah_blk = default_num
        us_kanan_blk = default_num
        
    if len(datasplit_belakang) == 0:
        us_kiri_blk = default_num
        us_tengah_blk = default_num
        us_kanan_blk = default_num

    #save variable files
    f = open("data_serial_belakang.txt","w")
    f.write("%d \r\n" %us_kiri_blk)
    f.write("%d \r\n" %us_tengah_blk)
    f.write("%d \r\n" %us_kanan_blk)
    f.close()
