# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MAPIR
                                 A QGIS plugin
 The MAPIR plugin allows for calibrating and processing images taken b the MAPIR camera
                             -------------------
        begin                : 2016-09-12
        copyright            : (C) 2016 by Peau Productions
        email                : info@peauproductions.com
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
    """Load MAPIR class from file MAPIR.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .MAPIR import MAPIR
    return MAPIR(iface)
