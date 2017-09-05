import numpy
import cv2

def cvResizeAspectFill(src, maxSize, upInterpolation = cv2.INTER_LANCZOS4, downInterpolation = cv2.INTER_AREA):
    height, width = src[:2]
    if width > height:
        if width > maxSize:
            interpolation = downInterpolation
        else:
            interpolation = upInterpolation

        height = int(maxSize * height / float(width))
        width = maxSize
    else:
        if height > maxSize:
            interpolation = downInterpolation
        else:
            interpolation = upInterpolation
        width = int(maxSize * width / float(height))
        height = maxSize

    dst = cv2.resize(src, (width, height), interpolation = interpolation)
    return dst

