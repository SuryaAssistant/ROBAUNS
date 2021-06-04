# Color set as (Blu,e Green, Red)
def color_primary():
    return (255, 123, 0)

def color_secondary():
    return (125,117,108)

def color_danger():
    return (69,53,220)

def color_success():
    return (69, 167, 40)

def color_warning():
    return (7, 193, 255)

def color_info():
    return (184, 162, 23)

def color_light():
    return (250, 249, 248)

def color_dark():
    return (64, 58, 52)

def color_white():
    return (255, 255, 255)

if __name__ == "__main__":
    print("This is color package based on Bootstrap v4\n")
    print("Example : \n")
    print("from color import *")
    print("object_color = color_success()")
