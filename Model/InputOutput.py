import os
import csv
import cv2
from PIL import Image
import PyQt5.QtWidgets
from Model.DataHolder import DataHolder as DH


def browseFile():
    DH.pathToFile = PyQt5.QtWidgets.QFileDialog.getOpenFileName(None, 'Open file', os.getcwd(), "*.nd2")[0]
    if DH.pathToFile is not None:
        __file_name_setter()

def browseFolder():
    DH.defaultOutputFolder = PyQt5.QtWidgets.QFileDialog.getExistingDirectory(None, 'Open Folder', os.getcwd())
    if DH.defaultOutputFolder is not None:
        DH.defaultOutputPath = DH.defaultOutputFolder + "\\Output_"

def __file_name_setter():
    DH.fileNameWithExtension = DH.pathToFile.split("/")[len(DH.pathToFile.split("/")) - 1]
    DH.fileNameWithoutExtension = DH.fileNameWithExtension[:-4]

def __directory_setter():
    print(DH.defaultOutputPath)
    DH.updatedOutputPath = DH.defaultOutputPath + DH.fileNameWithoutExtension
    print(DH.updatedOutputPath)
    DH.PreProcessedOutputPath = DH.updatedOutputPath + "\\PreProcessed"
    DH.GraphOutputPath = DH.updatedOutputPath + "\\Stack_analysis"
    DH.SegmentedOutputPath = DH.updatedOutputPath + "\\Segmented_Cells"

def directory_creator():
    __directory_setter()

    os.mkdir(DH.updatedOutputPath)
    os.mkdir(DH.PreProcessedOutputPath)
    os.mkdir(DH.GraphOutputPath)
    os.mkdir(DH.SegmentedOutputPath)

def save_metadata_to_csv():
    directory_creator()
    csv_file_name = DH.fileNameWithoutExtension + "_metadata.csv"
    csv_path = [DH.updatedOutputPath, csv_file_name]
    csv_file_path = "\\".join(csv_path)
    writer = csv.writer(open(csv_file_path, "w"))
    for key, val in DH.Metadata.items():
        writer.writerow([key, val])

def save_pre_processed_to_destination():
    os.chdir(DH.PreProcessedOutputPath)
    iterator = 1
    for i in range(len(DH.PreProcessedImageStack)):
        for j in range(len(DH.PreProcessedImageStack[i])):
            cv2.imwrite(DH.fileNameWithoutExtension + "_segmented_%d.png" % iterator, DH.PreProcessedImageStack[i][j])
            iterator += 1

def create_and_save_graph():
    os.chdir(DH.GraphOutputPath)
    PIL_image = Image.fromarray(DH.Graphs[0].astype('uint8'), 'RGB')
    PIL_image.save(DH.fileNameWithoutExtension + "_effective_resolution.png")
    PIL_image = Image.fromarray(DH.Graphs[1].astype('uint8'), 'RGB')
    PIL_image.save(DH.fileNameWithoutExtension + "_spatial_corr_between_slices.png")
    PIL_image = Image.fromarray(DH.Graphs[2].astype('uint8'), 'RGB')
    PIL_image.save(DH.fileNameWithoutExtension + "_spatial_corr_within_slices.png")

def createVideoFromImageData():
    os.chdir(DH.SegmentedOutputPath)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(DH.fileNameWithoutExtension + "cv2_segmented_cells_in_stack.mp4", fourcc, 15, (1024, 1024))

    for i in range(0, len(DH.SegmentedImages)):
        video.write(DH.SegmentedImages[i])

    cv2.destroyAllWindows()
    video.release()

