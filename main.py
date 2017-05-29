import os
import tracker

# Define Hotspots
hotspot1 = tracker.Hotspot((0, 0), (150, 150), os.getcwd() + "/test.mkv")

colour_tracker = tracker.Tracker(hotspots=[hotspot1])
colour_tracker.start()
