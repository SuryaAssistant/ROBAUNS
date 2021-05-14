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

# Unique function
# create command string
def command(belakang, depan, kamera):
    kode_enkripsi = "1" + str(belakang) + str(depan) + str(kamera)
    command_string = ("{}\n".format(kode_enkripsi))
    return command_string

# force stop command
def force_stop():
    belakang = belakang_diam()
    depan = depan_diam()
    kamera = kamera_diam()

    stop_kode = command(belakang, depan, kamera)
    stop_command = ("{}\n".format(stop_kode))

    return stop_command
    