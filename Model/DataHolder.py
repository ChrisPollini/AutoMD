import os

class DataHolder:

    #DataExtractor / 1st page: BrowsePage
    pathToFile = ""
    fileNameWithExtension = ""
    fileNameWithoutExtension = ""
    defaultOutputFolder = os.getcwd()
    defaultOutputPath = defaultOutputFolder + "\\Output_"
    updatedOutputPath = "" #Default + FileName path
    Metadata = {}
    RawDAPI = [] #hidden on window
    RawAlx647 = [] #hidden on window
    RawImageStackTemp = [] #hidden on window
    RawImageStack = [RawDAPI, RawAlx647]

    #ImagePreProcessor / 2nd page: PreProcessPage
    PreProcessedOutputPath = ""
    PreProcessedDAPI = []
    PreProcessedAlx647 = []
    PreProcessedImageStack = [[], []]

    #StackAnalyser / 3rd page: ProcessedPage
    GraphOutputPath = ""
    histogramOfImages = [[], []]
    percentileOfImgData = [[], []]
    effectiveResolution = []
    Graphs = []
    CutImageStack = [[], []]

    #CellSegmenter / 4th page: SegmentPage
    SegmentedOutputPath =""
    SegmentedImages = []
