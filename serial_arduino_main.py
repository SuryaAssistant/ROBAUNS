#for serial communication Arduino-Raspberry Pi
import time
import serial

default_num = 10000

# data send in (kode_motor_belakang,kode_motor_depan,kode_kamera)

data_send = [30, 60, 100]

kode_motor_belakang = 30
kode_motor_depan = 60
kode_kamera = 100

#---------------------------Operation Code---------------------------#
# send and receive data to main arduino
ser_belakang = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

# Get rid of garbage/incomplete data
ser.flush()

while True:

    # Open file that contains 'kode' value

        with open("/home/pi/RoboCov19UNS/data_serial_main.txt", "r", encoding = "utf-8") as h:
            data_serial_main = list(map(int, h.readlines()))

            # pemisahan data
            m = len(data_serial_main)

            #detect and correction if data can't read
            #read data depan = m
            #non-read data depan = n
            n = 5 - m

            #print read data with their value
            for l in range(m):
                if data_serial_belakang[l] != '':
                    data_belakang[l] = int (data_serial_main[l])
                #if datasplit_arduino[l] == '':
                #    data[l] = default_num

            #print non-read data with default_num
            #for h in range(j):
            #   data[h+k] = default_num
            print(data)

            if n != 0:
                kode_motor_belakang = data_belakang[0]
                kode_motor_depan = data_belakang[1]
                kode_kamera = data_belakang[2]
            
    # Convert the integers to a comma-separated string
    angle_value_list = [str(kode_motor_belakang),str(kode_motor_depan),str(kode_kamera)]
    send_string = ','.join(angle_value_list)
    send_string += "\n"
    
    # Send the string. 
    ser.write(send_string.encode('utf-8'))

    # After sending, set  position of motor depan and kamera to be diam to prevent from next unpressed key
    # save command to file and send to arduino main

    kode_motor_depan = 60
    kode_kamera = 100
    
    f = open("data_serial_main.txt","w")
    f.write("%d \r\n" %kode_motor_belakang)
    f.write("%d \r\n" %kode_motor_depan)
    f.write("%d \r\n" %kode_kamera)
    f.close()
