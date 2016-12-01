# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MAPIR_Processing
                                 A QGIS plugin
 Widget for processing images captured by MAPIR cameras
                             -------------------
        begin                : 2016-09-26
        copyright            : (C) 2016 by Peau Productions
        email                : ethan@peauproductions.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load MAPIR_Processing class from file MAPIR_Processing.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .MAPIR_Processing import MAPIR_Processing
    return MAPIR_Processing(iface)
