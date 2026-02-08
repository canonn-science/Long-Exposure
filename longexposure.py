import os
import sys
import cv2
import numpy as np
import glob
import shutil

# Supported video extensions
VIDEO_EXTENSIONS = [".mp4", ".avi", ".mov", ".mkv"]


# Directories
if getattr(sys, "frozen", False):
    # Running as a bundled executable
    CURRENT_DIR = os.path.dirname(sys.executable)
else:
    # Running from source
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
EXPOSURES_DIR = os.path.join(CURRENT_DIR, "exposures")
PROCESSED_DIR = os.path.join(CURRENT_DIR, "processed")

os.makedirs(EXPOSURES_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)


def is_video_file(filename):
    return any(filename.lower().endswith(ext) for ext in VIDEO_EXTENSIONS)


def process_video(video_path):
    print(f"Processing video: {os.path.basename(video_path)}")
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"  Failed to open {video_path}")
        return
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"  Frame count: {frame_count}")
    ret, frame = cap.read()
    if not ret:
        print(f"  No frames in {video_path}")
        cap.release()
        return
    max_frame = frame.astype(np.uint8)
    min_frame = frame.astype(np.uint8)
    sum_frame = frame.astype(np.float64)
    count = 1
    prev_frame = frame.astype(np.uint8)
    pixel_changes = np.zeros(frame.shape[:2], dtype=np.uint16)
    # For motion variance
    motion_sum = np.zeros(frame.shape[:2], dtype=np.float64)
    motion_sq_sum = np.zeros(frame.shape[:2], dtype=np.float64)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if count % 50 == 0:
            print(f"    Processing frame {count+1}...")
        frame_uint8 = frame.astype(np.uint8)
        max_frame = np.maximum(max_frame, frame_uint8)
        min_frame = np.minimum(min_frame, frame_uint8)
        sum_frame += frame_uint8
        # For heatmap: count pixel changes (any channel)
        changed = np.any(frame_uint8 != prev_frame, axis=2)
        pixel_changes[changed] += 1
        # Motion variance: compute grayscale diff
        diff = cv2.absdiff(
            cv2.cvtColor(frame_uint8, cv2.COLOR_BGR2GRAY),
            cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY),
        ).astype(np.float64)
        motion_sum += diff
        motion_sq_sum += diff**2
        prev_frame = frame_uint8
        count += 1
    cap.release()
    if count == 0:
        print(f"  No frames processed in {video_path}")
        return
    print(f"  Composited {count} frames using max, min, and average brightness...")
    base = os.path.splitext(os.path.basename(video_path))[0]
    out_path_max = os.path.join(EXPOSURES_DIR, base + "_max.png")
    out_path_min = os.path.join(EXPOSURES_DIR, base + "_min.png")
    out_path_avg = os.path.join(EXPOSURES_DIR, base + "_avg.png")
    avg_frame = (sum_frame / count).astype(np.uint8)
    cv2.imwrite(out_path_max, max_frame)
    cv2.imwrite(out_path_min, min_frame)
    cv2.imwrite(out_path_avg, avg_frame)

    # Motion variance image
    print("  Generating motion variance image...")
    n_motion = count - 1 if count > 1 else 1
    mean_motion = motion_sum / n_motion
    mean_sq_motion = motion_sq_sum / n_motion
    variance = mean_sq_motion - mean_motion**2
    # Normalize for visualization: set min to 0, max to 255, so unchanging areas are black
    min_var = variance.min()
    max_var = variance.max()
    # Normalize so min is 0, max is 255 for full contrast
    if max_var > min_var:
        variance_norm = np.clip(
            (variance - min_var) / (max_var - min_var) * 255, 0, 255
        ).astype(np.uint8)
    else:
        variance_norm = np.zeros_like(variance, dtype=np.uint8)
    # Colorize: keep black as black, colorize only nonzero values
    colorized = cv2.applyColorMap(variance_norm, cv2.COLORMAP_JET)
    mask = (variance_norm == 0)
    colorized[mask] = [0, 0, 0]  # Set zero-variance pixels to black
    out_path_var = os.path.join(EXPOSURES_DIR, base + "_motion_variance.png")
    cv2.imwrite(out_path_var, colorized)
    print(f"  Saved motion variance (colorized, black stays black) image to {out_path_var}")

    # Max minus min image (moving areas only)
    print("  Generating max-minus-min image...")
    max_minus_min = cv2.absdiff(max_frame, min_frame)
    # Normalize to 0-255 for each channel
    max_val = max_minus_min.max()
    if max_val > 0:
        max_minus_min_norm = (max_minus_min.astype(np.float32) / max_val * 255).astype(
            np.uint8
        )
    else:
        max_minus_min_norm = max_minus_min
    out_path_maxmin = os.path.join(EXPOSURES_DIR, base + "_max_minus_min.png")
    cv2.imwrite(out_path_maxmin, max_minus_min_norm)
    print(f"  Saved max-minus-min image to {out_path_maxmin}")

    print(
        f"  Saved max, min, average, heatmap, motion variance, and max-minus-min images to exposures/"
    )
    shutil.move(video_path, os.path.join(PROCESSED_DIR, os.path.basename(video_path)))
    print(f"  Moved {video_path} to processed/\n")


def main():
    print("Starting long exposure processing...")
    found = False
    for filename in os.listdir(CURRENT_DIR):
        if is_video_file(filename):
            found = True
            process_video(os.path.join(CURRENT_DIR, filename))
    if not found:
        print("No video files found in the current directory.")


if __name__ == "__main__":
    main()
