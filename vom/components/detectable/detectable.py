import cv2
from vom.utils import detection

class Detectable():
    def __init__(self,bounding_box):
        self.bb = bounding_box
        self.color = (0,0,255)

    def draw_box(self,frame,thickness=2):
        box = cv2.rectangle(frame,self.bb.start,self.bb.end,self.color,thickness)
    
    def get_box_dim(self):
        return self.bb[0], self.bb[1], self.bb[2], self.bb[3]

    def analysis(self,frame):
        raise NotImplementedError('I need to be implemented!')
    