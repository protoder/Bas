import sys, os
path_cur = os.path.dirname(os.path.abspath(__file__))
path_parent = os.sep.join(path_cur.split(os.sep)[:-1])
sys.path.insert(0, path_parent)

from model.bass import Bass_detect, StepInd
from settings import *

import cv2
import time
import numpy as np

import matplotlib.pyplot as plt

cwd = os.getcwd()

CrShot = 0 # текущий прочитанный кадр

if cwd.endswith('back'):
    os.chdir('../')
# Определяет парметры последней отправки картинки во фронт
SendTime = time.time()
SendIndex = 0
CrIndex = 0
Drawings = 0


detect = Bass_detect()

class THistory:
    def __init__(self, Sz, Dim):
        self.Count = Sz
        self.Pos = Sz - 1
        self.QueueSz = 0
        self.List = np.zeros( (Sz, Dim), dtype = np.float32)
        self.Speed = np.zeros(Sz, dtype=np.float32)

        self.LastY = 0


    def GetList(self):
        if self.QueueSz < self.Count:
            return self.List[-self.QueueSz:]

        return self.List[-self.Pos:].append(self.List[:self.Pos], axis = 0)

    def GetItem(self, Index):
        Index = self.Pos + Index + 1

        if Index >= self.Count:
            Index -= self.Count

        return Index

    def __iter__(self):
        return self.GetList().__iter__()

    def __getitem__(self, key):
        return self.List[self.GetItem(key)]

    def __setitem__(self, key, value):
        Item = self.GetItem(key)
        self.List[Item: Item + 1] = value

    def append(self, Item):
        self.List[self.Pos, :] = Item

        if self.Pos == 0:
            self.Pos = self.Count - 1
        else:
            self.Pos -= 1

            if self.QueueSz < self.Count:
                self.QueueSz += 1

class TSwimer(THistory):
    def append(self, Item):

        super().append(Item)
       

    def __init__(self, Pos, Sz = 10):

        super().__init__(20, 3)

        self.X = Pos[1]
        self.Y = Pos[2]
        self.Class = Pos[0]

        self.append(Pos)

        self.YStep = True

        self.IsNew = 0 #

        self.Skipping = 0

    def TryItem(self, CrSwimers, Mask):
        global DXLimit
        global DYLimit
        MinPos = None
        MinD = 10000000
        MinIndex = 0
        self.IsNew += 1
        for i, Pos in enumerate(CrSwimers):

            if Mask[i] == 0 or Pos[0] == water: # 0 признак того, что пловец уже занят или это не пловец
                continue

            Cr_DX = (Pos[1] - self.X)**2 # ищем точки в окрестностях пловца
            Cr_DY = (Pos[2] - self.Y)**2

            if Cr_DX < DXLimit and Cr_DY  < DYLimit:
                if Cr_DX + Cr_DY < MinD:
                    MinD = Cr_DX + Cr_DY
                    MinPos = Pos
                    MinIndex = i # берем наиближайшую из свободных точек

        if MinPos is not None:
            self.append(MinPos) # должен быть одномерный или [1,...]

            Mask[MinIndex] = 0

            self.Skipping = 0 #cчетчик пропущенных кадров. Через какое-то время пловец пропадает

            self.X, self.Y = np.sum(self.List[-self.QueueSz:, 1:3], 0) / self.QueueSz
            #Sz = min(4, self.QueueSz)
            #self.Y = np.sum(self.GetList()[-self.QueueSz:(Sz - self.QueueSz) if self.QueueSz > 4 else None, 2], 0) / Sz
            #self.X = np.sum(self.List[-self.QueueSz:, 1], 0) / self.QueueSz
            # обрабатываем изменения
            '''X = np.sum(self.List[:, 1])/self.QueueSz
            self.Y = np.sum(self.List[:, 2]) / self.QueueSz'''

            '''if (X - self.X) ** 2 > DXLimit:
                self.X = X#горизонтальную координату меняем только при существенном смещение'''

            self.Class = MinPos[0]

        else:
            self.Skipping += 1

        return Mask

    def Draw(self, Img, Add):
        if self.Skipping > SkeepingCount or self.IsNew < SkeepingCount:
            return Img

        Img1 = Img.copy()
        return cv2.circle(Img1, (int(self.X*WinK + Add[0]), int(self.Y*WinK + Add[1])), Radius, Colors[int(self.Class)], thickness=-1)

class TSwimers():
    def __init__(self):
        self.List = []

    def Add(self, CrSwimers):
        Mask = np.ones(len(CrSwimers))
        # Разбираем пловцов
        for Swimer in self.List:
            Mask = Swimer.TryItem(CrSwimers, Mask)

        # Пристраиваем не разобранных
        for i, CrMask in enumerate(Mask):
            if CrMask == 1:
                Item = CrSwimers[i];

                self.List.append(TSwimer(Item))

        # Удаляем "исчезнувших" пловцов
        Sz = len(self.List)

        i = len(self.List) - 1

        while i >= 0:
            Swimer = self.List[i]
            if Swimer.Skipping >= SkeepingCount:
                del self.List[i]

            i -= 1

#History = THistory(Sz = 10, Dim = 3)
Swimers = TSwimers()
SkipImg = np.zeros( (30, 30, 3))

def ProcessShot(detect, Shot):
    global CrIndex      # 
    global SendTime     #
    global SendIndex    #
    global Drawings     #
    global WaterBox     #
    global DebugPath    #

    result = detect.detect_human(Shot)

    Res = np.zeros((len(result), 3), dtype=np.float32)

    i = 0

    for BBox in result:
        Code = int(BBox[0][0])
       
        if Code != water:
            Res[i:i + 1, :] = (Code, BBox[1] + BBox[3] / 2, BBox[2] + BBox[4] / 2)
            i += 1

    #if CommonMode:
    Img0 = DrawBassReal(Shot, result)
   
    if CrIndex == 141:
        a = 0

    Res = Res[:i]

    if not CommonMode:
        Res[:, 1:3] -= WaterBox[0:2]  # учитываем координаты бассейна

        Res[:, 1:3] *= (BassSize / WaterBox[2:])

    Res.astype(np.int32)

    Swimers.Add(Res)
    #History.append(Res)

    ResOut = None
    Img = None


    CrTime = time.time()
    CrIndex += 1

    Scheme = None
    BasSheme = None
    if CrTime - SendTime > RefrashTime:

        ResOut = Res # ProcessHistory(History, CrIndex - SendIndex)

        # рисуем бассейн
        Scheme, BasSheme = DrawBassSheme(Swimers, Img0)

        SendTime = CrTime
        SendIndex = CrIndex

        Drawings += 1

        if DebugOut:
            cv2.imwrite(f'{DebugPath}/Sheme{CrIndex}.jpg', Scheme)
            cv2.imwrite(f'{DebugPath}/Dbg{CrIndex}.jpg', BasSheme)
            cv2.imwrite(f'{DebugPath}/Inp{CrIndex}.jpg', Img0)

    return Scheme, BasSheme, Img0



def DrawBassSheme(Swimmers, Bas):
    SchemeImg = np.zeros((int(BassHeight * WinK) + 16, int(BassWidth * WinK) + 16, 3))

    # Рисуем
    SchemeImg = cv2.rectangle(SchemeImg, (8, 8), (8 + int(BassWidth * WinK), 8 + int(BassHeight * WinK)), (128, 0, 0), -1)  #



    for Swimmer in Swimmers.List:
        SchemeImg = Swimmer.Draw(SchemeImg, (0,0))
        Bas = Swimmer.Draw(Bas, WaterBox[0:2])

    return SchemeImg, Bas


def DrawBassReal(Shot, result):
    for BBox in result:
        Code = int(BBox[0][0])

        if Code != water:
            Shot = cv2.rectangle(Shot, (int(BBox[1]),int(BBox[2])),(int(BBox[1]+BBox[3]),int(BBox[2]+BBox[4])),(0, 255, 0), thickness = 2)

        #text = LabelCaptions[Code]

        #Shot = cv2.putText(Shot, text, (int(BBox[1]), int(BBox[2] - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.2, (0, 0, 0), 1)
            # Отобразить изображение

    return Shot