# DS9RegionSaver

A Python script to automate the process of saving regions from DS9 images, with custom scaling, zooming, and labeling options.

## Features

- Load multiple FITS files in different colors.
- Apply custom scaling parameters for each FITS file.
- Zoom and pan to specific regions based on RA and Dec.
- Label images with source names from a specified file.
- Save images with custom filenames.

## Requirements

- Python 3.x
- DS9
- XPA (X Public Access)

## Installation

1. Install DS9 and XPA:
   - **macOS**: `brew install saods9 xpa`
   - **Linux**: Follow the instructions on the [DS9 website](https://sites.google.com/cfa.harvard.edu/saoimageds9)
   - **Windows**: Use the [Windows Subsystem for Linux (WSL)](https://docs.microsoft.com/en-us/windows/wsl/install)

2. Clone this repository:
   ```bash
   git clone https://github.com/your-username/DS9RegionSaver.git
   cd DS9RegionSaver


# Usage

1. Prepare the source file (`pan_zoom.txt`) with the following format:
   ```text
   RA Dec Radius
   56.67657665 68.160590675005 2.6687305341091236
   56.68005265 68.036525675005 3.1234567890123456
   ...
2. Prepare the name file (`name.txt`) with the following format:
   ```text
   Name RA Dec
   034642.35+680938.2 56.67657665 68.160590675005
   034643.19+680211.6 56.68005265 68.036525675005
   ...

3. Update the file paths in the script.
   
   For example:
   ```bash
   fits_files = [
    '/path/to/f606w_drc.fits',
    '/path/to/f435w_drc.fits'
   ]
   colors = ['green', 'blue']  # Colors for the FITS files
   scaling_params = [
       {'scaling': 'log', 'scale_min': 0, 'scale_max': 1.6e6, 'contrast': 3.3, 'bias': 0.25},
       {'scaling': 'log', 'scale_min': 0, 'scale_max': 740000, 'contrast': 6.6, 'bias': 0.12}
   ]
   region_files = [
       '/path/to/xray99_hst.reg',
       '/path/to/X_ray99_final_123sig.reg'
   ]
   source_file = '/path/to/pan_zoom.txt'
   name_file = '/path/to/name.txt'
   output_dir = 'images/'

4. Run the script:
   ```bash
   python ds9_region_saver.py
