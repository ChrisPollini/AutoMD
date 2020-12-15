import numpy as np
import os
import cv2
from PIL import Image
from Model.DataHolder import DataHolder as DH


def change_contrast(imgC, level):
    factor = (259 * (level + 255)) / (255 * (259 - level))

    def contrast(c):
        value = 128 + factor * (c - 128)
        return max(0, min(255, value))

    return imgC.point(contrast)


def preprocess_images():
    for ch in range(0, len(DH.RawImageStack)):
        for img in range(0, len(DH.RawImageStack[ch])):
            img8 = (DH.RawImageStack[ch][img] / 256).astype(np.uint8)
            darken = np.where((255 - img8) == 255, 0, np.where((255 - img8) < 125, 255, img8 + 125))

            darkenToImage = Image.fromarray(darken)
            contrastedDarkenImage = change_contrast(darkenToImage, 300)
            contrastedToArray = np.asarray(contrastedDarkenImage)

            #blur = cv2.bilateralFilter(contrastedToArray, 4, 75, 75)
            blur = cv2.medianBlur(contrastedToArray, 5)
            DH.PreProcessedImageStack[ch].append(blur)
            if ch == 0:
                DH.PreProcessedDAPI.append(blur)
            else:
                DH.PreProcessedAlx647.append(blur)
    print('I finished the for')



