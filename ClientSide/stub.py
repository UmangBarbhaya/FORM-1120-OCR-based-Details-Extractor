from ServerSide import ServiceImpl
import cv2

filestr = 'C:/Users/H P/Desktop/UBSForm1120Extractor/input/f1120_2.jpg'
img = cv2.imread(filestr)
obj = ServiceImpl.ServiceImpl(img)
data = obj.serviceImpl()
print(data)

