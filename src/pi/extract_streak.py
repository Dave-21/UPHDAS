"""
extract_streak.py
    - This provides functions to detect a satellite streak in an image
    - Sample evenly spaced points along the detected streak (RA/Dec & corresponding times).
    - The streak detection uses the Hough Transform to find lines in the image.
"""

import cv2
import numpy as np

# This is the main function that detects satellite arc (streak) in a frame
# It takes as parameters: Path to image, Minimum streak length (in pixels),
#   and border tolerance (in pixels) to filter false positives
# It returns a tuple (x1, y1, x2, y2) for the longest valid line or None if no valid streak is found
def detect_satellite_streak(image_path, min_length=50, border_tolerance=10):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print("Error: Could not load image for streak detection.")
        return None

    # Reduce noise and extract edges
    blurred = cv2.GaussianBlur(img, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150, apertureSize=3)

    # Use the Probabilistic Hough Transform to detect lines
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=50, minLineLength=min_length, maxLineGap=5)
    if lines is None:
        return None

    height, width = img.shape
    valid_lines = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        # Exclude lines that are too close to any border
        if ((x1 < border_tolerance and x2 < border_tolerance) or
            (y1 < border_tolerance and y2 < border_tolerance) or
            (x1 > width - border_tolerance and x2 > width - border_tolerance) or
            (y1 > height - border_tolerance and y2 > height - border_tolerance)):
            continue
        valid_lines.append((x1, y1, x2, y2))
    
    if not valid_lines:
        return None

    # Choose the longest line (assumed to be the satellite streak)
    longest_line = max(valid_lines, key=lambda l: np.hypot(l[2] - l[0], l[3] - l[1]))
    return longest_line

# This simulates x amount of points along streak segment and returns their tuples
def sample_line(line, num_points):
    x1, y1, x2, y2 = line
    points = []
    for i in range(num_points):
        t = i / (num_points - 1) if num_points > 1 else 0.5
        x = x1 + t * (x2 - x1)
        y = y1 + t * (y2 - y1)
        points.append((x, y))
    return points

if __name__ == "__main__":
    # this is a test we need to replace with valid test image
    test_image = "leo_test_img.png"
    streak = detect_satellite_streak(test_image)
    if streak:
        print("Detected streak:", streak)
        points = sample_line(streak, 5)
        print("Sampled points:", points)
    else:
        print("No valid streak detected.")
