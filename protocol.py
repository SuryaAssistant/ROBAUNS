# Motor Belakang
def belakang_maju():
    return 1

def belakang_mundur():
    return 2

def belakang_diam():
    return 3

# Motor Depan
def depan_kanan():
    return 4

def depan_kiri():
    return 5

def depan_diam():
    return 6

# Kamera
def kamera_kanan():
    return 11

def kamera_kiri():
    return 10

def kamera_tengah():
    return 12

def kamera_diam():
    return 13

def force_stop():
    belakang_diam()
    depan_diam()
    kamera_diam()

    kode_enkripsi = "1" + str(kode_motor_belakang) + str(kode_motor_depan) + str(kode_kamera)
    string_kode = kode_enkripsi
    stop_string = ("{}\n".format(string_kode))

    return stop_string
