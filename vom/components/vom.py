import numpy as np
import cv2
import os
import time

from vom.utils.singleton import Singleton
from vom.utils import detection

from vom.model import Model # FAKE MODEL for TESTING (ik zou het echte model zo snel mogelijk implementeren)

from vom.components.detectableFactory import DetectableFactory
from vom.components.detectable.detectable import Detectable
# Detected instances
from vom.components.detectable.gate import Gate
from vom.components.detectable.sign import Sign

import norfair
from norfair import Detection, Paths, Tracker, Video

class VOM(metaclass=Singleton):
    def __init__(cls,source,view_bbs=True,view_lines=True,view_angles=True,resolution=(640,640)):
        cls.source = source
        cls.view_bounding_boxes = view_bbs
        cls.view_lines = view_lines
        cls.view_angles = view_angles
        cls.resolution = resolution
        
        cls.frame_rate = 25
        cls.frame_counter = 0

        cls.cap = cls._read_source(cls.source)
        cls.start_frame = cls._resize(cls.cap.read()[1])

        cls.model = Model()
        cls.detectable_factory = DetectableFactory(cls.resolution)
        cls.detected_objects = cls.detectable_factory.create_detected_objects(cls.model.predict(cls.start_frame))

        cls.path_drawer = Paths()

    def _read_source(cls,source):
        try:
            return cv2.VideoCapture(source)
        except:
            print("Source can NOT be found!")
            print("Program is now quitting...")
            exit()

    def _resize(cls,frame):
        return cv2.resize(frame, cls.resolution)

    def _visualise_feedback(cls,frame,obj):
        if isinstance(obj, Gate):
            if cls.view_lines: obj.display_line(frame)
            if cls.view_angles: obj.write_angle(frame)
        if isinstance(obj, Sign):
            #print(obj.bb)
            pass
        if cls.view_bounding_boxes: obj.draw_box(frame)

    def _render(cls,frame):
        frame = cls._resize(frame)
        motion_frame = detection.motion(frame,dis=False)
        tracked = cls.model.track(frame)
        if detection.calculate_motion(motion_frame) >  200:
            #cls.frame_counter = 0
            cls.detected_objects = cls.detectable_factory.create_detected_objects(cls.model.predict(frame))
        else:
            cls.detected_objects = []

        for obj in cls.detected_objects:
            obj.analysis(motion_frame) 
            cls._visualise_feedback(frame,obj)
        #paths = cls.path_drawer.draw(frame,tracked)
        cv2.imshow('video_stream',frame)
        #cv2.imshow('vide0_stream',paths)
        
        
    def set_source(cls,source):
        cls.source = source

    def run(cls):
        while cls.cap.isOpened:
            success, frame = cls.cap.read()
            
            if success:
                start_time = time.process_time()
                cls._render(frame)
                end_time = time.process_time()
                print(f'process time:{end_time-start_time}')
                #cls.frame_counter += 1
                #if cls.frame_counter % cls.frame_rate == 0:
                    #cls.frame_counter = 0
                
            key = cv2.waitKey(1)
            if key == ord('q'):
                break
            if key == ord('p'):
                cv2.waitKey(-1) #wait until any key is pressed