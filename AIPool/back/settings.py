import os
import numpy as np

Debug = False
DebugOut = False
DebugPath = 'e:/Bas/Test3'
CommonMode = False # совмещаем кадр и схему
# размер бассейна на картинке
BassWidth, BassHeight = 1800, 1430

WinK = 1

DXLimit = 12000
DYLimit = 65000


# Сколько пропускаем пустых
SkeepingCount = 4

#Радиус метки
Radius = 20

RefrashTime = 0.1 # время обновления экрана в секундах

out_water = 0# человек находится на суше
horiz_above_water = 1# человек находится в бассейне горизонтально, голова человека находится над водой
horiz_under_water = 2# человек находится в бассейне горизонтально, голова человека находится над водой
vert_above_water = 3 # человек находится в бассейне вертикально, голова человека находится над водой
vert_under_water = 4 # человек находится в бассейне вертикально, голова находится под водой
water = 5 # водная поверхность бассейна
Colors = [(255, 255, 255), (0, 255, 0), (0, 255, 0), (0, 255, 0), (0, 255, 0), (0, 0, 128)]

WaterBox = np.array([700, 0, 1800, 1430], dtype = np.float32)

LabelCaptions = ['out_water', 'horiz_above_water', 'horiz_under_water', 'vert_above_water', 'vert_under_water', 'water']

BassSize = np.array( (BassWidth, BassHeight))