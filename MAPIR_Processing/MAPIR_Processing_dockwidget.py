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
from PyQt4 import uic, QtGui
from PyQt4.QtCore import pyqtSignal
from qgis.core import QgsMessageLog
import cv2
import numpy as np
import exiftool
import glob




FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'MAPIR_Processing_dockwidget_base.ui'))


class MAPIR_ProcessingDockWidget(QtGui.QDockWidget, FORM_CLASS):

    closingPlugin = pyqtSignal()

    def __init__(self, parent=None):
        """Constructor."""
        super(MAPIR_ProcessingDockWidget, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

    def on_PreProcessInButton_released(self):
        self.PreProcessInFolder.setText(QtGui.QFileDialog.getExistingDirectory())
    def on_PreProcessOutButton_released(self):
        self.PreProcessOutFolder.setText(QtGui.QFileDialog.getExistingDirectory())
    def on_PreProcessButton_released(self):
        infolder = self.PreProcessInFolder.text()
        outfolder = self.PreProcessOutFolder.text()
        os.umask(0)
        rawext = '*.RAW'
        imcols = 4608
        imrows = 3456
        imsize = imcols * imrows
        infiles = []
        if "DJI" in self.PreProcessCameraModel.currentText():
            os.chdir(infolder)
            infiles.extend(glob.glob("./*.DNG"))
        else:
            print "infolder: " + infolder
            os.chdir(infolder)
            infiles.extend(glob.glob("./*.RAW"))
            infiles.extend(glob.glob("./*.JPG"))
            print "Input:\n"
            print infiles
            infiles.sort()
            print "Sorted: \n"
            print infiles
            QgsMessageLog.logMessage(outfolder)
            if ("RAW" in infiles[0]) and ("JPG" in infiles[1]):
                 counter = 0
                 for input in infiles[::2]:
                     print input
                     with open(input, "rb") as rawimage:
                         img = np.fromfile(rawimage, np.dtype('u2'), imsize).reshape((imrows,imcols))
                         color = cv2.cvtColor(img,cv2.COLOR_BAYER_RG2RGB)
                         filename = input.split('.')
                         outputfilename = filename[1] + '.TIFF'
                         #print "Outputfilename: " + outputfilename
                         QgsMessageLog.logMessage(outputfilename)
                         cv2.imwrite(outfolder + outputfilename, color)
                     with exiftool.ExifTool() as et:
                         #print "infiles[i + 1]: " + infiles[counter+1]
                         QgsMessageLog.logMessage(infiles[counter+1])
                         et.execute("-overwrite_original", "-tagsfromfile", "\"" + infiles[counter+1] + "\"", "\"" + outfolder + outputfilename + "\"")
                     counter += 2
        #todo Print variables to make sure all of the new code is fetching data properly.

         
    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()

