import numpy
import cv2
import wx

def wxBitmapFromCvImage(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    height, width = image.shape[:2]
    bitmap = wx.BitmapFromBuffer(width, height, image)
    return bitmap

