import numpy as np
import torch
import pandas as pd
import os

StepInd = 0

class Bass_detect:
    
    def __init__(self):
        path_model = os.path.join('model', os.getenv('MODEL_NAME'))
        path_best = os.path.join('model', 'best', os.getenv('MODEL_BEST') )
        self.model = torch.hub.load(path_model, 'custom', path=path_best, source='local')
        
    def detect_human(self, img):
        self.results = self.model(img)
        df = self.results.pandas().xyxy[0]

        global StepInd

        StepInd+= 1
        
        df = df.drop(np.where(df['confidence'] < 0.3)[0])
        ob = pd.DataFrame()
        ob['class'] = df['name']
        ob['x'] = df['xmin']
        ob['y'] = df['ymin']
        ob['w'] = df['xmax'] - df['xmin']
        ob['h'] = df['ymax'] - df['ymin']
        oblasty = ob.values.tolist()
        return oblasty