import cv2
import numpy as np
import argparse
from pathlib import Path

"""
Script for syncing two videos in time and making these equally long.
Provide the paths to the videos and the name of the output video as arguments.

Press "1" to move forward in the first video, "2" for the second video, and enter to
initiate saving.
"""

path1 = Path.joinpath(
    Path(__file__).parents[0].resolve(), "videos_original/video1.mp4"
)
path2 = Path.joinpath(
    Path(__file__).parents[0].resolve(), "videos_original/video2.mp4" 
)
vidname = "syncedvideo"

cap1 = cv2.VideoCapture(str(path1))
nbr_frames1 = int(cap1.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
cap2 = cv2.VideoCapture(str(path2))
nbr_frames2 = int(cap2.get(cv2.CAP_PROP_FRAME_COUNT)) - 1

_, f1 = cap1.read()
_, f2 = cap2.read()
height, width, _ = f1.shape

# Find a starting point
while True:
    f = np.hstack((f1, f2))
    f = cv2.resize(f, (0, 0), fx=0.5, fy=0.5)
    cv2.imshow("", f)
    k = cv2.waitKey(0) & 0xFF
    if k == 49:  # 1 is pressed
        _, f1 = cap1.read()
        nbr_frames1 -= 1
    elif k == 50:  # 2 is pressed
        _, f2 = cap2.read()
        nbr_frames2 -= 1
    else:
        break

# Create and save two equally long clips
clip1 = cv2.VideoWriter(
    str(
        Path.joinpath(
            Path(__file__).parents[0].resolve(), "videos/" + vidname + "_1.mp4"
        )
    ),
    cv2.VideoWriter_fourcc(*"mp4v"),
    30.0,
    (width, height),
)
clip2 = cv2.VideoWriter(
    str(
        Path.joinpath(
            Path(__file__).parents[0].resolve(), "videos/" + vidname + "_2.mp4"
        )
    ),
    cv2.VideoWriter_fourcc(*"mp4v"),
    30.0,
    (width, height),
)

for _ in range(min([nbr_frames1, nbr_frames2])):
    _, f1 = cap1.read()
    _, f2 = cap2.read()
    clip1.write(f1)
    clip2.write(f2)
clip1.release()
clip2.release()
cap1.release()
cap2.release()
cv2.destroyAllWindows()