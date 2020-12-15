import numpy as np
import cv2
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, QPropertyAnimation, QEasingCurve, Qt
from PyQt5.QtGui import QPixmap, QImage
from Model.DataHolder import DataHolder as DH

from . import GUI as Layout

class MainViewer(QMainWindow):

    BrowseFolderClicked = pyqtSignal()

    #1st widget
    BrowseClicked = pyqtSignal()
    LoadClicked = pyqtSignal()

    #2nd Widget
    PPStartClicked = pyqtSignal()
    DapiClicked = pyqtSignal()
    AlxClicked = pyqtSignal()
    NextClicked = pyqtSignal()
    PrevClicked = pyqtSignal()

    #3rd Widget
    EffectiveClicked = pyqtSignal()
    CorrClicked = pyqtSignal()
    ExecuteClicked = pyqtSignal()
    PrevGraphClicked = pyqtSignal()
    NextGraphClicked = pyqtSignal()

    #4th Widget
    BeginClicked = pyqtSignal()
    NextStepClicked = pyqtSignal()
    PriorStepClicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.ui = Layout.Ui_MainWindow()
        self.ui.setupUi(self)

        # string value
        title = "AutoMD"

        # set the title
        self.setWindowTitle(title)

        self.ui.MenuBrowse.clicked.connect(
            lambda: self.ui.PagesWidget.setCurrentWidget(self.ui.BrowsePage)
        )
        self.ui.MenuProcess.clicked.connect(
            lambda: self.ui.PagesWidget.setCurrentWidget(self.ui.PreProcessedPage)
        )
        self.ui.MenuAnal.clicked.connect(
            lambda: self.ui.PagesWidget.setCurrentWidget(self.ui.ProcessedPage)
        )
        self.ui.MenuSegment.clicked.connect(
            lambda: self.ui.PagesWidget.setCurrentWidget(self.ui.SegmentPage)
        )
        self.ui.SettingBttn.clicked.connect(
            lambda: self.ui.PagesWidget.setCurrentWidget(self.ui.SettingsPage)
        )

        self.ui.PathLine_2.setText(DH.defaultOutputFolder)


        self.ui.LoadBttn.setEnabled(False)

        self.ui.MenuProcess.setEnabled(False)
        self.ui.StartBttn.setEnabled(False)
        self.ui.ForwStepBttn.setEnabled(False)
        self.ui.PrevStepBttn.setEnabled(False)
        self.ui.DAPIBttn.setEnabled(False)
        self.ui.AlxBttn.setEnabled(False)

        self.ui.MenuAnal.setEnabled(False)
        self.ui.ExecuteBttn.setEnabled(False)
        self.ui.Set1.setEnabled(False) #effective button
        self.ui.Set2.setEnabled(False) #correlation button
        self.ui.PregGraph.setEnabled(False)
        self.ui.NextGraph.setEnabled(False)

        self.ui.MenuSegment.setEnabled(False)
        self.ui.BeginBttn.setEnabled(False)
        self.ui.NextStepBttn.setEnabled(False)
        self.ui.PriorStepBttn.setEnabled(False)

        #Frame stuff
        self.ui.MenuBttn.clicked.connect(lambda: self.toggleMenu())
        self.ui.BrowseBttn_2.clicked.connect(lambda: self.onBrowseFolderClicked())

        # 1. Widget
        self.ui.BrowseBttn.clicked.connect(lambda: self.onBrowseClicked())
        self.ui.LoadBttn.clicked.connect(lambda: self.onLoadClicked())

        # 2. Widget
        self.ui.StartBttn.clicked.connect(lambda: self.onStartClicked())
        self.ui.ForwStepBttn.clicked.connect(lambda: self.onNextClick())
        self.ui.PrevStepBttn.clicked.connect(lambda: self.onPrevClicked())
        self.ui.DAPIBttn.clicked.connect(lambda: self.onDapiClicked())
        self.ui.AlxBttn.clicked.connect(lambda: self.onAxlClicked())

        #3. Widget
        self.ui.Set1.clicked.connect(lambda: self.onEffectivelClicked())
        self.ui.Set2.clicked.connect(lambda: self.onCorrClicked())
        self.ui.ExecuteBttn.clicked.connect(lambda: self.onExecuteClicked())
        self.ui.NextGraph.clicked.connect(lambda: self.onNextGraphClicked())
        self.ui.PregGraph.clicked.connect(lambda:self.onPregGraphClicked())

        #4. Widget
        self.ui.BeginBttn.clicked.connect(lambda: self.onBeginClicked())
        self.ui.NextStepBttn.clicked.connect(lambda: self.onNextStepClicked())
        self.ui.PriorStepBttn.clicked.connect(lambda: self.onPriorStepClicked())

    #toggle Menu Animation
    def toggleMenu(self):
        width = self.ui.MenuFrane.width()
        maxExtend = 250
        standard = 70

        if width == 70:
            widthExtend = maxExtend
        else:
            widthExtend = standard

        #Animation:
        self.anim = QPropertyAnimation(self.ui.MenuFrane, b"minimumWidth")
        self.anim.setDuration(400)
        self.anim.setStartValue(width)
        self.anim.setEndValue(widthExtend)
        self.anim.setEasingCurve(QEasingCurve.InOutQuart)
        self.anim.start()

    def onBrowseFolderClicked(self):
        print("Browse Folder Button clicked")
        self.BrowseFolderClicked.emit()

    def onBrowseClicked(self):
        print("Browse Button clicked")
        self.BrowseClicked.emit()

    def onLoadClicked(self):
        print("Load Button clicked")
        self.LoadClicked.emit()


    def onStartClicked(self):
        print("PreProcess Start Button clicked")
        self.PPStartClicked.emit()
        self.ui.ForwStepBttn.setEnabled(True)
        self.ui.PrevStepBttn.setEnabled(True)
        self.ui.AlxBttn.setEnabled(True) # csak az axl-t oldjuk fel, mert alapból Dapi a cél.

        self.ui.MenuAnal.setEnabled(True)
        self.ui.Set1.setEnabled(True)
        self.ui.Set2.setEnabled(True)

    def onDapiClicked(self):
        self.ui.DAPIBttn.setEnabled(False)
        self.ui.AlxBttn.setEnabled(True)
        self.DapiClicked.emit()

    def onAxlClicked(self):
        self.ui.AlxBttn.setEnabled(False)
        self.ui.DAPIBttn.setEnabled(True)
        self.AlxClicked.emit()

    def onNextClick(self):
        self.NextClicked.emit()

    def onPrevClicked(self):
        self.PrevClicked.emit()


    def onEffectivelClicked(self):
        self.EffectiveClicked.emit()

    def onCorrClicked(self):
        self.CorrClicked.emit()

    def onExecuteClicked(self):
        self.ExecuteClicked.emit()

    def onNextGraphClicked(self):
        self.NextGraphClicked.emit()

    def onPregGraphClicked(self):
        self.PrevGraphClicked.emit()


    def onBeginClicked(self):
        self.BeginClicked.emit()
        self.ui.NextStepBttn.setEnabled(True)
        self.ui.PriorStepBttn.setEnabled(True)

    def onNextStepClicked(self):
        self.NextStepClicked.emit()

    def onPriorStepClicked(self):
        self.PriorStepClicked.emit()


    #Get property
    def getEffectiveNum(self):
        print('I was called')
        print(str(self.ui.EffValLine.text()))
        return str(self.ui.EffValLine.text())

    #Get property
    def getCorrNum(self):
        print('I was called')
        print(str(self.ui.SpatialValLine.text()))
        return str(self.ui.SpatialValLine.text())

    def changeFolderPathDisplay(self):
        print("___")
        self.ui.PathLine_2.setText(DH.defaultOutputFolder)

    def changePathDisplay(self):
        self.ui.PathLine.setText(DH.pathToFile)
        self.ui.LoadBttn.setEnabled(True)

    def changeMetaDisplay(self):
        self.ui.ContentTable.setColumnCount(1)
        self.ui.ContentTable.setRowCount(len(list(DH.Metadata.keys())))

        self.ui.ContentTable.setVerticalHeaderLabels(list(DH.Metadata.keys()))

        for i in range(len(list(DH.Metadata.values()))):
            self.ui.ContentTable.setItem(i, 0, QTableWidgetItem(str(list(DH.Metadata.values())[i])))

        self.ui.MenuProcess.setEnabled(True)
        self.ui.StartBttn.setEnabled(True)

    def changePictureDisplay(self, ch, index):
        data = np.array(DH.PreProcessedImageStack[ch][index]).reshape(1024, 1024).astype(np.uint8)
        img = QImage(data, data.shape[0], data.shape[1], QImage.Format_Grayscale8)
        pixmap = QPixmap(img).scaled(512, 512, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.ui.PreProcessLabel.setScaledContents(True)
        self.ui.PreProcessLabel.setPixmap(pixmap)

    def enableStartButton(self):
        self.ui.ExecuteBttn.setEnabled(True)

    def enableNextPrevButton(self):
        self.ui.PregGraph.setEnabled(True)
        self.ui.NextGraph.setEnabled(True)
        self.ui.MenuSegment.setEnabled(True)
        self.ui.BeginBttn.setEnabled(True)

    def changeGraphDisplay(self, index):
        data = DH.Graphs[index].astype(np.uint8)
        w, h, ch = data.shape

        bytesPerLine = 3 * h
        img = QImage(data, w, h, bytesPerLine, QImage.Format_RGB888)
        pixmap = QPixmap(img).scaled(512, 512, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.ui.GraphLabel.setScaledContents(True)
        self.ui.GraphLabel.setPixmap(pixmap)

    def changeSegmentDisplay(self, index):
        data = cv2.cvtColor(DH.SegmentedImages[index].astype(np.uint8), cv2.COLOR_BGR2RGB)
        w, h, ch = data.shape

        bytesPerLine = 3 * h
        img = QImage(data, w, h, bytesPerLine, QImage.Format_RGB888)
        pixmap = QPixmap(img).scaled(512, 512, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.ui.SegmentedLabel.setScaledContents(True)
        self.ui.SegmentedLabel.setPixmap(pixmap)

