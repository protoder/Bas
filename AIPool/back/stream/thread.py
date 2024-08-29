import os
from threading import Thread
import numpy as np
from stream.stream import Stream
import cv2

class StreamThread(Stream):
    
    def __init__(self, *arg, **kword):
        super().__init__(*arg, **kword)
    
    def run(self):
        super().run()
        Thread(target=self.thread, daemon=True).start()
        
    def thread(self):
        while True:
            with self.lock:
                self.writer()

    def generate(self, name):
        while True:
            if self.orig is None: continue
            with self.lock:
                (flag, encodedImage) = cv2.imencode(".webp", getattr(self, name), self.codec)
                if not flag: continue
 
            yield self.data(encodedImage)