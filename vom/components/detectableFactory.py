from vom.utils.singleton import Singleton
from vom.components.detectable.detectable import Detectable
from vom.components.detectable.gate import Gate
from vom.components.detectable.car import Car
from vom.components.detectable.sign import Sign
from vom.components.boundingBox import BoundingBox

class DetectableFactory(metaclass=Singleton):

    def __init__(cls,resulution,padding=8):
        cls.resolution = resulution
        cls.test = 'test'
        cls.padding = padding

    def testing(cls):
        print(cls.test)

    def create_detected_objects(cls,predictions):
        result = []

        df = predictions.pandas().xyxy[0]
        #print(df)
        for id, obj in df.iterrows():

            xmin = int(obj.xmin) - cls.padding
            ymin = int(obj.ymin) - cls.padding
            xmax = int(obj.xmax) + cls.padding
            ymax = int(obj.ymax) + cls.padding

            bounding_box = BoundingBox(xmin,ymin,xmax,ymax)
            #if obj[5] == 0:
                #print('bike')
            if obj[5] == 1:
                #print('car')
                result.append(Car(bounding_box))
            #if obj[5] == 2:
                #print('cross')
            if obj[5] == 3:
                result.append(Gate(bounding_box))
            #if obj[5] == 4:
            #if obj[5] == 5:
                #print('pole')
            #if obj[5] == 6:
               #print('signoff')
            #if obj[5] == 7:
            #if obj[5] == 8:
            #if obj[5] == 9:
            

        return result
