from PyQt5.QtCore import pyqtSignal, QObject, Qt
from PyQt5.QtWidgets import QApplication
import Model.InputOutput as IO
import Model.DataExtractor as DE
import Model.ImagePreProcessor as PP
import Model.StackAnalyser as SA
import Model.CellSegmenter as CS
from View.MainViewer import MainViewer
from Model.DataHolder import DataHolder as DH
import time
from PyQt5 import QtCore as qtc


class MainPresenter(QObject):
    sendFolder = pyqtSignal()
    sendPath = pyqtSignal()
    sendMeta = pyqtSignal()


    ch = 0
    currentIndex = 0

    effectiveBool = False
    corrBool = False

    GraphIndex = 0

    SegmentedIndex = 0

    def __init__(self):
        super(MainPresenter, self).__init__()
        self.view = MainViewer()

        self.view.BrowseFolderClicked.connect(lambda: self.onBrowseFolderClicked())
        self.sendFolder.connect(lambda: self.view.changeFolderPathDisplay())

        # 1. tab dolgai
        self.view.BrowseClicked.connect(lambda: self.onBrowseClicked())
        self.sendPath.connect(lambda: self.view.changePathDisplay())
        self.view.LoadClicked.connect(lambda: self.onLoadClicked())
        self.sendMeta.connect(lambda: self.view.changeMetaDisplay())

        # 2. tab dolgai
        self.view.PPStartClicked.connect(lambda: self.onStartClicked())
        self.view.NextClicked.connect(lambda: self.NextClicked())
        self.view.PrevClicked.connect(lambda: self.PrevClicked())
        self.view.DapiClicked.connect(lambda: self.DapiClicked())
        self.view.AlxClicked.connect(lambda: self.AlxClicked())

        # 3. tab dolgai
        self.view.EffectiveClicked.connect(lambda: self.EffectiveClicked())
        self.view.CorrClicked.connect(lambda: self.CorrClicked())
        self.view.ExecuteClicked.connect(lambda: self.ExecuteClicked())
        self.view.NextGraphClicked.connect(lambda: self.NextGraphClicked())
        self.view.PrevGraphClicked.connect(lambda: self.PrevGraphClicked() )

        #4. tab dolgai
        self.view.BeginClicked.connect(lambda: self.BeginClicked())
        self.view.NextStepClicked.connect(lambda: self.NextStepClicked())
        self.view.PriorStepClicked.connect(lambda: self.PriorStepClicked())

        self.view.show()


    # legyen mindegyik simán "<gombnév>Clicked" ne pedig on, mert az megegyezik a MainViewerbeni naminggel.

    def onBrowseFolderClicked(self):
        IO.browseFolder()
        self.sendFolder.emit()


    def onBrowseClicked(self):
        IO.browseFile()
        self.sendPath.emit()

    def onLoadClicked(self):
        now = time.time()
        QApplication.setOverrideCursor(Qt.WaitCursor)
        DE.nd2_processor()
        QApplication.restoreOverrideCursor()
        future = time.time()

        self.view.ui.statusBar.showMessage("Loading finished in " + str(future-now) + " seconds")
        IO.save_metadata_to_csv()
        self.sendMeta.emit()


    def onStartClicked(self):
        now = time.time()
        QApplication.setOverrideCursor(Qt.WaitCursor)
        PP.preprocess_images()
        QApplication.restoreOverrideCursor()
        future = time.time()
        self.view.ui.statusBar.showMessage('Pre-processing finished')
        print('I finished the preprocess, about to start the save')
        IO.save_pre_processed_to_destination()
        self.SendImage()

    def DapiClicked(self):
        self.ch = 0
        self.SendImage()

    def AlxClicked(self):
        self.ch = 1
        self.SendImage()

    def NextClicked(self):
        self.currentIndex += 1
        self.SendImage()

    def PrevClicked(self):
        self.currentIndex -= 1
        self.SendImage()

    def SendImage(self):
        stackLen = len(DH.PreProcessedImageStack[self.ch])

        print(stackLen)
        if self.currentIndex < 0:
            self.currentIndex = stackLen - 1
        elif self.currentIndex >= stackLen:
            self.currentIndex = 0

        print(str(self.ch) + " | " + str(self.currentIndex))
        if self.ch == 0:
            self.view.ui.statusBar.showMessage("DAPI image: " + str(self.currentIndex) + " / " + str(stackLen))
        else:
            self.view.ui.statusBar.showMessage("Alx647 image: " + str(self.currentIndex) + " / " + str(stackLen))

        self.view.changePictureDisplay(self.ch, self.currentIndex)


    def EffectiveClicked(self):
        self.effectiveBool = True
        self.BothTrue()

    def CorrClicked(self):
        self.corrBool = True
        self.BothTrue()

    def BothTrue(self):
        if self.effectiveBool == True and self.corrBool == True:
            self.view.enableStartButton()
            print("enabled start button")

    def NextGraphClicked(self):
        self.GraphIndex += 1
        self.SendGraph()

    def PrevGraphClicked(self):
        self.GraphIndex -= 1
        self.SendGraph()

    def SendGraph(self):
        graphsLen = len(DH.Graphs)

        print(graphsLen)
        if self.GraphIndex < 0:
            self.GraphIndex = graphsLen - 1
        elif self.GraphIndex >= graphsLen:
            self.GraphIndex = 0

        print(self.GraphIndex)
        self.view.changeGraphDisplay(self.GraphIndex)

    def ExecuteClicked(self):
        now = time.time()
        QApplication.setOverrideCursor(Qt.WaitCursor)
        SA.analyse_stack(
            self.view.getEffectiveNum(),
            self.view.getCorrNum()
        )
        QApplication.restoreOverrideCursor()
        future = time.time()
        self.view.ui.statusBar.showMessage("Stack analysis finished in " + str(future - now) + " seconds")
        self.view.enableNextPrevButton()
        IO.create_and_save_graph()
        self.SendGraph()

    def NextStepClicked(self):
        self.SegmentedIndex += 1
        self.SendSegmented()

    def PriorStepClicked(self):
        self.SegmentedIndex -= 1
        self.SendSegmented()

    def SendSegmented(self):
        segmentedLen = len(DH.SegmentedImages)

        print(segmentedLen)
        if self.SegmentedIndex < 0:
            self.SegmentedIndex = segmentedLen - 1
        elif self.SegmentedIndex >= segmentedLen:
            self.SegmentedIndex = 0
        print(self.SegmentedIndex)
        self.view.ui.statusBar.showMessage("Segmented image: " + str(self.SegmentedIndex))
        self.view.changeSegmentDisplay(self.SegmentedIndex)

    def BeginClicked(self):
        now = time.time()
        QApplication.setOverrideCursor(Qt.WaitCursor)
        CS.segment_cells_into_parts()
        QApplication.restoreOverrideCursor()
        future = time.time()
        self.view.ui.statusBar.showMessage("Segmentation finished in " + str(future - now) + " seconds")
        IO.createVideoFromImageData()
        self.SendSegmented()

