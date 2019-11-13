import cv2
#import matplotlib.pyplot as plt
import numpy as np
#import numpy as np
from netCDF4 import Dataset
import glob
import cv2
import tkinter
from tkinter import font
from tkinter import messagebox
from tkinter import filedialog
from tkinter import Button, Label
from PIL import ImageTk, Image
#the packages above are imported because of the GUI utilization
import os
import glob
import cv2
from skimage import color
import sys
#import rad_to_reflectance
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QToolTip, QMessageBox
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSlot, QDir, QCoreApplication
from PyQt5.QtWidgets import QFileDialog, QDialog, QListView, QAbstractItemView, QTreeView
from PIL import Image
#the packages above are imported because of the GUI utilization

import numpy as np
from netCDF4 import Dataset
import glob
import cv2


# read the image and define the stepSize and window size
# (width,height)
#DATA won't be normalised during the execution, it is demanded to training step
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

        buttonReply = QMessageBox.question(self, 'SLSTR Patch Extraction', "Press Yes to browse SLSTR data folder", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
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

app=QApplication(sys.argv)
ex = Example()
#fetching the SLSTR root directory
source = ex.on_click()
app.quit()

import matplotlib.pyplot as plt
print("Here is the path you've just selected as root path:::",source)
os.chdir(source[0])


#NUM_BANDS = 11
Data_Bands = np.load('Data.npy')
Cloud = np.load('Cloud_an.npy')


NUM_DATA = Data_Bands.shape[0]
NUM_CLOUD_DATA = Cloud.shape[0]
[M,N]=Cloud.shape[1:]

stepSize = 199
w_width = 398
w_height = 398
#M,N are the size of each Image from where we will extract all patches
patch_cloud_mask = []
cloudy_data_refined = []
clear_data_refined = []
for i in range(0,NUM_CLOUD_DATA):
    for x in range(0, M - w_width , stepSize):
        for y in range(0, N - w_height, stepSize):
            #window_image = image[x:x + w_width, y:y + w_height, :]
            cloud = Cloud[i,...] #let's analyze the i° cloud
            #check the cloudy pixels
            window_cloud = cloud[x:x + w_width, y:y + w_height]
            #print("window_cloud size:::",window_cloud.shape)
            if np.all(window_cloud!=0):
                #it means we have a cloudy patch
                print("cloudy patch found")
                PATCH = Data_Bands[i:i+11,x:x+w_width,y:y+w_height]
                print("SIZE",PATCH.shape)
                cloudy_data_refined.append(Data_Bands[i:i+11,x:x+w_width,y:y+w_height])
                patch_cloud_mask.append(window_cloud)
                #print(cloudy_data_refined.shape)
            if np.all(window_cloud==0):
                print("clear patch found")
                #print(clear_data_refined.shape)
                #it means we have a clear patch
                clear_data_refined.append(Data_Bands[i:i+11,x:x+w_width,y:y+w_height])
cloudy_data_refined_2 = np.asarray(cloudy_data_refined)
#print("Size of cloudy data:::",cloudy_data_refined.shape)
clear_data_refined_2 = np.asarray(clear_data_refined)
patch_cloud_mask_refined2 = np.asarray(patch_cloud_mask)
#print("Size of clear data:::",clear_data_refined.shape)

K_cloudy = cloudy_data_refined_2.shape
if K_cloudy[0]>0:
    [k1, k2, k3, k4]=cloudy_data_refined_2.shape
    for k in range(0,k2):
        cloudy_data_refined_2[:,k,:,:]=(cloudy_data_refined_2[:,k,:,:]-np.mean(cloudy_data_refined_2[:,k,:,:]))/((np.std(cloudy_data_refined_2[:,k,:,:]))+np.finfo(float).eps)

K_clear = clear_data_refined_2.shape
if K_clear[0]>0:
    print("\n\n clear data shape  is :::",K[0])
    [k1, k2, k3, k4]=clear_data_refined_2.shape
    print(k2)
    for k in range(0,k2):
        print("Mean and Std:::",np.mean(clear_data_refined_2[:,k,:,:]),np.std(clear_data_refined_2[:,k,:,:]))
        clear_data_refined_2[:,k,:,:]=(clear_data_refined_2[:,k,:,:]-np.mean(clear_data_refined_2[:,k,:,:]))/((np.std(clear_data_refined_2[:,k,:,:]))+0.000005)

#the archive function allows for saving all data_bands with respect to the cloud presence
np.save('Cloudy_Data.npy',cloudy_data_refined_2)
np.save('Clear_Data.npy',clear_data_refined_2)
np.save('patch_cloud_mask.npy',patch_cloud_mask_refined2)
