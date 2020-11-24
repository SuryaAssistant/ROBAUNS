import cv2
import cv2 as cv
import pyzbar
import time
import threading
import tkinter as tk

from PIL import Image, ImageTk

class Scanner(object):
    def __init__(self, handler, *args, **kw):
        self.thread = threading.Thread(target=self.run)
        self.handler = handler

        self.CV_SYSTEM_CACHE_CNT = 5 # Cv has 5-frame cache
        self.LOOP_INTERVAL_TIME = 0.2
        self.cam = cv2.VideoCapture(-1)

        self.scanner = zbar.ImageScanner()
        self.scanner.parse_config('enable')
        self.cam_width = int(self.cam.get(cv.CV_CAP_PROP_FRAME_WIDTH))
        self.cam_height = int(self.cam.get(cv.CV_CAP_PROP_FRAME_HEIGHT))

        self.last_symbol = None

    def start(self):
        self.thread.start()

    def scan(self, aframe):
        imgray = cv2.cvtColor(aframe, cv2.COLOR_BGR2GRAY)
        raw = str(imgray.data)
        image_zbar = zbar.Image(self.cam_width, self.cam_height, 'Y800', raw)
        self.scanner.scan(image_zbar)

        for symbol in image_zbar:
            return symbol.data

    def run(self):
        print ('starting scanner')

        while True:
            if self.handler.need_stop():
                break

            # explanation for this in
            # http://stackoverflow.com/a/35283646/5781248
            for i in range(0, self.CV_SYSTEM_CACHE_CNT):
                self.cam.read()

            img = self.cam.read()

            self.handler.send_frame(img)

            self.data = self.scan(img[1])

            if self.handler.need_stop():
                break

            if self.data is not None and (self.last_symbol is None):
                # print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data
                self.handler.send_symbol(self.data)
                self.last_symbol = self.data

            time.sleep(self.LOOP_INTERVAL_TIME)

        self.cam.release()

class ScanWindow(tk.Toplevel):
    def __init__(self, parent, gui, *args, **kw):
        tk.Toplevel.__init__(self, master=parent, *args, **kw)

        self.parent = parent
        self.gui = gui
        self.scanner = None

        self.lock = threading.Lock()
        self.stop_event = threading.Event()

        self.img_label = tk.Label(self)
        self.img_label.pack(side=tk.TOP)

        self.close_button = tk.Button(self, text='close', command=self._stop)
        self.close_button.pack()

        self.bind('<Escape>', self._stop)

        parent.bind('<<ScannerFrame>>', self.on_frame)
        parent.bind('<<ScannerEnd>>', self.quit)
        parent.bind('<<ScannerSymbol>>', self.on_symbol)

    def start(self):
        self.frames = []
        self.symbols = []

        class Handler(object):
            def need_stop(self_):
                return self.stop_event.is_set()

            def send_frame(self_, frame):
                self.lock.acquire(True)
                self.frames.append(frame)
                self.lock.release()

                self.parent.event_generate('<<ScannerFrame>>', when='tail')

            def send_symbol(self_, data):
                self.lock.acquire(True)
                self.symbols.append(data)
                self.lock.release()

                self.parent.event_generate('<<ScannerSymbol>>', when='tail')

        self.stop_event.clear()
        self.scanner = Scanner(Handler())
        self.scanner.start()
        self.deiconify()

    def _stop(self, *args):
        self.gui.stop()

    def stop(self):
        if self.scanner is None:
            return

        self.stop_event.set()

        self.frames = []
        self.symbols = []
        self.scanner = None
        self.iconify()

    def quit(self, *args):
        self.parent.event_generate('<<ScannerQuit>>', when='tail')

    def on_symbol(self, *args):
        self.lock.acquire(True)
        symbol_data = self.symbols.pop(0)
        self.lock.release()

        print ('symbol', '"%s"' % symbol_data)
        self.after(500, self.quit)

    def on_frame(self, *args):
        self.lock.acquire(True)
        frame = self.frames.pop(0)
        self.lock.release()

        _, img = frame
        img = cv2.flip(img, 1)
        cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.img_label.imgtk = imgtk
        self.img_label.configure(image=imgtk)

class GUI(object):
    def __init__(self, root):
        self.root = root

        self.scan_window = ScanWindow(self.root, self)
        self.scan_window.iconify()

        self.root.title('QR Scan !!')

        self.lframe = tk.Frame(self.root)
        self.lframe.pack(side=tk.TOP)

        self.start_button = tk.Button(self.lframe, text='start', command=self.start)
        self.start_button.pack(side=tk.LEFT)

        self.stop_button = tk.Button(self.lframe, text='stop', command=self.stop)
        self.stop_button.configure(state='disabled')
        self.stop_button.pack(side=tk.LEFT)

        self.close_button = tk.Button(self.root, text='close', command=self.quit)
        self.close_button.pack(side=tk.TOP)

        self.root.bind('<<ScannerQuit>>', self.stop)
        self.root.bind('<Control-s>', self.start)
        self.root.bind('<Control-q>', self.quit)
        self.root.protocol('WM_DELETE_WINDOW', self.quit)

    def start(self, *args):
        self.start_button.configure(state='disabled')
        self.scan_window.start()
        self.stop_button.configure(state='active')

    def stop(self, *args):
        self.scan_window.stop()
        self.start_button.configure(state='active')
        self.stop_button.configure(state='disabled')

    def quit(self, *args):
        self.scan_window.stop()
        self.root.destroy()

def main():
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()

main()