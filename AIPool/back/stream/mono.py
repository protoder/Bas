import os
import numpy as np
from stream.stream import Stream
import cv2

class StreamMono(Stream):
    
    def __init__(self, *arg, **kword):
        super().__init__(*arg, **kword)
    
    def run(self):
        pass
        
    def generate(self, name):
    
        if not (self.cap is None or self.cap.isOpened()):
            print('camera open failed')
            yield None
            
        while True:
        
            ret_val, out = self.cap.read()
            
            if out is None: continue
            
            img = out.copy()
            
            if 'schm' == name:
                img, _, _ = self.handler(out)     
            if 'test' == name:
                _, img, _ = self.handler(out)  
            if 'yolo' == name:    
                _, _, img = self.handler(out)
            
            (flag, encodedImage) = cv2.imencode(".webp", img, self.codec)
            if not flag: continue
 
            yield self.data(encodedImage)