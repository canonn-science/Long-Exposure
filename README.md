# Long Exposure Video Frame Averager

This project processes video files by averaging their frames to create a long exposure effect image. It supports common video formats and automatically organizes processed files.

## Features
- Supports .mp4, .avi, .mov, .mkv video files
- Averages all frames in a video to produce a single PNG image
- Moves processed videos to a `processed/` directory
- Saves output images to an `exposures/` directory
- Automatically creates required directories if they do not exist

## Usage

1. Place your video files in the project directory.
2. Run the script:
   ```bash
   python longexposure.py
   ```
3. Find the resulting PNG images in the `exposures/` folder. Processed videos are moved to `processed/`.

## Build Windows EXE
A GitHub Actions workflow is provided to build a standalone Windows executable using PyInstaller. The EXE can be downloaded from the GitHub Actions artifacts after a successful run.

## Requirements
- Python 3.8+
- opencv-python
- numpy

Install dependencies with:
```bash
pip install opencv-python numpy
```

## License
MIT License. See LICENSE file for details.
