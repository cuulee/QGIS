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

### [1.0.1] - 2016-12-13
#### ADDED
- Legacy support for Survey1 camera models in Calibrate tab.

### [1.0.0] - 2016-12-13
#### ADDED
- MacOS X is now supported

#### Fixed
- Plugin now warns when trying to overwrite tiffs created when preprocessing DNG images instead of throwing an exception.

### [0.0.3] - 2016-12-6
#### Fixed
- Tiffs now properly convert to Jpegs when checking the "Convert calibrated tiffs to jpgs" box

#### TO DO
- Found issues when trying to install plugin on Mac OSX. Working on a solution.

### [0.0.2] - 2016-12-2
#### ADDED
- Now stores previously selected filepaths to make navigation easier

#### Changed
- Cleaned up UI layout

#### FIXED
- Missing default calibration for DKI camera models
- QR calibration percentage values

### [0.0.1] - 2016-12-1
#### FIXED
- Issue with merging channels in DJIx3 images
