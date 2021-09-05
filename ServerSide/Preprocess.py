import cv2
import cv2
import numpy as np
from scipy import ndimage
from PIL import Image, ImageChops
import math


class Preprocess:
    def __init__(self, img):
        self.img = img

    def preprocess(self):
        img = self.img

        # Converting image to gray scale
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Removing Noise from Image by Dilating, Eroding and Gaussian Blur
        kernel = np.ones((1, 1), np.uint8)
        img = cv2.dilate(img, kernel, iterations=1)
        img = cv2.erode(img, kernel, iterations=1)
        img = cv2.GaussianBlur(img, (3, 3), 0)

        # Binarization
        img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        # Trimming the White Space
        im = Image.fromarray(img)
        bg = Image.new(im.mode, im.size, im.getpixel((0, 0)))
        diff = ImageChops.difference(im, bg)
        diff = ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.getbbox()
        img1 = im.crop(bbox)
        img = np.asarray(img1)

        # detecting the Edges using Canny Edge detector
        edges = cv2.Canny(img, 50, 150, apertureSize=3)
        cv2.imwrite(
            'C:/Users/UmangRB/Desktop/Ex_Files_Deep_Learning_Face_Recog/final_tess/Intermediary/houghlineedges.jpg',
            edges)

        # Finding the Lines using HoughLineP
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=500, maxLineGap=10)
        n, m, l = np.shape(lines)

        # Sorting the Lines
        array = np.empty([n, l])
        for i in range(0, n):
            array[i, 0] = int(lines[i, 0, 0])
            array[i, 1] = int(lines[i, 0, 1])
            array[i, 2] = int(lines[i, 0, 2])
            array[i, 3] = int(lines[i, 0, 3])
        array = np.int64(array)
        array = array[array[:, 1].argsort()]
        angles = []
        for i in range(0, n):
            x1, y1, x2, y2 = array[i]
            if abs(y2 - y1) < 15:
                angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
                angles.append(angle)
            print(array[i])
        print(angles)
        median_angle = 1.1111111
        median_angle = np.mean(angles)
        print(median_angle)
        img = ndimage.rotate(img, median_angle, cval=255)

        im = Image.fromarray(img)
        bg = Image.new(im.mode, im.size, im.getpixel((0, 0)))
        diff = ImageChops.difference(im, bg)
        diff = ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.getbbox()
        img1 = im.crop(bbox)
        img = np.asarray(img1)

        width = 4250
        height = 5500
        dim = (width, height)
        img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        img = cv2.resize(img, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
        return img

