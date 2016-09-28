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

from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSignal
from osgeo import gdal
import cv2
import numpy as np
import time

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
    def on_pushButton_clicked(self):
        infile = '/home/ethan/Downloads/test_ndvi/2015_0121_230450_001.RAW'
        imcols = 4608
        imrows = 3456
        imsize = imcols*imrows
        with open(infile, "rb") as rawimage:
            os.umask(0)
            img = np.fromfile(rawimage, np.dtype('u2'), imsize).reshape((imrows,imcols))
            colour = cv2.cvtColor(img, cv2.COLOR_BAYER_RG2RGB)
            cv2.imwrite('/home/ethan/Downloads/test_ndvi/newtiff.TIFF', colour)
            exifsrc = gdal.Open('/home/ethan/Downloads/test_ndvi/2015_0121_230452_002.JPG')
            exifdst = gdal.Open('/home/ethan/Downloads/test_ndvi/newtiff.TIFF')
            exifdst.SetMetadata(exifsrc.GetMetadata())
            print exifdst.GetMetadata()

         
    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()

