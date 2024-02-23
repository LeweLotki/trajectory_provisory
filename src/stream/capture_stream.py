import cv2
import os
from shutil import rmtree

# Create output directories if they don't exist
output_dir = 'output'
left_dir = os.path.join(output_dir, 'L')
right_dir = os.path.join(output_dir, 'R')

if os.path.exists(output_dir):
    rmtree(output_dir)
   
os.makedirs(left_dir)
os.makedirs(right_dir)

# Initialize a variable to keep track of frame count
frame_count = 0

# Capture frames from the camera
cap = cv2.VideoCapture(0)  # Adjust the device index if necessary

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break  # Exit loop if no frame is captured

        # Assuming the left and right images are side-by-side, split the frame in half
        height, width = frame.shape[:2]
        mid_point = width // 2
        left_image = frame[:, :mid_point]
        right_image = frame[:, mid_point:]

        # Display the split frames (optional, for testing)
        cv2.imshow('Left Image', left_image)
        cv2.imshow('Right Image', right_image)

        # Save frames to their respective directories
        left_path = os.path.join(left_dir, f'{frame_count}.png')
        right_path = os.path.join(right_dir, f'{frame_count}.png')
        cv2.imwrite(left_path, left_image)
        cv2.imwrite(right_path, right_image)

        frame_count += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
            print(f"Stream finished. Frames saved to '{output_dir}' directory.")
            break
finally:
    cap.release()
    cv2.destroyAllWindows()


