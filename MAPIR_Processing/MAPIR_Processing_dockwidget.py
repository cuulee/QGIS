# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MAPIR_ProcessingDockWidget
                                 A QGIS plugin
 Widget for processing images captured by MAPIR cameras
                             -------------------
        begin                : 2016-09-26
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Peau Productions
        email                : ethan@peauproductions.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os
os.umask(0)
import sys
import shutil
from PyQt4 import uic, QtGui
from PyQt4.QtCore import pyqtSignal
# from qgis.core import QgsMessageLog

from scipy import stats
import numpy as np
modpath = os.path.dirname(os.path.realpath(__file__))
pypath = os.path.split(os.path.split(sys.executable)[0])[0] + os.sep + "apps" + os.sep + "Python27"
if not os.path.exists(pypath + os.sep + "Scripts" + os.sep + "exiftool.exe")\
        or not os.path.exists(pypath + os.sep + "Scripts" + os.sep + "dcraw.exe")\
        or not os.path.exists(pypath + os.sep + "Scripts" + os.sep + "cygwin1.dll")\
        or not os.path.exists(pypath + os.sep + "Lib" + os.sep + "site-packages" + os.sep + "exiftool.py")\
        or not os.path.exists(pypath + os.sep + "Lib" + os.sep + "site-packages" + os.sep + "exiftool.pyc")\
        or not os.path.exists(pypath + os.sep + "Lib" + os.sep + "site-packages" + os.sep + "cv2.pyd"):
    os.chmod(pypath,0777)
    shutil.copy(modpath + os.sep + "exiftool.exe", pypath + os.sep + "Scripts")
    shutil.copy(modpath + os.sep + "dcraw.exe", pypath + os.sep + "Scripts")
    shutil.copy(modpath + os.sep + "cygwin1.dll", pypath + os.sep + "Scripts")
    shutil.copy(modpath + os.sep + "exiftool.py", pypath + os.sep + "Lib" + os.sep + "site-packages")
    shutil.copy(modpath + os.sep + "exiftool.pyc", pypath + os.sep + "Lib" + os.sep + "site-packages")
    shutil.copy(modpath + os.sep + "cv2.pyd", pypath + os.sep + "Lib" + os.sep + "site-packages")
import cv2
import glob
import subprocess
import exiftool

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'MAPIR_Processing_dockwidget_base.ui'))


class MAPIR_ProcessingDockWidget(QtGui.QDockWidget, FORM_CLASS):
    BASE_COEFF_SURVEY2_RED_JPG = [-2.55421832, 16.01240929, 0.0, 0.0, 0.0, 0.0]
    BASE_COEFF_SURVEY2_GREEN_JPG = [0.0, 0.0, -0.60437250, 4.82869470, 0.0, 0.0]
    BASE_COEFF_SURVEY2_BLUE_JPG = [0.0, 0.0, 0.0, 0.0, -0.39268985, 2.67916884]
    BASE_COEFF_SURVEY2_NDVI_JPG = [-0.29870245, 6.51199915, 0.0, 0.0, -0.65112026, 10.30416005]
    BASE_COEFF_SURVEY2_NIR_JPG = [-0.46967653, 7.13619139, 0.0, 0.0, 0.0, 0.0]
    BASE_COEFF_SURVEY1_NDVI_JPG = [-6.33770486888, 331.759383023, 0.0, 0.0, -0.6931339436, 51.3264675118]
    BASE_COEFF_SURVEY2_RED_TIF = [-5.09645820, 0.24177528, 0.0, 0.0, 0.0, 0.0]
    BASE_COEFF_SURVEY2_GREEN_TIF = [0.0, 0.0, -1.39528479, 0.07640011, 0.0, 0.0]
    BASE_COEFF_SURVEY2_BLUE_TIF = [0.0, 0.0, 0.0, 0.0, -0.67299134, 0.03943339]
    BASE_COEFF_SURVEY2_NDVI_TIF = [-0.60138990, 0.14454211, 0.0, 0.0, -3.51691589, 0.21536524]
    BASE_COEFF_SURVEY2_NIR_TIF = [-2.24216724, 0.12962333, 0.0, 0.0, 0.0, 0.0 ]
    BASE_COEFF_DJIX3_NDVI_JPG = [-0.34430543, 4.63184993, 0.0, 0.0, -0.49413940, 16.36429964]
    BASE_COEFF_DJIX3_NDVI_TIF = [-0.74925346, 0.01350319, 0.0, 0.0, -0.77810008, 0.03478272]
    BASE_COEFF_DJIPHANTOM4_NDVI_JPG = [-1.17016961, 0.03333209, 0.0, 0.0, -0.99455214, 0.05373502]
    BASE_COEFF_DJIPHANTOM4_NDVI_TIF = [-1.17016961, 0.03333209, 0.0, 0.0, -0.99455214, 0.05373502]
    BASE_COEFF_DJIPHANTOM3_NDVI_JPG = [-1.54494979, 3.44708472, 0.0, 0.0, -1.40606832, 6.35407929]
    BASE_COEFF_DJIPHANTOM3_NDVI_TIF = [-1.37495554, 0.01752340, 0.0, 0.0, -1.41073753, 0.03700812]

    #Load FlatField Arrays
    # SURVEY_FF_RED_JPG = np.load(modpath + os.sep + "FlatFields" + os.sep + "FF_red_JPG.npy")
    # SURVEY_FF_GREEN_JPG = np.load(modpath + os.sep + "FlatFields" + os.sep + "FF_green_JPG.npy")
    # SURVEY_FF_BLUE_JPG = np.load(modpath + os.sep + "FlatFields" + os.sep + "FF_blue_JPG.npy")
    # SURVEY_FF_NIR_JPG = np.load(modpath + os.sep + "FlatFields" + os.sep + "FF_nir_JPG.npy")
    # SURVEY_FF_NDVI_JPG = np.load(modpath + os.sep + "FlatFields" + os.sep + "FF_ndvi_JPG.npy")
    # SURVEY_FF_RGB_JPG = np.load(modpath + os.sep + "FlatFields" + os.sep + "FF_rgb_JPG.npy")
    # FC350_FF_NDVI_JPG = np.load(modpath + os.sep + "FlatFields" + os.sep + "FF_FC350_JPG.npy")
    # FC330_FF_NDVI_JPG = np.load(modpath + os.sep + "FlatFields" + os.sep + "FF_FC330_JPG.npy")
    # FC300S_FF_NDVI_JPG = np.load(modpath + os.sep + "FlatFields" + os.sep + "FF_FC300S_JPG.npy")
    # FC300X_FF_NDVI_JPG = np.load(modpath + os.sep + "FlatFields" + os.sep + "FF_FC300X_JPG.npy")
    # SURVEY_FF_RED = np.load(modpath + os.sep + "FlatFields" + os.sep + "FF_red_RAW.npy")
    # SURVEY_FF_GREEN = np.load(modpath + os.sep + "FlatFields" + os.sep + "FF_green_RAW.npy")
    # SURVEY_FF_BLUE = np.load(modpath + os.sep + "FlatFields" + os.sep + "FF_blue_RAW.npy")
    # SURVEY_FF_NIR = np.load(modpath + os.sep + "FlatFields" + os.sep + "FF_nir_RAW.npy")
    # with open(modpath + os.sep + "FlatFields" + os.sep + "1.RAW", "rb") as ndvi:
    #     SURVEY_FF_NDVI = np.fromfile(ndvi, np.dtype('u2'), 3456 * 4608).reshape((3456,4608))
    # SURVEY_FF_RGB = np.load(modpath + os.sep + "FlatFields" + os.sep + "FF_rgb_RAW.npy")
    # FC350_FF_NDVI = np.load(modpath + os.sep + "FlatFields" + os.sep + "FF_FC350_DNG.npy")
    # FC330_FF_NDVI = np.load(modpath + os.sep + "FlatFields" + os.sep + "FF_FC330_DNG.npy")
    # FC300S_FF_NDVI = np.load(modpath + os.sep + "FlatFields" + os.sep + "FF_FC300S_DNG.npy")
    # FC300X_FF_NDVI = np.load(modpath + os.sep + "FlatFields" + os.sep + "FF_FC300X_DNG.npy")
    #
    # #Load Dark Currant Arrays
    # SURVEY_DC_RED_JPG = np.load(modpath + os.sep + "FlatFields" + os.sep + "DC_red_JPG.npy")
    # SURVEY_DC_GREEN_JPG = np.load(modpath + os.sep + "FlatFields" + os.sep + "DC_green_JPG.npy")
    # SURVEY_DC_BLUE_JPG = np.load(modpath + os.sep + "FlatFields" + os.sep + "DC_blue_JPG.npy")
    # SURVEY_DC_NIR_JPG = np.load(modpath + os.sep + "FlatFields" + os.sep + "DC_nir_JPG.npy")
    # SURVEY_DC_NDVI_JPG =  np.load(modpath + os.sep + "FlatFields" + os.sep + "DC_ndvi_JPG.npy")
    # SURVEY_DC_RGB_JPG = np.load(modpath + os.sep + "FlatFields" + os.sep + "DC_rgb_JPG.npy")
    # FC350_DC_NDVI_JPG = 0 #np.load(modpath + os.sep + "FlatFields" + os.sep + "DC_FC350_JPG.npy")
    # FC330_DC_NDVI_JPG = 0 #np.load(modpath + os.sep + "FlatFields" + os.sep + "DC_FC330_JPG.npy")
    # FC300S_DC_NDVI_JPG = 0 #np.load(modpath + os.sep + "FlatFields" + os.sep + "DC_FC300S_JPG.npy")
    # FC300X_DC_NDVI_JPG = 0 #np.load(modpath + os.sep + "FlatFields" + os.sep + "DC_FC300X_JPG.npy")
    # SURVEY_DC_RED = np.load(modpath + os.sep + "FlatFields" + os.sep + "DC_red_RAW.npy")
    # SURVEY_DC_GREEN = np.load(modpath + os.sep + "FlatFields" + os.sep + "DC_green_RAW.npy")
    # SURVEY_DC_BLUE = np.load(modpath + os.sep + "FlatFields" + os.sep + "DC_blue_RAW.npy")
    # SURVEY_DC_NIR = np.load(modpath + os.sep + "FlatFields" + os.sep + "DC_nir_RAW.npy")
    # with open(modpath + os.sep + "FlatFields" + os.sep + "2015_0522_232450_001.RAW", "rb") as ndvi:
    #     SURVEY_DC_NDVI = np.fromfile(ndvi, np.dtype('u2'), 3456 * 4608).reshape((3456,4608))
    # SURVEY_DC_RGB = np.load(modpath + os.sep + "FlatFields" + os.sep + "DC_rgb_RAW.npy")
    # FC350_DC_NDVI = 0 #np.load(modpath + os.sep + "FlatFields" + os.sep + "DC_FC350_DNG.npy")
    # FC330_DC_NDVI = 0 #np.load(modpath + os.sep + "FlatFields" + os.sep + "DC_FC330_DNG.npy")
    # FC300S_DC_NDVI = 0 #np.load(modpath + os.sep + "FlatFields" + os.sep + "DC_FC300S_DNG.npy")
    # FC300X_DC_NDVI = 0 #np.load(modpath + os.sep + "FlatFields" + os.sep + "DC_FC300X_DNG.npy")

    SQ_TO_TARG = 2.1875
    SQ_TO_SQ = 5.0
    TARGET_LENGTH = 2.0
    TARG_TO_TARG = 2.6

    imcols = 4608
    imrows = 3456
    imsize = imcols * imrows
    closingPlugin = pyqtSignal()
    firstpass = True
    useqr = False
    qrcoeffs = [] #  Red Intercept, Red Slope,  Green Intercept, Green Slope, Blue Intercept, Blue Slope
    refvalues = {
        "660/850":[[87.032549, 52.135779, 23.664799],[0, 0, 0],[84.63514, 51.950608, 22.795518]],
        "446/800":[[0.8419608509,0.520440145,0.230113958],[0,0,0],[0.8645652801,0.5037779363,0.2359041624]],
        "850":[[0.8463514, 0.51950608, 0.22795518], [0, 0, 0],[0, 0, 0]],
        "808":[[0,0,0],[0,0,0],[0,0,0]],
        "650":[[0.87032549, 0.52135779, 0.23664799],[0, 0, 0],[0, 0, 0]],
        "548":[[0, 0, 0],[0.87415089, 0.51734381, 0.24032515],[0, 0, 0]],
        "450":[[0, 0, 0],[0, 0, 0],[0.86469794, 0.50392915, 0.23565447]]
    }

    # with open("./values.csv") as values:
    #     refvalues = csv.reader(values)

    def __init__(self, parent=None):
        """Constructor."""
        super(MAPIR_ProcessingDockWidget, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

#Pre-Process Steps: Start
    def on_PreProcessInButton_released(self):
        self.PreProcessInFolder.setText(QtGui.QFileDialog.getExistingDirectory())
    def on_PreProcessOutButton_released(self):
        self.PreProcessOutFolder.setText(QtGui.QFileDialog.getExistingDirectory())
    def on_PreProcessButton_released(self):
        if self.PreProcessCameraModel.currentIndex() == -1:
            self.PreProcessLog.append("Attention! Please select a camera model.\n")
        else:
            infolder = self.PreProcessInFolder.text()
            outfolder = self.PreProcessOutFolder.text()
            self.PreProcessLog.append("Input folder: " + infolder)
            self.PreProcessLog.append("Output folder: " + outfolder)
            infiles = []
            if "DJI" in self.PreProcessCameraModel.currentText():
                os.chdir(infolder)
                infiles.extend(glob.glob("." + os.sep + "*.[dD][nN][gG]"))
                counter = 0
                for input in infiles:
                    self.PreProcessLog.append(
                        "processing image: " + str((counter) + 1) + " of " + str(len(infiles)) +
                        " " + input.split('\\')[1])
                    self.openDNG(input, outfolder)

                    counter += 1
            else:
                os.chdir(infolder)
                infiles.extend(glob.glob("." + os.sep + "*.[rR][aA][wW]*"))
                infiles.extend(glob.glob("." + os.sep + "*.[jJ][pP][gG]*"))
                infiles.sort()

                if ("RAW" in infiles[0].upper()) and ("JPG" in infiles[1].upper()):
                     counter = 0
                     for input in infiles[::2]:
                         self.PreProcessLog.append("processing image: " + str((counter / 2) + 1) + " of " + str(len(infiles) / 2) +
                                                  " " + input.split(os.sep)[1])
                         with open(input, "rb") as rawimage:
                             img = np.fromfile(rawimage, np.dtype('u2'), self.imsize).reshape((self.imrows,self.imcols))
                             color = cv2.cvtColor(img,cv2.COLOR_BAYER_RG2RGB)
                             if self.RgbBox.isChecked():
                                if self.PreProcessCameraModel.currentIndex() == 1:
                                    cv2.merge((color[:, :, 0] * 2, color[:, :, 1], color[:, :, 2] * 2), color)
                                    cv2.norm(color,cv2.NORM_MINMAX)
                                else:
                                    self.PreProcessLog.append("Normalization for RGB camera models only")


                             filename = input.split('.')
                             outputfilename = filename[1] + '.tif'

                             cv2.imwrite(outfolder + outputfilename, color)
                             self.copyExif(infiles[counter + 1], outfolder + outputfilename)
                         counter += 2

                else:
                    self.PreProcessLog.append("Incorrect file structure. Please arrange files in a RAW, JPG, RAW, JGP... format.")
# Pre-Process Steps: End

# Calibration Steps: Start
    def on_CalibrationInButton_released(self):
        self.CalibrationInFolder.setText(QtGui.QFileDialog.getExistingDirectory())
    def on_CalibrationQRButton_released(self):
        self.CalibrationQRFile.setText(QtGui.QFileDialog.getOpenFileName())
    def on_CalibrationGenButton_released(self):
        if self.CalibrationCameraModel.currentIndex() == -1:
            self.CalibrationLog.append("Attention! Please select a camera model.\n")
        elif len(self.CalibrationQRFile.text()) > 0:
            self.qrcoeffs = self.findQR(self.CalibrationQRFile.text())
            self.useqr = True
        else:
            self.CalibrationLog.append("Attention! Please select a target image.\n")
    def on_CalibrateButton_released(self):
        if self.CalibrationCameraModel.currentIndex() == -1:
            self.CalibrationLog.append("Attention! Please select a camera model.\n")
        elif len(self.CalibrationInFolder.text()) <= 0:
            self.CalibrationLog.append("Attention! Please select a calibration folder.\n")
        else:
            self.firstpass = True
            # self.CalibrationLog.append("CSV Input: \n" + str(self.refvalues))
            # self.CalibrationLog.append("Calibration button pressed.\n")
            calfolder = self.CalibrationInFolder.text()
            # self.CalibrationLog.append("Calibration target folder is: " + calfolder + "\n")
            files_to_calibrate = []
            os.chdir(calfolder)
            files_to_calibrate.extend(glob.glob("." + os.sep + "*.[tT][iI][fF]*"))
            files_to_calibrate.extend(glob.glob("." + os.sep + "*.[jJ][pP][gG]*"))
            #self.CalibrationLog.append("Files to calibrate[0]: " + files_to_calibrate[0])
            pixel_min_max = {"redmax" : 0.0, "redmin" : 65535.0,
                             "greenmax" : 0.0, "greenmin" : 65535.0,
                             "bluemax" : 0.0, "bluemin" : 65535.0}
            if "tif" or "TIF" or "jpg" or "JPG" in files_to_calibrate[0]:
                # self.CalibrationLog.append("Found files to Calibrate.\n")
                outdir = calfolder + os.sep + "Calibrated"
                if not os.path.exists(outdir):
                    os.mkdir(outdir)

                for calpixel in files_to_calibrate:

                    img = cv2.imread(calpixel, -1)


                    if self.CalibrationCameraModel.currentIndex() == 5: #Survey1_NDVI
                        # img = img.astype('float')

                        img[:, :, 0] = img[:, :, 0] - ((img[:, :, 2] / 5) * 4)
                    elif self.CalibrationCameraModel.currentIndex() == 0 or self.CalibrationCameraModel.currentIndex() > 5: #Survey2 NDVI, DJI NDVI cameras
                        # img = img.astype('float')

                        img[:, :, 2] = img[:, :, 2] - ((img[:, :, 0] / 5) * 4)
                    # these are a little confusing, but the check to find the highest and lowest pixel value
                    # in each channel in each image and keep the highest/lowest value found.
                    pixel_min_max["redmax"] = max(img[:, :, 2].max(), pixel_min_max["redmax"])
                    pixel_min_max["redmin"] = min(img[:, :, 2].min(), pixel_min_max["redmin"])
                    pixel_min_max["greenmax"] = max(img[:, :, 1].max(), pixel_min_max["greenmax"])
                    pixel_min_max["greenmin"] = min(img[:, :, 1].min(), pixel_min_max["greenmin"])
                    pixel_min_max["bluemax"] = max(img[:, :, 0].max(), pixel_min_max["bluemax"])
                    pixel_min_max["bluemin"] = min(img[:, :, 0].min(), pixel_min_max["bluemin"])


                if self.useqr == True:
                    pixel_min_max["redmax"] = pixel_min_max["redmax"] * self.qrcoeffs[1] + self.qrcoeffs[0]
                    pixel_min_max["redmin"] = pixel_min_max["redmin"] * self.qrcoeffs[1] + self.qrcoeffs[0]
                    pixel_min_max["greenmax"] = pixel_min_max["greenmax"] * self.qrcoeffs[3] + self.qrcoeffs[2]
                    pixel_min_max["greenmin"] = pixel_min_max["greenmin"] * self.qrcoeffs[3] + self.qrcoeffs[2]
                    pixel_min_max["bluemax"] = pixel_min_max["bluemax"] * self.qrcoeffs[5] + self.qrcoeffs[4]
                    pixel_min_max["bluemin"] = pixel_min_max["bluemin"] * self.qrcoeffs[5] + self.qrcoeffs[4]

                else:
                    if self.CalibrationCameraModel.currentIndex() == 5:  # Survey1_NDVI
                        if "tif" or "TIF" in calpixel:
                            pixel_min_max["redmax"] = (pixel_min_max["redmax"] * self.BASE_COEFF_SURVEY1_NDVI_TIF[1])\
                                + self.BASE_COEFF_SURVEY1_NDVI_TIF[0]
                            pixel_min_max["redmin"] = (pixel_min_max["redmin"] * self.BASE_COEFF_SURVEY1_NDVI_TIF[1])\
                                + self.BASE_COEFF_SURVEY1_NDVI_TIF[0]
                            pixel_min_max["bluemin"] = (pixel_min_max["bluemin"] * self.BASE_COEFF_SURVEY1_NDVI_TIF[3])\
                                + self.BASE_COEFF_SURVEY1_NDVI_TIF[2]
                            pixel_min_max["bluemax"] = (pixel_min_max["bluemax"] * self.BASE_COEFF_SURVEY1_NDVI_TIF[3])\
                                + self.BASE_COEFF_SURVEY1_NDVI_TIF[2]
                        elif "jpg" or "JPG" in calpixel:
                            pixel_min_max["redmax"] = (pixel_min_max["redmax"] * self.BASE_COEFF_SURVEY1_NDVI_JPG[1])\
                                + self.BASE_COEFF_SURVEY1_NDVI_JPG[0]
                            pixel_min_max["redmin"] = (pixel_min_max["redmin"] * self.BASE_COEFF_SURVEY1_NDVI_JPG[1])\
                                + self.BASE_COEFF_SURVEY1_NDVI_JPG[0]
                            pixel_min_max["bluemin"] = (pixel_min_max["bluemin"] * self.BASE_COEFF_SURVEY1_NDVI_JPG[3])\
                                + self.BASE_COEFF_SURVEY1_NDVI_JPG[2]
                            pixel_min_max["bluemax"] = (pixel_min_max["bluemax"] * self.BASE_COEFF_SURVEY1_NDVI_JPG[3])\
                                + self.BASE_COEFF_SURVEY1_NDVI_JPG[2]
                    if self.CalibrationCameraModel.currentIndex() == 0\
                            or self.CalibrationCameraModel.currentIndex() > 5:  # Survey2_NDVI

                        if "tif" or "TIF" in calpixel:
                            pixel_min_max["redmax"] = (pixel_min_max["redmax"] * self.BASE_COEFF_SURVEY2_NDVI_TIF[1])\
                                + self.BASE_COEFF_SURVEY2_NDVI_TIF[0]
                            pixel_min_max["redmin"] = (pixel_min_max["redmin"] * self.BASE_COEFF_SURVEY2_NDVI_TIF[1])\
                                + self.BASE_COEFF_SURVEY2_NDVI_TIF[0]
                            pixel_min_max["bluemin"] = (pixel_min_max["bluemin"] * self.BASE_COEFF_SURVEY2_NDVI_TIF[3])\
                                + self.BASE_COEFF_SURVEY2_NDVI_TIF[2]
                            pixel_min_max["bluemax"] = (pixel_min_max["bluemax"] * self.BASE_COEFF_SURVEY2_NDVI_TIF[3])\
                                + self.BASE_COEFF_SURVEY2_NDVI_TIF[2]
                        elif "jpg" or "JPG" in calpixel:
                            pixel_min_max["redmax"] = (pixel_min_max["redmax"] * self.BASE_COEFF_SURVEY2_NDVI_JPG[1])\
                                + self.BASE_COEFF_SURVEY2_NDVI_JPG[0]
                            pixel_min_max["redmin"] = (pixel_min_max["redmin"] * self.BASE_COEFF_SURVEY2_NDVI_JPG[1])\
                                + self.BASE_COEFF_SURVEY2_NDVI_JPG[0]
                            pixel_min_max["bluemin"] = (pixel_min_max["bluemin"] * self.BASE_COEFF_SURVEY2_NDVI_JPG[3])\
                                + self.BASE_COEFF_SURVEY2_NDVI_JPG[2]
                            pixel_min_max["bluemax"] = (pixel_min_max["bluemax"] * self.BASE_COEFF_SURVEY2_NDVI_JPG[3])\
                                + self.BASE_COEFF_SURVEY2_NDVI_JPG[2]

                for calfile in files_to_calibrate:
                    
                    cameramodel = self.CalibrationCameraModel.currentIndex()
                    if self.useqr is True:
                        # self.CalibrationLog.append("Using QR")
                        self.CalibratePhotos(calfile, self.qrcoeffs, pixel_min_max, outdir)
                    else:
                        # self.CalibrationLog.append("NOT Using QR")
                        if cameramodel == 0: # Survey2 NDVI
                            if "TIF" in calfile.split('.')[2].upper():
                                self.CalibratePhotos(calfile,self.BASE_COEFF_SURVEY2_NDVI_TIF, pixel_min_max, outdir)
                            elif "JPG" in calfile.split('.')[2].upper():
                                self.CalibratePhotos(calfile, self.BASE_COEFF_SURVEY2_NDVI_JPG, pixel_min_max, outdir)
                        elif cameramodel == 1:# Survey2 NIR
                            if "TIF" in calfile.split('.')[2].upper():
                                self.CalibratePhotos(calfile,self.BASE_COEFF_SURVEY2_NIR_TIF, pixel_min_max, outdir)
                            elif "JPG" in calfile.split('.')[2].upper():
                                self.CalibratePhotos(calfile, self.BASE_COEFF_SURVEY2_NIR_JPG, pixel_min_max, outdir)
                        elif cameramodel == 2:# Survey2 RED
                            if "TIF" in calfile.split('.')[2].upper():
                                self.CalibratePhotos(calfile,self.BASE_COEFF_SURVEY2_RED_TIF, pixel_min_max, outdir)
                            elif "JPG" in calfile.split('.')[2].upper():
                                self.CalibratePhotos(calfile, self.BASE_COEFF_SURVEY2_RED_JPG, pixel_min_max, outdir)
                        elif cameramodel == 3:# Survey2 GREEN
                            if "TIF" in calfile.split('.')[2].upper():
                                self.CalibratePhotos(calfile,self.BASE_COEFF_SURVEY2_GREEN_TIF, pixel_min_max, outdir)
                            elif "JPG" in calfile.split('.')[2].upper():
                                self.CalibratePhotos(calfile, self.BASE_COEFF_SURVEY2_GREEN_JPG, pixel_min_max, outdir)
                        elif cameramodel == 4:# Survey2 BLUE
                            if "TIF" in calfile.split('.')[2].upper():
                                self.CalibratePhotos(calfile,self.BASE_COEFF_SURVEY2_BLUE_TIF,pixel_min_max, outdir)
                            elif "JPG" in calfile.split('.')[2].upper():
                                self.CalibratePhotos(calfile, self.BASE_COEFF_SURVEY2_BLUE_JPG, pixel_min_max, outdir)
                        elif cameramodel == 5:# Survey1 NDVI
                            if "JPG" in calfile.split('.')[2].upper():
                                self.CalibratePhotos(calfile, self.BASE_COEFF_SURVEY1_NDVI_JPG, pixel_min_max, outdir)
                        elif cameramodel == 6:# DJI X3 NDVI
                            if "TIF" in calfile.split('.')[2].upper():
                                self.CalibratePhotos(calfile,self.BASE_COEFF_DJIX3_NDVI_TIF,pixel_min_max, outdir)
                            elif "JPG" in calfile.split('.')[2].upper():
                                self.CalibratePhotos(calfile, self.BASE_COEFF_DJIX3_NDVI_JPG, pixel_min_max, outdir)
                        elif cameramodel == 7:# DJI Phantom3 NDVI
                            if "TIF" in calfile.split('.')[2].upper():
                                self.CalibratePhotos(calfile,self.BASE_COEFF_DJIPHANTOM3_NDVI_TIF,pixel_min_max, outdir)
                            elif "JPG" in calfile.split('.')[2].upper():
                                self.CalibratePhotos(calfile, self.BASE_COEFF_DJIPHANTOM3_NDVI_JPG, pixel_min_max, outdir)
                        elif cameramodel == 8:# DJI PHANTOM4 NDVI
                            if "TIF" in calfile.split('.')[2].upper():
                                self.CalibratePhotos(calfile,self.BASE_COEFF_DJIPHANTOM4_NDVI_TIF,pixel_min_max, outdir)
                            elif "JPG" in calfile.split('.')[2].upper():
                                self.CalibratePhotos(calfile, self.BASE_COEFF_DJIPHANTOM4_NDVI_JPG, pixel_min_max, outdir)
                        else:
                            self.CalibrationLog.append("No default calibration data for selected camera model. Please use a MAPIR Reflectance Target.\n")
                self.CalibrationLog.append("Finished Calibrating " + str(len(files_to_calibrate)) + " images\n")

    def CalibratePhotos(self, photo, coeffs, minmaxes, output_directory):
        refimg = cv2.imread(photo, -1)


        ### split channels (using cv2.split caused too much overhead and made the host program crash)
        blue = refimg[:, :, 0]
        green = refimg[:, :, 1]
        red = refimg[:, :, 2]


        ### find the maximum and minimum pixel values over the entire directory.
        if self.CalibrationCameraModel.currentIndex() == 5: ###Survey1 NDVI
            maxpixel = minmaxes["redmax"] if minmaxes["redmax"] > minmaxes["bluemax"] else minmaxes["bluemax"]
            minpixel = minmaxes["redmin"] if minmaxes["redmin"] < minmaxes["bluemin"] else minmaxes["bluemin"]
            blue = refimg[:, :, 0] - (refimg[:, :, 2] * 0.80)# Subtract the NIR bleed over from the blue channel
        elif self.CalibrationCameraModel.currentIndex() == 1 or self.CalibrationCameraModel.currentIndex() == 2:
            ### red and NIR
            maxpixel = minmaxes["redmax"]
            minpixel = minmaxes["redmin"]
        elif self.CalibrationCameraModel.currentIndex() == 3:
            ### green
            maxpixel = minmaxes["greenmax"]
            minpixel = minmaxes["greenmin"]
        elif self.CalibrationCameraModel.currentIndex() == 4:
            ### blue
            maxpixel = minmaxes["bluemax"]
            minpixel = minmaxes["bluemin"]
        else: ###Survey2 NDVI or any DJI ndvi
            maxpixel = minmaxes["redmax"] if minmaxes["redmax"] > minmaxes["bluemax"] else minmaxes["bluemax"]
            minpixel = minmaxes["redmin"] if minmaxes["redmin"] < minmaxes["bluemin"] else minmaxes["bluemin"]
            red = refimg[:, :, 2] - (refimg[:, :, 0] * 0.80)# Subtract the NIR bleed over from the red channel





    ### Calibrate pixels based on the default reflectance values (or the values gathered from the MAPIR reflectance target)
        red = (red * coeffs[1]) + coeffs[0]
        green = (green * coeffs[3]) + coeffs[2]
        blue = (blue * coeffs[5]) + coeffs[4]

    ### Scale calibrated values back down to a useable range (Adding 1 to avaoid 0 value pixels, as they will cause a
    #### devide by zero case when creating an index image.
        if "JPG" in photo.split('.')[2].upper():
            red = (((red - minpixel + 1) / (maxpixel - minpixel + 1)) * 255)
            green = (((green - minpixel + 1) / (maxpixel - minpixel + 1)) * 255)
            blue = (((blue - minpixel + 1) / (maxpixel - minpixel + 1)) * 255)
        else:
            red = (((red - minpixel + 1) / (maxpixel - minpixel + 1)) * 65535)
            green = (((green - minpixel + 1) / (maxpixel - minpixel + 1)) * 65535)
            blue = (((blue - minpixel + 1) / (maxpixel - minpixel + 1)) * 65535)



    ### remove the floating point values from the 3 channels
        red = np.floor(red)
        green = np.floor(green)
        blue = np.floor(blue)



        if photo.split('.')[2].upper() == "JPG": #Remove the gamma correction that is automaticall applied to JPGs
            # self.CalibrationLog.append("Removing Gamma")
            red = np.power(red, 1/2.2)
            green = np.power(green, 1/2.2)
            blue = np.power(blue, 1/2.2)

    ### Merge the channels back into a single image
        refimg[:, :, 0] = blue
        refimg[:, :, 1] = green
        refimg[:, :, 2] = red

    ### If the image is a .tiff then change it to a 16 bit color image
        if "TIF" in photo.split('.')[2].upper():
            refimg = refimg.astype("uint16")



        if self.CalibrationCameraModel.currentIndex() == 0 or self.CalibrationCameraModel.currentIndex() >= 5:
            ### Remove green information if NDVI camera
            refimg[:, :, 1] = 1
        elif self.CalibrationCameraModel.currentIndex() == 1 or self.CalibrationCameraModel.currentIndex() == 2:
            ### Remove blue and green information if NIR or Red camera
            refimg[:, :, 0] = 1
            refimg[:, :, 1] = 1
        elif self.CalibrationCameraModel.currentIndex() == 3:
            ### Remove blue and red information if GREEN camera
            refimg[:, :, 0] = 1
            refimg[:, :, 2] = 1
        elif self.CalibrationCameraModel.currentIndex() == 4:
            ### Remove red and green information if BLUE camera
            refimg[:, :, 1] = 1
            refimg[:, :, 2] = 1


        if self.Tiff2JpgBox.checkState() > 0:
            cv2.imencode(".jpg", refimg)
            cv2.imwrite(output_directory + photo.split('.')[1] + "_CALIBRATED.JPG", refimg, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
            self.copyExif(photo, output_directory + photo.split('.')[1] + "_CALIBRATED.JPG")
            # if self.IndexBox.checkState() > 0:
            #     indeximg = (blue - red) / (blue + red)
            #     indeximg = indeximg.astype("float32")
            #     cv2.imwrite(output_directory + photo.split('.')[1] + "_Indexed.JPG", indeximg, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
            #     self.copyExif(photo, output_directory + photo.split('.')[1] + "_Indexed.JPG")
        else:
            cv2.imwrite(output_directory + photo.split('.')[1] + "_CALIBRATED." + photo.split('.')[2], refimg)
            self.copyExif(photo, output_directory + photo.split('.')[1] + "_CALIBRATED." + photo.split('.')[2])
            # if self.IndexBox.checkState() > 0:
            #     indeximg = (blue - red) / (blue + red)
            #     cv2.imwrite(output_directory + photo.split('.')[1] + "_Indexed." + photo.split('.')[2], indeximg)
            #     self.copyExif(photo, output_directory + photo.split('.')[1] + "_Indexed" + photo.split('.')[2])


####Function for finding he QR target and calculating the calibration coeficients
    def findQR(self, image):
        im = cv2.imread(image)
        grayscale = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)

        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        cl1 = clahe.apply(grayscale)

        denoised = cv2.fastNlMeansDenoising(cl1,None,14,7,21)

        threshcounter = 0
        while threshcounter <= 255:
            ret, thresh = cv2.threshold(denoised, threshcounter, 255, 0)

            im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            coords = []
            count = 0

            for i in hierarchy[0]:

                self.traverseHierarchy(hierarchy, contours, count, im, 0, coords)

                count += 1
            if len(coords) == 3:
                break
            else:
                threshcounter += 5


        if len(coords) is not 3:
            self.CalibrationLog.append("Could not find MAPIR ground target.")
            return

        line1 = np.sqrt(np.power((coords[0][0] - coords[1][0]), 2) + np.power((coords[0][1] - coords[1][1]), 2))  # Getting the distance between each centroid
        line2 = np.sqrt(np.power((coords[1][0] - coords[2][0]), 2) + np.power((coords[1][1] - coords[2][1]), 2))
        line3 = np.sqrt(np.power((coords[2][0] - coords[0][0]), 2) + np.power((coords[2][1] - coords[0][1]), 2))

        hypotenuse = line1 if line1 > line2 else line2
        hypotenuse = line3 if line3 > hypotenuse else hypotenuse

        if hypotenuse == line1:

            slope = (coords[1][1] - coords[0][1])/(coords[1][0] - coords[0][0])
            dist = coords[2][1] - (slope * coords[2][0]) + ((slope * coords[1][0]) - coords[1][1])
            dist /= np.sqrt(np.power(slope,2) + 1)
            center = coords[2]
            if (slope < 0 and dist < 0) or (slope >= 0 and dist >= 0):

                bottom = coords[0]
                right = coords[1]
            else:

                bottom = coords[1]
                right = coords[0]
        elif hypotenuse == line2:

            slope = (coords[2][1] - coords[1][1]) / (coords[2][0] - coords[1][0])
            dist = coords[0][1] - (slope * coords[0][0]) + ((slope * coords[2][0]) - coords[2][1])
            dist /= np.sqrt(np.power(slope, 2) + 1)
            center = coords[0]
            if (slope < 0 and dist < 0) or (slope >= 0 and dist >= 0):

                bottom = coords[1]
                right = coords[2]
            else:

                bottom = coords[2]
                right = coords[1]
        else:

            slope = (coords[0][1] - coords[2][1]) / (coords[0][0] - coords[2][0])
            dist = coords[1][1] - (slope * coords[1][0]) + ((slope * coords[0][0]) - coords[0][1])
            dist /= np.sqrt(np.power(slope, 2) + 1)
            center = coords[1]
            if (slope < 0 and dist < 0) or (slope >= 0 and dist >= 0):
                # self.CalibrationLog.append("slope and dist share sign")
                bottom = coords[0]
                right = coords[2]
            else:

                bottom = coords[2]
                right = coords[0]




        guidelength = np.sqrt(np.power((center[0] - bottom[0]), 2) + np.power((center[1] - bottom[1]), 2))
        pixelinch = guidelength/self.SQ_TO_SQ

        rad = (pixelinch * self.SQ_TO_TARG)
        vx = center[0] - bottom[0]
        vy = center[1] - bottom[1]
        newlen = np.sqrt(vx*vx + vy*vy)
        targ1x = (rad * (vx / newlen)) + center[0]
        targ1y = (rad * (vy / newlen)) + center[1]
        targ3x = (rad * (vx / newlen)) + right[0]
        targ3y = (rad * (vy / newlen)) + right[1]


        target1 = (int(targ1x),int(targ1y))
        target3 = (int(targ3x),int(targ3y))
        target2 = ((np.abs(target1[0] + target3[0])) / 2, np.abs((target1[1] + target3[1])) / 2)


        im2 = cv2.imread(image, -1)
        # im2 = im2.astype('float')
        blue = im2[:, :, 0]
        green = im2[:, :, 1]
        red = im2[:, :, 2] - ((im2[:, :, 0]/5) * 4)

        red = np.floor(red)
        if "TIF" in image.split('.')[1].upper():
            red = red.astype("uint16")
            blue = blue.astype("uint16")
            green = green.astype("uint16")
        im2 = cv2.merge((blue, green, red))



        targ1values = im2[(target1[1] - ((pixelinch * 0.75) / 2)):(target1[1] + ((pixelinch * 0.75) / 2)),
                      (target1[0] - ((pixelinch * 0.75) / 2)):(target1[0] + ((pixelinch * 0.75) / 2))]
        targ2values = im2[(target2[1] - ((pixelinch * 0.75) / 2)):(target2[1] + ((pixelinch * 0.75) / 2)),
                      (target2[0] - ((pixelinch * 0.75) / 2)):(target2[0] + ((pixelinch * 0.75) / 2))]
        targ3values = im2[(target3[1] - ((pixelinch * 0.75) / 2)):(target3[1] + ((pixelinch * 0.75) / 2)),
                      (target3[0] - ((pixelinch * 0.75) / 2)):(target3[0] + ((pixelinch * 0.75) / 2))]


        t1redmean = np.mean(targ1values[:, :, 2])/100
        t1greenmean = np.mean(targ1values[:, :, 1])/100
        t1bluemean = np.mean(targ1values[:, :, 0])/100
        t2redmean = np.mean(targ2values[:, :, 2])/100
        t2greenmean = np.mean(targ2values[:, :, 1])/100
        t2bluemean = np.mean(targ2values[:, :, 0])/100
        t3redmean = np.mean(targ3values[:, :, 2])/100
        t3greenmean = np.mean(targ3values[:, :, 1])/100
        t3bluemean = np.mean(targ3values[:, :, 0])/100


        yred = [0.87, 0.51, 0.23]
        yblue = [0.87, 0.51, 0.23]
        ygreen = [0.87, 0.51, 0.23]
        if 1 <= self.CalibrationCameraModel.currentIndex() <= 4:
            if self.CalibrationCameraModel.currentIndex() == 1:
                yred = self.refvalues["850"][0]
                ygreen = self.refvalues["850"][1]
                yblue = self.refvalues["850"][2]
            elif self.CalibrationCameraModel.currentIndex() == 2:
                yred = self.refvalues["650"][0]
                ygreen = self.refvalues["650"][1]
                yblue = self.refvalues["650"][2]
            elif self.CalibrationCameraModel.currentIndex() == 3:
                yred = self.refvalues["548"][0]
                ygreen = self.refvalues["548"][1]
                yblue = self.refvalues["548"][2]
            elif self.CalibrationCameraModel.currentIndex() == 4:
                yred = self.refvalues["450"][0]
                ygreen = self.refvalues["450"][1]
                yblue = self.refvalues["450"][2]
        else:
            yred = self.refvalues["660/850"][0]
            ygreen = self.refvalues["660/850"][1]
            yblue = self.refvalues["660/850"][2]

        xred = [t1redmean, t2redmean, t3redmean]
        xgreen = [t1greenmean, t2greenmean, t3greenmean]
        xblue = [t1bluemean, t2bluemean, t3bluemean]


        redslope, redintcpt, r_value, p_value, std_err = stats.linregress(xred, yred)

        greenslope, greenintcpt, r_value, p_value, std_err = stats.linregress(xgreen, ygreen)

        blueslope, blueintcpt, r_value, p_value, std_err = stats.linregress(xblue, yblue)




        self.CalibrationLog.append("Found QR Target, please proceed with calibration.")


        return [redintcpt, redslope, greenintcpt, greenslope, blueintcpt, blueslope]

    def traverseHierarchy(self, tier, cont, index, image, depth , coords):

        if tier[0][index][2] != -1:
            self.traverseHierarchy(tier,cont,tier[0][index][2],image,depth + 1, coords)
            return
        elif depth >= 2:
            c = cont[index]
            moment = cv2.moments(c)
            if int(moment['m00']) != 0:
                x = int(moment['m10']/moment['m00'])
                y = int(moment['m01']/moment['m00'])
                coords.append([x, y])
            return




# Calibration Steps: End


# Helper functions
    def openDNG(self, inphoto, outfolder):
        subprocess.call("dcraw -T " + inphoto, shell=True)
        newfile = "./" + inphoto.split(".")[1] + ".tiff"
        self.copyExif(inphoto, newfile)
        shutil.move(newfile, outfolder)
    def copyExif(self, inphoto, outphoto):
        # self.PreProcessLog.append(str(os.path.abspath(inphoto)))
        # self.PreProcessLog.append(str(outphoto))
        # subprocess.call(pypath + os.sep + "Scripts" + os.sep + "exiftool.exe -overwrite_original -tagsfromfile " + os.path.abspath(inphoto) + ' ' + os.path.abspath(outphoto), shell=True)
        with exiftool.ExifTool() as et:
            et.execute("-overwrite_original", "-tagsfromfile", os.path.abspath(inphoto), os.path.abspath(outphoto))
    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()

