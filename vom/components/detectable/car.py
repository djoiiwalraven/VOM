import cv2
import time
import numpy as np
from vom.components.detectable.detectable import Detectable
from vom.utils import detection

class Car(Detectable):
    def __init__(self,*args, **kwargs):
        super(Car,self).__init__(*args, **kwargs)
        self.color = (255,0,255)

    def analysis(self,frame):
        print('calculate speed here')
            

    