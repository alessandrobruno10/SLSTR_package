#this program allows for unpacking cloud masks from flag data
import os
import netCDF4
import matplotlib.pyplot as plt
import numpy as np

#let's say we want to extract cirrus mask from a SLSTR product sample
# suppose we have already got into the SLSTR product folder, so we have a list of .nc files

data = netCDF4.Dataset('flags_an.nc','r','NETCDF4').variables['cloud_an'][:]
data = data.data
flags=np.unpackbits(data[...,np.newaxis].view("uint8")[...,::-1][...,np.newaxis],axis=-1).reshape(data.shape+(-1,))[...,::-1]

#in this case flags will be shown as a [M,N,16] sized array where M is the width and N is the height of the flagging data
#arranged in 2-dimensional arrays
#if we get back to analyse the correspondences between flagging data and cloud_mask it will be shown something as it follows:
#flag_masks: [    1     2     4     8    16    32    64   128   256   512  1024  2048  4096  8192 16384 32768]
#flag_meanings: [0]visible [1]1.37_threshold [2]1.6_small_histogram [3]1.6_large_histogram [4]2.25_small_histogram
#[[5]2.25_large_histogram [6]11_spatial_coherence [7]gross_cloud [8]thin_cirrus medium_high [9]fog_low_stratus
#[10]11_12_view_difference [11]3.7_11_view_difference [12]thermal_histogram [13]spare [14]spare
#I add the ascendent number of component in the array so it is more understandable how cloud_masks are arranged and indexed
#if, for instance, we want to show the cirrus mask... we will need to extract the 8th component from the flags array unpacked

plt.imshow(flags[...,8],cmap=plt.cm.gray)
plt.show()
