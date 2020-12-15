import pims
from Model.DataHolder import DataHolder as DH



def nd2_processor():

    images = pims.Bioformats(DH.pathToFile)
    print("Sikeres megnyitás")

    meta = images.metadata
    DH.Metadata.update({'File Name': DH.fileNameWithExtension})
    DH.Metadata.update({'Image Dim (x)': meta.PixelsSizeX(0)})
    DH.Metadata.update({'Image Dim (Y)': meta.PixelsSizeY(0)})
    DH.Metadata.update({'Image Dim (Z)': meta.PixelsSizeZ(0)})
    DH.Metadata.update({'Channel Number': meta.PixelsSizeC(0)})
    DH.Metadata.update({'Channel Name (1)': meta.ChannelName(0, 0)})
    DH.Metadata.update({'Channel Name (2)': meta.ChannelName(0, 1)})
    DH.Metadata.update({'Sample Size (x)': meta.PixelsPhysicalSizeX(0)})
    DH.Metadata.update({'Sample Size (Y)': meta.PixelsPhysicalSizeY(0)})
    DH.Metadata.update({'Sample Depth': meta.PixelsPhysicalSizeZ(0)})

    images.bundle_axes = 'xy'
    images.iter_axes = 'cz'

    for img in range(0, len(images) + 1):
        DH.RawImageStackTemp.append(images.get_frame(img))

    __get_dapi_channel()
    __get_alx_channel()


def __get_dapi_channel():
    inLineIndex = int(len(DH.RawImageStackTemp) / 2)

    for img in range(0, inLineIndex):
        DH.RawDAPI.append(DH.RawImageStackTemp[img])

    print("Sikeres Dapi")

def __get_alx_channel():
    inLineIndex = int(len(DH.RawImageStackTemp) / 2)

    for img in range(inLineIndex + 1, len(DH.RawImageStackTemp)):
        DH.RawAlx647.append(DH.RawImageStackTemp[img])

    print("Sikeres ALX")