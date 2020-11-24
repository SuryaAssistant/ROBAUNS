#for serial communication Arduino-Raspberry Pi
import serial

default_num = 10000

us_kiri_dpn = default_num
us_tengah_dpn = default_num
us_kanan_dpn = default_num

us_kiri_blk = default_num
us_tengah_blk = default_num
us_kanan_blk = default_num

#---------------------------Operation Code---------------------------#
# depan
ser_depan = serial.Serial('/dev/ttyUSB1',9600)

# belakang
ser_belakang = serial.Serial('/dev/ttyUSB2',9600)

counter = 0

while 1:
    read_depan=ser_depan.readline()
    read_belakang = ser_belakang.readline()
    #print(read_depan, read_belakang)

    datasplit_depan = read_depan.decode('utf-8', 'ignore').strip('\r\n').strip().split(',')
    datasplit_belakang = read_belakang.decode('utf-8', 'ignore').strip('\r\n').strip().split(',')

    print(datasplit_depan, datasplit_belakang)

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

    if len(datasplit_depan) == 1:
        if datasplit_depan[0] != '':
            us_kiri_dpn = int(datasplit_depan[0])
        if datasplit_depan[0] == '':
            us_kiri_dpn = default_num
        
    if len(datasplit_depan) == 0:
        us_kiri_dpn = default_num
        us_tengah_dpn = default_num
        us_kanan_dpn = default_num
        
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

    if len(datasplit_belakang) == 1:
        if datasplit_belakang[0] != '':
            us_kiri_blk = int(datasplit_belakang[0])
        if datasplit_belakang[0] == '':
            us_kiri_blk = default_num
        
    if len(datasplit_belakang) == 0:
        us_kiri_blk = default_num
        us_tengah_blk = default_num
        us_kanan_blk = default_num

    #save variable files
    f = open("data_serial.txt","w")
    f.write("%d \r\n" %us_tengah_dpn)
    f.write("%d \r\n" %us_kanan_dpn)
    f.write("%d \r\n" %us_kiri_dpn)
    f.write("%d \r\n" %us_tengah_blk)
    f.write("%d \r\n" %us_kanan_blk)
    f.write("%d \r\n" %us_kiri_blk)
    f.close()
