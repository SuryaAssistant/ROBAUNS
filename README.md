<span align = "center">
  
# RoboCov19UNS

### Sedang dalam pengembangan
  
</span>

<br>

## Pendahuluan
Merupakan robot pembantu perawat untuk mengantarkan barang dan memonitoring pasien Covid 19 secara remote

Robot menggunakan Raspberry Pi 3B+ sebagai komputer pengontrol robot serta menggunakan Arduino untuk mengontrol motor, servo, dan membaca sensor.

- Release algoritma yang digunakan
  > https://github.com/robotcovid19uns/RoboCov19UNS/tree/main

- Release algoritma baru 
  > https://github.com/robotcovid19uns/RoboCov19UNS/tree/only_serial

- Upload update algoritma lama
  > https://github.com/robotcovid19uns/RoboCov19UNS/tree/pengembangan

- Upload update algoritma baru (edit_serial)
  > https://github.com/robotcovid19uns/RoboCov19UNS/tree/edit_serial

<br>

## Cara Install

Salin _command_ di bawah dan tempel di terminal Raspberry Pi

### Update

```
sudo apt-get update
```
```
sudo apt-get upgrade
```

### Instal _Dependency(s)_
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
git clone https://github.com/robotcovid19uns/RoboCov19UNS
```

Masuk ke dalam folder `RoboCov19UNS` dan kemudian jalankan `main_program.py`
