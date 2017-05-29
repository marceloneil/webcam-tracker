import cv2 as cv
import numpy as np
import time


class Tracker:
    """Video tracker"""

    def __init__(self, src=0, windows=["preview"], hotspots=[]):
        self.video = cv.VideoCapture(src)
        self.height = self.video.get(cv.CAP_PROP_FRAME_HEIGHT)
        self.width = self.video.get(cv.CAP_PROP_FRAME_WIDTH)
        self.windows = windows
        self.hotspots = hotspots
        self.time = 0

        for window in self.windows:
            cv.namedWindow("preview")

    def start(self):
        cv.setMouseCallback(self.windows[0], self.on_click)
        if self.video.isOpened():  # try to get the first frame
            rval, frame = self.video.read()
            frame = cv.flip(frame, 1)
        else:
            rval = False

        while rval:
            if hasattr(self, 'colour'):
                point = self.closest_point(self.colour, frame)
                frame = cv.circle(frame, point, 20, (0, 255, 0), thickness=10)
                if time.time() - self.time > 5:
                    for hotspot in self.hotspots:
                        if hotspot.check(point):
                            self.play_video(hotspot.filename)
                            # Hack to keep the video from playing instantly
                            self.time = time.time()
            for window in self.windows:
                cv.imshow(window, frame)
            rval, frame = self.video.read()
            frame = cv.flip(frame, 1)
            key = cv.waitKey(20)
            if key == 27:  # exit on ESC
                self.stop()
                break

    def stop(self):
        for window in self.windows:
            cv.destroyWindow(window)

    def play_video(self, filename):
        video = cv.VideoCapture(filename)

        if video.isOpened():
            rval, frame = video.read()
        else:
            rval = False

        while rval:
            cv.imshow(self.windows[0], frame)
            rval, frame = video.read()

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
