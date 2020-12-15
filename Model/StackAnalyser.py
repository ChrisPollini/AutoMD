import csv
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
from Model.DataHolder import DataHolder as DH


def analyse_stack(effective, spatial):
    __histogram_of_images(DH.PreProcessedImageStack)
    __percentile_calculation(DH.PreProcessedImageStack)
    __effective_calculation(DH.percentileOfImgData)

    idxOkLayer = [[], []]
    for i in range(0, len(DH.effectiveResolution)):
        idxOkLayer[i] = __longest_vector_segment(DH.effectiveResolution[i],
                                                 __default_or_user_given(effective, "effective"))

    idxOkSlice = __find_common_index_area(idxOkLayer)
    DH.Graphs.append(__create_graph(DH.effectiveResolution, idxOkLayer, idxOkSlice, "effective resolution",
                                    "Percentile range [99th-1st]"))

    idxOkLayerCorrelation, correlationBetweenSlices = __spatial_correlation(
        DH.PreProcessedImageStack, 'vertical', __default_or_user_given(spatial, "correlation")
    )

    idxOkSliceCorrelation = __find_common_index_area(idxOkLayerCorrelation)

    DH.Graphs.append(__create_graph(correlationBetweenSlices, idxOkLayerCorrelation,
                                    idxOkSliceCorrelation, "spatial corr between slices", "Pearson's r"))

    idxOkWithinLayerCorrelation, correlationInImages = __spatial_correlation(
        DH.PreProcessedImageStack, 'horizontal', __default_or_user_given(spatial, "correlation")
    )

    idxOkWithinSliceCorrelation = __find_common_index_area(idxOkWithinLayerCorrelation)

    DH.Graphs.append(__create_graph(correlationInImages, idxOkWithinLayerCorrelation,
                                    idxOkWithinSliceCorrelation, "spatial corr within slices", "Pearson's r"))

    __cut_images_from_stack(DH.PreProcessedImageStack, idxOkSliceCorrelation[0], idxOkSliceCorrelation[1])


def __default_or_user_given(data, type):
    if type == "correlation":
        pureData = data.replace(" ", "")
        if '.' in pureData:
            split_number = data.split('.')
            if len(split_number) == 2 and split_number[0].isdigit() and split_number[1].isdigit():
                thr = float(pureData)
                print(thr)
            else:
                thr = 0.78
                print("Default threshold value will be used! (Threshold = 0.78)")
        else:
            thr = 0.78
            print("Default threshold value will be used! (Threshold = 0.78)")
    else:
        pureData = data.replace(" ", "")
        if pureData.isdigit():
            thr = int(pureData)
            print(thr)
        else:
            thr = 45
            print("Default threshold value will be used! (Threshold = 45)")
    return thr


def __histogram_of_images(smoothedData):
    for smoothChannel in range(0, len(smoothedData)):
        for smoothImg in range(0, len(smoothedData[smoothChannel])):
            hist = np.histogram(smoothedData[smoothChannel][smoothImg], bins=np.arange(257), density=False)
            DH.histogramOfImages[smoothChannel].append(hist[0])


def __percentile_calculation(smoothedData):
    for smoothChannel in range(0, len(smoothedData)):
        for smoothImg in range(0, len(smoothedData[smoothChannel])):
            percentiles = [np.percentile(smoothedData[smoothChannel][smoothImg], 1, interpolation='midpoint'),
                           np.percentile(smoothedData[smoothChannel][smoothImg], 99, interpolation='midpoint')]
            DH.percentileOfImgData[smoothChannel].append(percentiles)


def __effective_calculation(percentileData):
    for percentileChannel in range(0, len(percentileData)):
        effective = np.squeeze(np.diff(percentileData[percentileChannel], 1, 1))
        DH.effectiveResolution.append(effective.tolist())


def __longest_vector_segment(inputArray, thr):
    boolEff = []
    for i in range(0, len(inputArray)):
        if inputArray[i] > thr:
            boolEff.append(1)
        else:
            boolEff.append(0)

    temp = [[boolEff[0], 0, None, None]]

    k = 0
    for i in range(1, len(boolEff)):
        if boolEff[i] != temp[len(temp) - 1][0]:
            temp[k][2] = i - 1
            temp[k][3] = i - temp[k][1]
            temp.append([boolEff[i], i, None, None])
            k += 1

    temp[k][2] = len(boolEff)
    temp[k][3] = len(boolEff) - temp[k][1] + 1

    newTemp = []
    for i in range(0, len(temp)):
        if temp[i][0] > 0:
            newTemp.append(temp[i])

    m = newTemp[0]
    for i in range(1, len(newTemp)):
        if newTemp[i][3] > m[3]:
            m = newTemp[i]

    idx1, idx2 = (m[1], m[2])
    return idx1, idx2


def __find_common_index_area(indexes):
    idxOkSlice = [max(indexes[0][0], indexes[1][0]), min(indexes[0][1], indexes[1][1])]
    return idxOkSlice


def __mean(x):
    y = np.sum(x) / np.size(x)
    return y


def __corr2(a, b):
    a = a - __mean(a)
    b = b - __mean(b)
    r = np.sum(a * b) / np.sqrt(np.sum(a * a) * np.sum(b * b))
    return r


def __spatial_correlation(imgStack, direction, thr):
    nL = len(imgStack)  # layer
    nS = len(imgStack[0])  # slice

    if direction == 'vertical':
        spatialCorr = [[], []]

        for iL in range(0, nL):
            for iS in range(0, nS - 1):
                spatialCorr[iL].append(__corr2(imgStack[iL][iS + 1], imgStack[iL][iS]))

    elif direction == 'horizontal':
        spatialCorrWithin = [[], []]

        spatialCorr = [[], []]

        for iL in range(0, nL):
            for iS in range(0, nS):
                spatialCorrWithin[iL].append([])

                spatialCorrWithin[iL][iS].append(
                    __corr2(imgStack[iL][iS][:-1, :-1],
                            imgStack[iL][iS][1:, 1:]))

                spatialCorrWithin[iL][iS].append(
                    __corr2(imgStack[iL][iS][1:, :-1],
                            imgStack[iL][iS][:-1, 1:]))

                spatialCorrWithin[iL][iS].append(
                    __corr2(imgStack[iL][iS][:-1, :],
                            imgStack[iL][iS][1:, :]))

                spatialCorrWithin[iL][iS].append(
                    __corr2(imgStack[iL][iS][:, :-1],
                            imgStack[iL][iS][:, 1:]))

                spatialCorr[iL].append(np.mean(spatialCorrWithin[iL][iS]))

        if nL == 1:
            spatialCorr = np.transpose(spatialCorr)

    spatialCorrSmoothed = []

    for iL in range(0, nL):
        spatialCorrSmoothed.append(__smooth_moving_average(spatialCorr[iL][:], 2, 1))

    if direction == 'vertical':
        with open('verticalSpatial.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(spatialCorrSmoothed)

    elif direction == 'horizontal':
        with open('horizontalSpatial.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(spatialCorrSmoothed)

    idxOkLayerSp = [[], []]

    for iL in range(0, nL):
        idxOkLayerSp[iL] = __longest_vector_segment(spatialCorrSmoothed[iL], thr)

    return idxOkLayerSp, spatialCorrSmoothed


def __smooth_moving_average(y, w, behaviourEdges):
    yt = []
    nY = len(y)
    if w is None:
        w = 3

    if behaviourEdges is None:
        behaviourEdges = 1

    if behaviourEdges == 1:

        for i in range(w, w + nY):
            yt.append(np.nanmean(y[i - w:i + w]))

    else:
        for i in range(0, nY):
            k1 = i - 1
            k2 = nY - i
            if k1 > w:
                k1 = w
            if k2 > w:
                k2 = w
            yt[i] = np.nanmean(y[i - k1:i + k2])

    return yt


def __cut_images_from_stack(stack, startIndex, stopIndex):
    for iL in range(0, len(stack)):
        for iS in range(startIndex, stopIndex + 1):
            DH.CutImageStack[iL].append(DH.PreProcessedImageStack[iL][iS])


def __create_graph(data, allIndexes, okIndexes, title, ylabel):
    fig = Figure(figsize=(4, 4), dpi=256)
    ax = fig.add_subplot(111)

    ax.plot(data[0], label="DAPI", color='red')
    ax.plot(data[1], label="Alx", color='blue')

    ax.axvline(min(allIndexes[0][0], allIndexes[1][0]), color='purple')
    ax.axvline(max(allIndexes[0][1], allIndexes[1][1]), color='purple')

    ax.axvline(okIndexes[0], color='green')
    ax.axvline(okIndexes[1], color='green')

    ax.set_title(title, fontsize=20)
    ax.set_xlabel('Slices', fontsize=18)
    ax.set_ylabel(ylabel, fontsize=18)
    ax.legend()

    canvas = FigureCanvasAgg(fig)
    canvas.draw()

    figRGB = canvas.renderer.tostring_rgb()
    ncols, nrows = canvas.get_width_height()
    figNP = np.fromstring(figRGB, dtype=np.uint8).reshape(nrows, ncols, 3)

    return figNP
