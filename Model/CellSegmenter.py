import numpy as np
import cv2
from Model.DataHolder import DataHolder as DH

def segment_cells_into_parts():

    kernel = np.ones((3, 3), np.uint8)

    detectedBranches = []
    detectedBorder = []
    detectedSoma = []
    detectedNucleus = []

    for i in range(0, len(DH.CutImageStack[1])):
        _, thresh = cv2.threshold(DH.CutImageStack[1][i], 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        detectedBranches.append(thresh)

        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=7)
        distanceTransform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
        detectedBorder.append(distanceTransform)

        _, foreGroundSoma = cv2.threshold(distanceTransform, 0.2 * distanceTransform.max(), 255, 0)
        detectedSoma.append(foreGroundSoma)

        _, foreGround = cv2.threshold(distanceTransform, 0.5 * distanceTransform.max(), 255, 0)
        detectedNucleus.append(foreGround)

    blackImageStack = []
    for img in range(0, len(DH.CutImageStack[1])):
        blackImageStack.append(np.zeros((1024, 1024, 3), np.uint8))

    detectedBranchesNumpy = np.array(detectedBranches)
    detectedBorderNumpy = np.array(detectedBorder)
    detectedSomaNumpy = np.array(detectedSoma)
    detectedNucleusNumpy = np.array(detectedNucleus)
    blackImageStackNumpy = np.array(blackImageStack)

    blackImageStackNumpy[detectedBranchesNumpy > 0] = [0, 204, 0]
    blackImageStackNumpy[detectedBorderNumpy > 0] = [255, 76, 204]
    blackImageStackNumpy[detectedSomaNumpy > 0] = [255, 0, 0]
    blackImageStackNumpy[detectedNucleusNumpy > 0] = [0, 255, 255]

    DH.SegmentedImages = blackImageStackNumpy

