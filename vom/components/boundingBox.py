class BoundingBox:
    def __init__(self, xmin, ymin, xmax, ymax):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        self.start = (xmin,ymin)
        self.end = (xmax,ymax)

    def crop(self, xmin, ymin, xmax, ymax):
        return image[ymin:ymax,xmin:xmax]

    def manual_crop(self,image):
        return image[self.ymin:self.ymax, self.xmin:self.xmax]
    
    def reset(self,image):
        self.start = (self.xmin,self.ymin)
        self.end = (self.xmax,self.ymax)
    
    def __str__(self):
        return f'{[self.xmin, self.xmax, self.ymin, self.ymax]}'