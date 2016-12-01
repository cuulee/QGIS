# QGIS Distribution for MAPIR Cameras
This repository contains the QGIS distribution for use with MAPIR cameras. The distribution is in a beta stage while we work on getting it placed in the QGIS plugin repository.

Camera supported:
- MAPIR Survey2 (all filter models)
- DJI Inspire X3 with [PEAU 3.97mm NDVI (Red+NIR) lens](http://www.peauproductions.com/products/gp39728) installed
- DJI Phantom 4 & 3 with [PEAU 3.97mm NDVI (Red+NIR) lens](http://www.peauproductions.com/products/gp39728) installed

Functionality for above supported cameras includes:
- Convert Survey2 RAW to TIFF, converts DJI DNG to TIFF
- Calibrate directory of images using [MAPIR Reflectance Target](http://www.mapir.camera/collections/accessories/products/mapir-camera-calibration-ground-target-package) image taken before survey or uses built-in reflectance values if no target image supplied
- Converts TIFF to JPG after calibration if desired

Functionality still in the works:
- Correcting vignette
- Normalizing color (RGB) photos
- Creating index images

### Installation
- Whe hope to have the plugin added to the QGIS plugin repository, but until then, please download the [MAPIR_Processing folder](https://github.com/mapircamera/QGIS/tree/master/Packages) and add it to you .qgis2/python/plugins folder
- In Windows, the .qgis2 folder is in C:\Users\<your user name>

### Using Plugin
#### Note, you'll need to run QGIS as an administrator the first time you load this plugin.

- To pre-process images (convet RAW images to TIFFs):
-- Select the "Pre-Process" tab
-- Select a camera model
-- Select an input folder
-- Select an output folder
-- Press the "Pre-Process Images" button

- To Calibrate images
-- Select the "Calibrate" tab
-- Select a camera model
-- Select a MAPIR ground target image (optional)
-- Press the "Generate Calibration Values" button
-- Select a folder containing images to calibrate
-- Press the "Calibrate Images From Directory" button

### Credits
 - [Photomonitoring Plugin](https://github.com/nedhorning/PhotoMonitoringPlugin) by Ned Horning - American Museum of Natural History, Center for Biodiversity and Conservation

## Change Log
All notable changes to this project will be documented in this file.

## [0.0.1] - 2016-12-1
### FIXED
- Issue with merging channels in DJIx3 images
