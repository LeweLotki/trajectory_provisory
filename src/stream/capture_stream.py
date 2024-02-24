import cv2
import os
from shutil import rmtree
from config import paths
import numpy as np

class Stream:

    frame_count = 0
    output_dir = paths.stream_frames_path
    left_dir = os.path.join(output_dir, 'L')
    right_dir = os.path.join(output_dir, 'R')

    def __init__(self, stream_mode=False):

        self.stream_mode = stream_mode
        self.cap = cv2.VideoCapture(0)

    def run(self):

        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    break 
                else:
                    self.frame_count += 1

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        finally:
            self.cap.release()
            cv2.destroyAllWindows()


    def __create_output_dir(self):
       
        if os.path.exists(self.output_dir):
            rmtree(self.output_dir)
           
        os.makedirs(self.left_dir)
        os.makedirs(self.right_dir)

    def __subdivide_camera_image(self, frame : np.ndarray) -> list:

        height, width = frame.shape[:2]
        mid_point = width // 2
        return [
                   frame[:, :mid_point],
                   frame[:, mid_point:]
               ]

    def __display_images(self, frame : np.ndarray):

        (
            left_image,
            right_image
        ) = self.__subdivide_camera_image(frame)                

        cv2.imshow('Left Image', left_image)
        cv2.imshow('Right Image', right_image)

    def __save_images(self, frame : np.ndarray):

        left_path = os.path.join(left_dir, f'{frame_count}.png')
        right_path = os.path.join(right_dir, f'{frame_count}.png')
        cv2.imwrite(left_path, left_image)
        cv2.imwrite(right_path, right_image)


