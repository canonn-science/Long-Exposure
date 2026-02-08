# Image Output Examples

When you process a video, the script creates several images that visualize different aspects of the video frames. Here are sample outputs and what they mean:

## 1. Average Image (`*_avg.png`)
- **Example:** `samples/Dryio Flyuae NC-V d2-1255_avg.png`
- **Description:** This image shows the average brightness and color of each pixel across all frames. It looks like a long exposure photo, blending all movement and light together.

## 2. Maximum Image (`*_max.png`)
- **Example:** `samples/Dryio Flyuae NC-V d2-1255_max.png`
- **Description:** Each pixel is set to the brightest value it reached in any frame. This highlights areas that were illuminated or changed the most during the video.

## 3. Minimum Image (`*_min.png`)
- **Example:** `samples/Dryio Flyuae NC-V d2-1255_min.png`
- **Description:** Each pixel is set to the darkest value it reached in any frame. This shows the parts of the scene that stayed dark throughout the video.

## 4. Max Minus Min Image (`*_max_minus_min.png`)
- **Example:** `samples/Dryio Flyuae NC-V d2-1255_max_minus_min.png`
- **Description:** This image shows the difference between the brightest and darkest values for each pixel. It highlights areas with the most change or movement.

## 5. Motion Variance Image (`*_motion_variance.png`)
- **Example:** `samples/Dryio Flyuae NC-V d2-1255_motion_variance.png`
- **Description:** This colorized image visualizes how much each pixel changed over time. Black means no change; colored areas show where motion or variation occurred. The more a pixel changed, the brighter and more colorful it appears.

---

These images help you see both the static and dynamic parts of your video in a single glance, using simple visual summaries.
