from numpy import float32, zeros, uint16
#from scipy.misc import imsave
from skimage import exposure
from time import time
from xarray import open_dataset
import math
from tkinter import filedialog
from netCDF4 import Dataset
import numpy as np
from tkinter import *
from PyQt5.QtWidgets import QFileDialog, QDialog
#from definitions import ROOT_DIR
from PyQt5 import QtCore
from PyQt5 import QtGui
import os

#As described in https://github.com/fer-marino/sentinel3_optical/
#Since we aim at comparing different band data from Sentinel-3 SLSTR products, we decide to convert TOA radiances into TOA (Top of Atmosphere) Reflectance.
#TOA Reflectance is a unitless number that can be computed using Satellite Spectral Radiance, The earth-sun distance
#in astronomical units, the mean solar exoatmospheric irradiance and the solar zenith angleself.
#To accomplish the aforementioned conversion we need to access the ancillary data from Sentinel-3 (in our case the SLSTR ancillary data)

def sza_nadir_500(row, col, sza):
    derived_column = int(col / 32)
    return sza[int(min(row / 2, sza.shape[0] - 1))][derived_column]  # TODO add fraction

def process(product):
    # open radiance datasets
    print("Loading data...")
    start_time = time()
    s3_an = open_dataset(product + "/S3_radiance_an.nc")["S3_radiance_an"].values[:]
    s1_an = open_dataset(product + "/S1_radiance_an.nc")["S1_radiance_an"].values[:]
    s5_an = open_dataset(product + "/S5_radiance_an.nc")["S5_radiance_an"].values[:]
    s2_an = open_dataset(product + "/S2_radiance_an.nc")["S2_radiance_an"].values[:]
    s4_an = open_dataset(product + "/S4_radiance_an.nc")["S4_radiance_an"].values[:]
    s6_an = open_dataset(product + "/S6_radiance_an.nc")["S6_radiance_an"].values[:]
    # ancillary data needed for TOA reflectance conversion
    solar_irradiance_s3 = open_dataset(product + "/S3_quality_an.nc")["S3_solar_irradiance_an"].values[:]
    solar_irradiance_s1 = open_dataset(product + "/S1_quality_an.nc")["S1_solar_irradiance_an"].values[:]
    solar_irradiance_s5 = open_dataset(product + "/S5_quality_an.nc")["S5_solar_irradiance_an"].values[:]
    solar_irradiance_s2 = open_dataset(product + "/S2_quality_an.nc")["S2_solar_irradiance_an"].values[:]
    solar_irradiance_s4 = open_dataset(product + "/S4_quality_an.nc")["S4_solar_irradiance_an"].values[:]
    solar_irradiance_s6 = open_dataset(product + "/S6_quality_an.nc")["S6_solar_irradiance_an"].values[:]

    detectors = open_dataset(product + "/indices_an.nc")["detector_an"].values[:]
    sza = open_dataset(product + "/geometry_tn.nc")["solar_zenith_tn"].values[:]

    width = s3_an.shape[1]
    height = s3_an.shape[0]
    print("Loading completed in {w:.2f} seconds".format(w=time() - start_time))

    # Set the RGB values
    print("Processing started. Dimension w:{w:d} h:{h:d}".format(w=width, h=height))
    start_time = time()
    perf_time = time()
    counter = 0
    for y in range(height):
        for x in range(width):
            counter += 1
            if not math.isnan(detectors[y][x]) and not math.isnan(s3_an[y][x]) and not math.isnan(s1_an[y][x]) and not math.isnan(s5_an[y][x]):
                sza_corrected = sza_nadir_500(x, y, sza)
                s5_reflectance = max(0, min(1., math.pi * (s5_an[y][x] / solar_irradiance_s5[int(detectors[y][x])]) / math.cos(math.radians(sza_corrected))))
                s3_reflectance = max(0, min(1., math.pi * (s3_an[y][x] / solar_irradiance_s3[int(detectors[y][x])]) / math.cos(math.radians(sza_corrected))))
                s1_reflectance = max(0, min(1., math.pi * (s1_an[y][x] / solar_irradiance_s1[int(detectors[y][x])]) / math.cos(math.radians(sza_corrected))))
                s2_reflectance = max(0, min(1., math.pi * (s2_an[y][x] / solar_irradiance_s2[int(detectors[y][x])]) / math.cos(math.radians(sza_corrected))))
                s4_reflectance = max(0, min(1., math.pi * (s4_an[y][x] / solar_irradiance_s4[int(detectors[y][x])]) / math.cos(math.radians(sza_corrected))))
                s6_reflectance = max(0, min(1., math.pi * (s6_an[y][x] / solar_irradiance_s6[int(detectors[y][x])]) / math.cos(math.radians(sza_corrected))))
                #once we extract products and compute the conversion into TOA reflectance we can save them into
    input("\n press a button to continue...")    #a new nc dataset called "reflectance.nc"
    if (os.path.isfile(product+"/reflectance.nc")):
        os.remove(product+"/reflectance.nc")
        print("\n reflectance.nc alredy in folder... removing reflectance.nc \n")
    with Dataset(product+"/reflectance.nc","w",format="NETCDF4") as f:
        #now it is needed to create a varibale using the method "createvariable" from the dataset variable we've just initialized
        tempgrp=f.createGroup('reflectance_an')
        tempgrp.createDimension('width',width)
        tempgrp.createDimension('height',height)
        S1_Reflectance_an = tempgrp.createVariable('s1_reflectance_an','d',('width','height'))
        S2_Reflectance_an = tempgrp.createVariable('s2_reflectance_an','d',('width','height'))
        S3_Reflectance_an = tempgrp.createVariable('s3_reflectance_an','d',('width','height'))
        S4_Reflectance_an = tempgrp.createVariable('s4_reflectance_an','d',('width','height'))
        S5_Reflectance_an = tempgrp.createVariable('s5_reflectance_an','d',('width','height'))
        S6_Reflectance_an = tempgrp.createVariable('s6_reflectance_an','d',('width','height'))
        S1_Reflectance_an=s1_reflectance
        S2_Reflectance_an=s2_reflectance
        S3_Reflectance_an=s3_reflectance
        S4_Reflectance_an=s4_reflectance
        S5_Reflectance_an=s5_reflectance
        S6_Reflectance_an=s6_reflectance
        #f.close()
        #after closing the dataset all reflectance channels can be accessed for the data analysis

def rad_to_reflectance(filename):
    #the main function allows us to browse the directory which includes the product of interest (SLSTR products in our case study)
    #filename = filedialog.askdirectory()
    process(filename)
