import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

kamera_kanan_pin = 6

GPIO.setup(kamera_kiri_pin , GPIO.OUT)

# Set pin awal "LOW"
GPIO.setup(kamera_kiri_pin , GPIO.LOW)

# Aktivasi
GPIO.output(kamera_kiri_pin , GPIO.HIGH)  

# Lama waktu aktif
sleep(0.1)

# Nonaktifkan kembali
GPIO.output(kamera_kiri_pin , GPIO.LOW)  
print ("kamera_kiri")
