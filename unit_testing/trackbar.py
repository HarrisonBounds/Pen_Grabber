import cv2 as cv

class Trackbar:
    def __init__(self):
        self.max_value = 255
        self.max_value_H = 360//2
        
        self.low_H = 0
        self.low_S = 0
        self.low_V = 0
        self.high_H = self.max_value_H
        self.high_S = self.max_value
        self.high_V = self.max_value
        
        self.low_H_name = 'Low H'
        self.low_S_name = 'Low S'
        self.low_V_name = 'Low V'
        self.high_H_name = 'High H'
        self.high_S_name = 'High S'
        self.high_V_name = 'High V'
        

    def get_low_H_Pos(self, window_name):
        return cv.getTrackbarPos(self.low_H_name, window_name)
        
    def get_high_H_Pos(self, window_name):
        return cv.getTrackbarPos(self.high_H_name, window_name)
        
    def get_low_S_Pos(self, window_name):
        return cv.getTrackbarPos(self.low_S_name, window_name)
        
    def get_high_S_Pos(self, window_name):
        return cv.getTrackbarPos(self.high_S_name, window_name)
        
    def get_low_V_Pos(self, window_name):
        return cv.getTrackbarPos(self.low_V_name, window_name)
        
    def get_high_V_Pos(self, window_name):
        return cv.getTrackbarPos(self.high_V_name, window_name)
