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


## Output Examples

Below are sample images generated from a video, with explanations:

### Average Image (long exposure effect)
![Average](samples/Dryio%20Flyuae%20NC-V%20d2-1255_avg.png)
Shows the average brightness and color of each pixel across all frames. Looks like a long exposure photo.

### Maximum Image (brightest pixels)
![Maximum](samples/Dryio%20Flyuae%20NC-V%20d2-1255_max.png)
Each pixel is set to the brightest value it reached in any frame.

### Minimum Image (darkest pixels)
![Minimum](samples/Dryio%20Flyuae%20NC-V%20d2-1255_min.png)
Each pixel is set to the darkest value it reached in any frame.

### Max Minus Min Image (areas of change)
![Max Minus Min](samples/Dryio%20Flyuae%20NC-V%20d2-1255_max_minus_min.png)
Shows the difference between the brightest and darkest values for each pixel, highlighting areas with the most change.

### Motion Variance Image (colorized motion map)
![Motion Variance](samples/Dryio%20Flyuae%20NC-V%20d2-1255_motion_variance.png)
Visualizes how much each pixel changed over time. Black means no change; colored areas show motion or variation.

These examples help you understand what each image represents in simple terms.

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
