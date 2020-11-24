#for serial communication Arduino-Raspberry Pi
import time
import serial

default_num = 10000

us_kiri_dpn = default_num
us_tengah_dpn = default_num
us_kanan_dpn = default_num

#---------------------------Operation Code---------------------------#
# depan
ser_depan = serial.Serial(
  
   port='/dev/ttyUSB0',
   baudrate = 9600,
   parity=serial.PARITY_NONE,
   stopbits=serial.STOPBITS_ONE,
   bytesize=serial.EIGHTBITS,
   timeout=1
)

counter=0

encoder = 0

while 1:
    read_depan=ser_depan.readline()
    #print(read_depan)

    datasplit_depan = read_depan.decode('utf-8', 'ignore').strip('\r\n').strip().split(',')

    #print(datasplit_depan)
    # pemisahan data:

    # banyak data (harusnya 3, tapi terkadang hanya 2 atau 1)
    # us_depan

    if len(datasplit_depan) == 3:
        if datasplit_depan[0] != '':
            us_kiri_dpn = int(datasplit_depan[0])
        if datasplit_depan[0] == '':
            us_kiri_dpn = default_num
        if datasplit_depan[1] !='':
            us_tengah_dpn = int(datasplit_depan[1])
        if datasplit_depan[1] =='':
            us_tengah_dpn = default_num
        if datasplit_depan[2] !='':
            us_kanan_dpn = int(datasplit_depan[2])
        if datasplit_depan[2] == '':
            us_kanan_dpn = default_num
        
    if len(datasplit_depan) == 2:
        if datasplit_depan[0] != '':
            us_kiri_dpn = int(datasplit_depan[0])
        if datasplit_depan[0] == '':
            us_kiri_dpn = default_num
        if datasplit_depan[1] !='':
            us_tengah_dpn = int(datasplit_depan[1])
        if datasplit_depan[1] =='':
            us_tengah_dpn = default_num
        us_kanan_dpn = default_num

    if len(datasplit_depan) == 1:
        if datasplit_depan[0] != '':
            us_kiri_dpn = int(datasplit_depan[0])
        if datasplit_depan[0] == '':
            us_kiri_dpn = default_num
        us_tengah_dpn = default_num
        us_kanan_dpn = default_num
        
    if len(datasplit_depan) == 0:
        us_kiri_dpn = default_num
        us_tengah_dpn = default_num
        us_kanan_dpn = default_num
        
    #save variable files
    f = open("data_serial_depan.txt","w")
    f.write("%d \r\n" %us_kiri_dpn)
    f.write("%d \r\n" %us_tengah_dpn)
    f.write("%d \r\n" %us_kanan_dpn)
    f.close()