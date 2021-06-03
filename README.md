<span align = "center">

 ![Logo](https://github.com/ROBA-UNS/ROBAUNS/blob/v0.9.1-beta/logo/Logo_UNS_1.png)

# ROBA UNS

### Sedang dalam pengembangan
  
</span>

<br>

## Pendahuluan
Merupakan robot pembantu perawat untuk mengantarkan barang dan memonitoring pasien secara remote.

- Release
  > https://github.com/Robot-Asisten-ROBA-UNS/ROBAUNS

<br>

## Cara Install

Salin command di bawah dan tempel di terminal Raspberry Pi

### Update

```
sudo apt-get update
```
```
sudo apt-get upgrade
```

### Instal Dependency
```
sudo apt-get install build-essential cmake pkg-config
```
```
sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
```
```
sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
```
```
sudo apt-get install libgtk2.0-dev
```
```
sudo apt-get install libatlas-base-dev gfortran
```
```
sudo pip install virtualenv virtualenvwrapper
```
```
sudo apt-get install libhdf5-dev libhdf5-serial-dev libhdf5-103 
```
```
sudo apt-get install libqtgui4 libqtwebkit4 libqt4-test 
```
```
sudo apt-get install libatlas-base-dev 
```
```
sudo apt-get install libjasper-dev 
```
```
wget https://bootstrap.pypa.io/get-pip.py 
```
```
sudo python3 get-pip.py 
```

### Instal OpenCV
```
sudo pip3 install opencv-contrib-python==3.4.6.27
```
```
pip install imutils
```

### Clone Github Repository
Buka terminal dan ketik
```
git clone https://github.com/Robot-Asisten-ROBA-UNS/ROBAUNS
```

Masuk ke dalam folder `ROBAUNS` dan kemudian jalankan `main_program.py`

### Testing
Apabila Anda ingin mencoba `main_program.py`, maka setidaknya memerlukan :
1. 1 buah Raspberry Pi (minimal 3B)
2. 3 buah Arduino dengan CH340G atau yang terbaca sebagai `tty/dev/USBx`
2. 1 buah kamera USB

Langkah - langkah :
1. Install dependency(s) yang diperlukan di terminal.
2. Clone repository ini di folder `/home/pi/`.
3. Upload program Arduino di folder `arduino_files` ke masing-masing Arduino.
4. Hubungkan tiga buah Arduino dengan port USB di Raspberry Pi.
5. Hubungkan sebuah kamera USB ke salah satu port USB Raspberry Pi.
6. Jalankan `main_program.py`
