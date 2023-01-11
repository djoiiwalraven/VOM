import cv2
import time
import numpy as np
from vom.components.detectable.detectable import Detectable
from vom.utils import detection

class Gate(Detectable):
    def __init__(self,*args, **kwargs):
        super(Gate,self).__init__(*args, **kwargs)
        self.line_threshold = 50
        self.line = None
        self.angle = None

    def _calculate_angle(self):
        if self.line is not None:
            rho, theta = self.line
            angle = theta / np.pi * 180
            angle = np.round(min(angle, 180 - angle),2)
            #print(f'HOEK: {angle}deg')
            self.angle = angle

    def _calculate_line(self,frame):
        lines = cv2.HoughLines(frame, 1, np.pi/180, self.line_threshold)
        if lines is not None:
            locations = np.array(lines)
            m = np.amax(locations)
            d = np.where(locations == m)
            self.line = locations[d[0]][0][0]

    def analysis(self,frame): # INSERT FG MASK?
        frame = self.bb.manual_crop(frame)
        #frame, amount = detection.motion(self.bb.manual_crop(frame))
        if detection.calculate_motion(frame) > 10:
            #cv2.imshow('analysis',frame)
            self._calculate_line(frame)
            self._calculate_angle()
            

    def write_angle(self,frame,color=(0,0,255),thickness=2):
        if self.angle is not None:
            org = self.bb.end[0]-80,self.bb.start[1]+24
            txt = "%03.0f" % self.angle + 'deg'
            cv2.putText(frame, str(txt), org, 1,2,color, thickness, cv2.LINE_AA)

    def display_line(self,frame,color=(255,0,0),thickness=2):
        if self.line is not None:
            rho, theta = self.line
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))
            line = [(x1,y1),(x2,y2)]
            cv2.line(self.bb.manual_crop(frame), line[0], line[1],color,thickness)