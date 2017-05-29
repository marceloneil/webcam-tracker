import cv2 as cv
import tracker

# Define Hotspots
hotspot1 = tracker.Hotspot((0, 0), (150, 150))

colour_tracker = tracker.Tracker(0, hotspots=[hotspot1])

cv.namedWindow("preview")
colour_tracker.start("preview")
cv.destroyWindow("preview")
