import os
import cv2
import threading

class Stream:

    def __init__(self, handler):
        self.source = os.getenv('STREAM_SRC', 'rtsp://admin:admin@80.252.145.203:561/live/main')#'rtsp://admin:admin@80.252.145.203:554/live/main')
        print('source', self.source)
        self.cap = cv2.VideoCapture(self.source)
        #
        self.quality = int(os.getenv('STREAM_QUALITY') or '50') # 1-100
        self.codec = (int(cv2.IMWRITE_WEBP_QUALITY), self.quality)
        #
        self.out = None
        self.orig = None  # обрабатываемый кадр
        self.yolo = None  # кадр из Yolo
        self.test = None  # схем + yolo
        self.schm = None  # выходная схема
        self.handler = handler
    
    def run(self): # Запуск в основном потоке OpevCV
        self.lock = threading.Lock()
        threading.Thread(target=self.reader, daemon=True).start()
        
    def reader(self):
        if not (self.cap is None or self.cap.isOpened()):
            print('camera open failed')
            return
        
        while True:
            ret_val, self.out = self.cap.read()
            
    def writer(self):
        if self.out is None: return
        self.orig = self.out.copy()
        self.schm, self.test, self.yolo = self.handler(self.out)
        self.out = None
    
    def generate(self, name):
        while True:
            with self.lock:
                self.writer()
                (flag, encodedImage) = cv2.imencode(".webp", getattr(self, name), self.codec)
                if not flag: continue
            yield self.data(encodedImage)
    
    def data(self, img):
        return (b'--frame\r\n' b'Content-Type: image/webp\r\n\r\n' + 
                    bytearray(img) + b'\r\n')
        
    def __close__(self):
        if self.cap is not None:
            self.cap.release()
        cv2.destroyAllWindows()