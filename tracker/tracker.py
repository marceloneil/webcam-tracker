import cv2 as cv
import numpy as np


class Tracker:
    """Video tracker"""

    def __init__(self, webcam_index, hotspots=[]):
        self.video = cv.VideoCapture(webcam_index)
        self.height = self.video.get(cv.CAP_PROP_FRAME_HEIGHT)
        self.width = self.video.get(cv.CAP_PROP_FRAME_WIDTH)
        self.hotspots = hotspots

    def start(self, window):
        cv.setMouseCallback(window, self.on_click)
        if self.video.isOpened():  # try to get the first frame
            rval, frame = self.video.read()
        else:
            rval = False

        while rval:
            if hasattr(self, 'colour'):
                point = self.closest_point(self.colour, frame)
                colour = (0, 255, 0)
                for hotspot in self.hotspots:
                    if hotspot.check(point):
                        colour = (255, 0, 0)
                frame = cv.circle(frame, point, 20, colour, thickness=10)
            cv.imshow(window, frame)
            rval, frame = self.video.read()
            frame = cv.flip(frame, 1)
            key = cv.waitKey(20)
            if key == 27:  # exit on ESC
                break

    def on_click(self, event, x, y, flags, param):
        if event == cv.EVENT_LBUTTONDOWN:
            rval, frame = self.video.read()
            x = int(self.width - x)
            self.colour = tuple(map(int, frame[y][x]))

    def closest_point(self, colour, frame):
        dists = np.sum((frame - colour)**2, axis=2)  # Get Euclidean distances
        minimum = dists.argmin()  # Return 1-D index of point that is closest
        x = int(minimum % self.width)
        y = int(minimum // self.width)
        return (x, y)
