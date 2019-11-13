import tkinter
from tkinter import font
from tkinter import messagebox
from tkinter import filedialog
from tkinter import Button, Label
from PIL import ImageTk, Image
#the packages above are imported because of the GUI utilization
import os
import numpy as np
from netCDF4 import Dataset
import glob
import cv2
from skimage import color
import sys
#import rad_to_reflectance
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QToolTip, QMessageBox
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSlot, QDir, QCoreApplication
from PyQt5.QtWidgets import QFileDialog, QDialog, QListView, QAbstractItemView, QTreeView
from PIL import ImageTk, Image
#the packages above are imported because of the GUI utilization
import os
import numpy as np
from netCDF4 import Dataset
import glob
import cv2
from skimage import color

#Once the code is executed the user should browse the folder containing all SLSTR_directory products (uncompressed or unzipped)
#this script allows for the extraction of multichannel bands from Sentinel-3 level_1B
#for each SLSTR product downloaded as a folder (unzipped file)
#all files related to reflectance Channels and Brightness Temperature Channels go stored into a data-cube
#as numpy array - afterward a normalisation steep is needed
#Several folders corresponding to Sentinel-3 SLSTR Level_1B_RBT are provided in reference directory
#to extract all reflectance and BT bands: S1,S1,S3,S5,S6,S7,S8,S9,F1,F2

#Notice that in SLSTR product Level_1B_RBT, for thermal IR and fire channels (labelled as S7 to S9 and F1, F2 for fire channels),
#the radiometric measurements are expressed in Top Of Atmosphere (TOA) brightness temperatures.
#In the case of visible / NIR / SWIR channels (labelled as S1 to S6 channels), these measurements are expressed
#in TOA reflectances.

#a simple GUI is given to users to select the root SLSTR folder containing all products
#PyQt5 has been used because of its portability over different operating systemsself.
#Tkinter package has revealed not to be Mac Os MoJave compliant

class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 messagebox - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 200
        self.initUI()


    def initUI(self):
        self.setWindowTitle("SLSTR Data Extraction...")
        self.setGeometry(self.left, self.top, self.width, self.height)

        buttonReply = QMessageBox.question(self, 'SLSTR Image Loading', "Press Yes to browse SLSTR main folder", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            print('Yes clicked.')
        else:
            #QApplication.quit()
            sys.exit()
        self.show()

    #@pyqtSlot()
    def on_click(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.DirectoryOnly)
        file_dialog.setOption(QFileDialog.DontUseNativeDialog, True)
        file_view = file_dialog.findChild(QListView, 'listView')
        # to make it possible to select multiple directories:
        if file_view:
            file_view.setSelectionMode(QAbstractItemView.MultiSelection)
        f_tree_view = file_dialog.findChild(QTreeView)
        if f_tree_view:
            f_tree_view.setSelectionMode(QAbstractItemView.MultiSelection)
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.DirectoryOnly)
        file_dialog.setOption(QFileDialog.DontUseNativeDialog, True)
        file_view = file_dialog.findChild(QListView, 'listView')
        if file_dialog.exec():
            sourceFolder = file_dialog.selectedFiles()
        return sourceFolder

#Initialisation of GUI
app=QApplication(sys.argv)
ex = Example()
#fetching the SLSTR root directory
source = ex.on_click()
app.quit()

import matplotlib.pyplot as plt
print("Here is the path you've just selected as root path:::",source)
os.chdir(source[0])
print("Here is the path you've just selected as root path:::",source)
print("Here is the file list inside the current directory",glob.glob('*.*'))

SLSTR_directories = glob.glob("*/") #catching all the SLSTR product directory paths
current_directory=[]
Data_Bands = []
#let's initialize a counter i=0

def data_refine(a,b,M_reflectance):
    M_array = np.asarray(M_reflectance).astype(float)
        #M_array = M_array[0:a,0:b]
        #[a2,b2]=M_array.shape
        #if a2!=a or b2!=b:
    M_array = cv2.resize(M_array, dsize=(b,a), interpolation=cv2.INTER_AREA)
    return M_array

def cloud_refine(a,b,Cloud):
        #Cloud_array = np.asarray(Cloud)#.astype(float)
    Cloud_array = Cloud[:]
    Cloud_array = Cloud_array[0:a,0:b]
        #[a2,b2]=Cloud_array.shape
        #if a2!=a or b2!=b:
        #    Cloud_array = cv2.resize(Cloud_array, dsize=(b,a), interpolation=cv2.INTER_AREA)
    return Cloud_array

i=0
Num_SLSTR_Products = len(SLSTR_directories) #this constant allows for counting the number of products to be iterated

sizes=[]
for KKK in SLSTR_directories:
    os.chdir(KKK)
    p = glob.glob("*.nc")
    Flags_an = Dataset("flags_an.nc","r",format="NETCDF4")
    Cloud_an = Flags_an.variables.get('cloud_an')
    [a,b]=Cloud_an.shape
    c = a*b
    sizes.append([a,b,c])
    os.chdir('../')

sizes=np.asarray(sizes)
result = np.where(sizes[:,2] == np.amin(sizes[:,2]))
a1 = sizes[result[0][0],0]
b1 = sizes[result[0][0],1]

for current_directory in SLSTR_directories:
    print("current_directory is:::",current_directory)
    os.chdir(current_directory)
    p = glob.glob("*.nc")
        #exploring data of each SLSTR product
    if i==0:
        reflectance = Dataset("reflectance.nc","r",format="NETCDF4")
        S1_reflectance = reflectance['reflectance_an'].variables.get("S1_reflectance_an")
        S1_reflectance_array = np.asarray(S1_reflectance)
        S2_reflectance = reflectance['reflectance_an'].variables.get("S2_reflectance_an")
        S2_reflectance_array = data_refine(a1,b1,S2_reflectance)
        S3_reflectance = reflectance['reflectance_an'].variables.get("S3_reflectance_an")
        S3_reflectance_array = data_refine(a1,b1,S3_reflectance)
        S4_reflectance = reflectance['reflectance_an'].variables.get("S4_reflectance_an")
        S4_reflectance_array = data_refine(a1,b1,S4_reflectance)
        S5_reflectance = reflectance['reflectance_an'].variables.get("S5_reflectance_an")
        S5_reflectance_array = data_refine(a1,b1,S5_reflectance)
        S6_reflectance = reflectance['reflectance_an'].variables.get("S6_reflectance_an")
        S6_reflectance_array = data_refine(a1,b1,S6_reflectance)
        S7 = Dataset("S7_BT_in.nc","r",format="NETCDF4")
        S7_BT = S7.variables.get("S7_BT_in")
        S7_BT_array = data_refine(a1,b1,S7_BT)
        S8 = Dataset("S8_BT_in.nc","r",format="NETCDF4")
        S8_BT = S8.variables.get("S8_BT_in")
        S8_BT_array = data_refine(a1,b1,S8_BT)
        S9 = Dataset("S9_BT_in.nc","r",format="NETCDF4")
        S9_BT = S9.variables.get("S9_BT_in")
        S9_BT_array = data_refine(a1,b1,S9_BT)
        F1 = Dataset("F1_BT_in.nc","r",format="NETCDF4")
        F1_BT = F1.variables.get("F1_BT_in")
        F1_BT_array = data_refine(a1,b1,F1_BT)
        F2 = Dataset("F2_BT_in.nc","r",format="NETCDF4")
        F2_BT = F2.variables.get("F2_BT_in")
        F2_BT_array = data_refine(a1,b1,F2_BT)

        Flags_an = Dataset("flags_an.nc","r",format="NETCDF4")
        Cloud_an = Flags_an.variables.get('cloud_an')
        Cloud_an = Cloud_an[:]
        Cloud_an_array = cloud_refine(a1,b1,Cloud_an)

            #Flags_in = Dataset("flags_in.nc","r",format="NETCDF4")
            #Cloud_in = Flags_in.variables.get('cloud_in')
            #Cloud_in_array = cloud_refine(a1,b1,Cloud_in)

        Data_Bands = np.ndarray((11*Num_SLSTR_Products,a1,b1), dtype=np.float32)
        Cloud_Data = np.ndarray((Num_SLSTR_Products,a1,b1), dtype=np.float32)
        Data_Bands[0,...]=S1_reflectance_array
        Data_Bands[1,...]=S2_reflectance_array
        Data_Bands[2,...]=S3_reflectance_array
        Data_Bands[3,...]=S4_reflectance_array
        Data_Bands[4,...]=S5_reflectance_array
        Data_Bands[5,...]=S6_reflectance_array
        Data_Bands[6,...]=S7_BT_array
        Data_Bands[7,...]=S8_BT_array
        Data_Bands[8,...]=S9_BT_array
        Data_Bands[9,...]=F1_BT_array
        Data_Bands[10,...]=F2_BT_array

        Cloud_Data[i,...] = Cloud_an_array
    else:
        reflectance = Dataset("reflectance.nc","r",format="NETCDF4")
        S1_reflectance = reflectance['reflectance_an'].variables.get("S1_reflectance_an")
        S1_reflectance_array = np.asarray(S1_reflectance)
        S2_reflectance = reflectance['reflectance_an'].variables.get("S2_reflectance_an")
        S2_reflectance_array = data_refine(a1,b1,S2_reflectance)
        S3_reflectance = reflectance['reflectance_an'].variables.get("S3_reflectance_an")
        S3_reflectance_array = data_refine(a1,b1,S3_reflectance)
        S4_reflectance = reflectance['reflectance_an'].variables.get("S4_reflectance_an")
        S4_reflectance_array = data_refine(a1,b1,S4_reflectance)
        S5_reflectance = reflectance['reflectance_an'].variables.get("S5_reflectance_an")
        S5_reflectance_array = data_refine(a1,b1,S5_reflectance)
        S6_reflectance = reflectance['reflectance_an'].variables.get("S6_reflectance_an")
        S6_reflectance_array = data_refine(a1,b1,S6_reflectance)
        S7 = Dataset("S7_BT_in.nc","r",format="NETCDF4")
        S7_BT = S7.variables.get("S7_BT_in")
        S7_BT_array = data_refine(a1,b1,S7_BT)
        S8 = Dataset("S8_BT_in.nc","r",format="NETCDF4")
        S8_BT = S8.variables.get("S8_BT_in")
        S8_BT_array = data_refine(a1,b1,S8_BT)
        S9 = Dataset("S9_BT_in.nc","r",format="NETCDF4")
        S9_BT = S9.variables.get("S9_BT_in")
        S9_BT_array = data_refine(a1,b1,S9_BT)
        F1 = Dataset("F1_BT_in.nc","r",format="NETCDF4")
        F1_BT = F1.variables.get("F1_BT_in")
        F1_BT_array = data_refine(a1,b1,F1_BT)
        F2 = Dataset("F2_BT_in.nc","r",format="NETCDF4")
        F2_BT = F2.variables.get("F2_BT_in")
        F2_BT_array = data_refine(a1,b1,F2_BT)

        Flags_an = Dataset("flags_an.nc","r",format="NETCDF4")
        Cloud_an = Flags_an.variables.get('cloud_an')
        Cloud_an = Cloud_an[:]
        Cloud_an_array = cloud_refine(a1,b1,Cloud_an)

        Data_Bands[i*11,...]=S1_reflectance_array
        Data_Bands[i*11+1,...]=S2_reflectance_array
        Data_Bands[i*11+2,...]=S3_reflectance_array
        Data_Bands[i*11+3,...]=S4_reflectance_array
        Data_Bands[i*11+4,...]=S5_reflectance_array
        Data_Bands[i*11+5,...]=S6_reflectance_array
        Data_Bands[i*11+6,...]=S7_BT_array
        Data_Bands[i*11+7,...]=S8_BT_array
        Data_Bands[i*11+8,...]=S9_BT_array
        Data_Bands[i*11+9,...]=F1_BT_array
        Data_Bands[i*11+10,...]=F2_BT_array

        Cloud_Data[i,...] = Cloud_an_array

    os.chdir('../')
    i = i+1
print("MAX VALUE of CLOUD :::",np.max(Cloud_Data))
print("MAX VALUE of Data :::",np.max(Data_Bands[~np.isnan(Data_Bands)]))
print("MIN VALUE of CLOUD :::",np.min(Cloud_Data))
print("MIN VALUE of Data :::",np.min(Data_Bands[~np.isnan(Data_Bands)]))

np.save('Data.npy', Data_Bands)  #data related to all bands are stored into Data.npy
np.save('Cloud_an.npy',Cloud_Data) #data related to Cloud are stored into Cloud_an.npy
#As far as it concerns normalisation step
