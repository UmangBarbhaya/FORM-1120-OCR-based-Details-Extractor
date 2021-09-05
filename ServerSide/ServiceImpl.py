from ServerSide import Preprocess, Tesseract, Zoning
import numpy as np
import cv2


class ServiceImpl:

    def __init__(self, img):
        self.img = img

    def serviceImpl(self):

        # convert string data to numpy array
        img=self.img
        # Pre-processing
        obj = Preprocess.Preprocess(img)
        img = obj.preprocess()
        # Zoning and OCR
        obj1 = Zoning.Zoning(img)
        data = obj1.zoning()

        #dates = {"Julian": 25, "Bob": 26, "Dan": 47, "Cornelius": 3}
        return data

