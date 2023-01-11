import torch
import cv2
import numpy as np
from PIL import Image
import torchvision.transforms as T

import norfair
from norfair import Detection, Paths, Tracker, Video


class Model():
    #runs/train/nano6/weights/best.pt
    def __init__(self,weights='runs/train/exp10/weights/best.pt',device=None,conf=0.5):
        if device is not None and 'cuda' in device and not torch.cuda.is_available():
            raise Exception("Selected device='cuda', but cuda is not available to pytorch")
        elif device is None:
            device0 = 'cuda:0' if torch.cuda.is_available() else 'cpu'
            device1 = 'cuda:1' if torch.cuda.is_available() else 'cpu'

        self.model = torch.hub.load('.', 'custom', path=weights, device=device0, source='local')
        self.modelx = torch.hub.load('ultralytics/yolov5', 'yolov5x', device=device0)
        self.model.conf = conf
        self.modelx.conf = 0.3
        #self.model.iou = 0.45

        self.tracker = Tracker(
            distance_function = 'iou',
            distance_threshold=0.7
        )
        
    def predict(self,frame):
        frame = Image.fromarray(frame)
        res = self.model(frame)
        # MOVE PREDICTION MANIPULATION HERE??
        #print(res.xyxy[0])
        return res

    def track(self,frame):
        #frame = Image.fromarray(frame)
        res = self.modelx(frame)
        
        norfairs: List[Detection] = []
        predictions = res.xyxy[0]
        for detection in predictions:
            bbox = np.array([
                [detection[0].item(),detection[1].item()],
                [detection[2].item(),detection[3].item()]
            ])
            scores = np.array([detection[4].item(),detection[4].item()])
            norfairs.append(Detection(
                points=bbox,scores=scores,label=int(detection[-1].item())
            ))

        tracked = self.tracker.update(detections=norfairs)
        print('tracked: ', tracked)
        
        norfair.draw_points(frame,norfairs)
        norfair.draw_tracked_boxes(frame,tracked)
        
        return tracked

    def display():
        im = self.results.ims[0]
        img = cv2.imshow('stream',im)

