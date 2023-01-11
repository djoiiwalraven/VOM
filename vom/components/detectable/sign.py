import cv2
import time
import numpy as np
from vom.components.detectable.detectable import Detectable
from vom.utils import detection

class Sign(Detectable):
    def __init__(self,*args, **kwargs):
        super(Sign,self).__init__(*args, **kwargs)
        self.light = False

    def analysis(self,frame):
        frame, amount = detection.motion(self.bb.manual_crop(frame))
        if amount > 1400:
            pass

    # VISUAL INDICATIONS BELOW: