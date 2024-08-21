import cv2
import sys

from settings import *

tracker_types = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']

from History import *

class TSwimer2(THistory):
    #tracker_type = 'KCF'
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

    @staticmethod
    def Init(cls, tracker_type, detect):
        cls.detect = detect
        cls.tracker_type = tracker_type

    def __init__(self, Pos, Sz = 10):

        super().__init__(20, 3)

        self.X = Pos[1]
        self.Y = Pos[2]
        self.Class = Pos[0]

        self.append(Pos)

        self.YStep = True

        self.IsNew = 0 #

        self.Skipping = 0

        tracker_type = TSwimer2.tracker_type
        if int(TSwimer2.minor_ver) < 3:
            tracker = cv2.Tracker_create(tracker_type)
        else:
            if tracker_type == 'BOOSTING':
                tracker = cv2.TrackerBoosting_create()
            if tracker_type == 'MIL':
                tracker = cv2.TrackerMIL_create()
            if tracker_type == 'KCF':
                tracker = cv2.TrackerKCF_create()
            if tracker_type == 'TLD':
                tracker = cv2.TrackerTLD_create()
            if tracker_type == 'MEDIANFLOW':
                tracker = cv2.TrackerMedianFlow_create()
            if tracker_type == 'GOTURN':
                tracker = cv2.TrackerGOTURN_create()
            if tracker_type == 'MOSSE':
                tracker = cv2.TrackerMOSSE_create()
            if tracker_type == "CSRT":
                tracker = cv2.TrackerCSRT_create()

        self.tracker = tracker



    def Yolo(self, bbox, Frame):
        ok = self.tracker.init(Frame, bbox)
        self.Point = (int(bbox[0] + bbox[2] / 2), int(bbox[1] + bbox[3] / 2))

    def Tracking(self, Frame):
        ok, bbox = self.tracker.update(Frame)

        if ok:
            # Tracking success
            self.Point = (int(bbox[0] + bbox[2]/2), int(bbox[1] + bbox[3]/2))

            return True
        else:
            # Tracking failure
            return False

    def Draw(self, Img, Add):
        if self.Skipping > SkeepingCount or self.IsNew < SkeepingCount:
            return Img

        Img1 = Img.copy()
        return cv2.circle(Img1, (int(self.X*WinK + Add[0]), int(self.Y*WinK + Add[1])), Radius, Colors[int(self.Class)], thickness=-1)