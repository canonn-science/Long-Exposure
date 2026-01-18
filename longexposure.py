import os
import cv2
import numpy as np
import glob
import shutil

# Supported video extensions
VIDEO_EXTENSIONS = [".mp4", ".avi", ".mov", ".mkv"]

# Directories
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
    acc = np.zeros_like(frame, dtype=np.float32)
    count = 0
    while ret:
        if count % 50 == 0:
            print(f"    Processing frame {count+1}...")
        acc += frame.astype(np.float32)
        count += 1
        ret, frame = cap.read()
    cap.release()
    if count == 0:
        print(f"  No frames processed in {video_path}")
        return
    print(f"  Averaging {count} frames...")
    avg = (acc / count).astype(np.uint8)
    base = os.path.splitext(os.path.basename(video_path))[0]
    out_path = os.path.join(EXPOSURES_DIR, base + ".png")
    cv2.imwrite(out_path, avg)
    print(f"  Saved long exposure image to {out_path}")
    # Move video to processed
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
