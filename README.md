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
