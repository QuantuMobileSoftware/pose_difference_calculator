import numpy as np
import cv2
import math
from cv2 import error as cv2error


# exception class for catching OpenCV exception
class ShapeError(Exception):
    pass


# input video stream from camera
capture = cv2.VideoCapture(0)

# params for ShiTomasi corner detection
feature_params = dict(maxCorners=100,
                      qualityLevel=0.3,
                      minDistance=7,
                      blockSize=7)

# Parameters for lucas kanade optical flow
lk_params = dict(winSize=(15, 15),
                 maxLevel=2,
                 criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

# Create some random colors
color = np.random.randint(0, 255, (100, 3))

# here we take first frame
# first frame means that it's our stable pose
ret, old_frame = capture.read()

# than we continue with grayscale image
old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)

# here we choosing feature to track with Lucas Kanade algorithm
p0 = cv2.goodFeaturesToTrack(old_gray, mask=None, **feature_params)

# Create a mask image for drawing purposes
mask = np.zeros_like(old_frame)

# here we continue to operate with video stream
while capture.isOpened():

    _, frame = capture.read()
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # calculate optical flow
    p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

    # Select good points
    good_new = p1[st == 1]
    good_old = p0[st == 1]

    # calculating essential matrix with RANSAC
    esentMat, _ = cv2.findEssentialMat(good_new, good_old)

    # recovering pose from essential matrix and two set of images
    # if number of points less than 5 recovering exception
    # (less than 5 because it's "5 points algorithm")
    try:
        m, r, t, h = cv2.recoverPose(esentMat, good_new, good_old)
    except cv2error:
        raise ShapeError

    # extracting from rotating matrix real rotates
    rotVec, _ = cv2.Rodrigues(r)

    # printing our results
    # as our rotate storages in radians we need to transform it to degreeses
    print rotVec * 180.0 / math.pi
    print t
    print '\n'

    # draw the tracks
    for i, (new, old) in enumerate(zip(good_new, good_old)):
        a, b = new.ravel()
        c, d = old.ravel()
        mask = cv2.line(mask, (a, b), (c, d), color[i].tolist(), 2)
        frame = cv2.circle(frame, (a, b), 5, color[i].tolist(), -1)

    # show an image
    img = cv2.add(frame, mask)
    cv2.imshow('frame', img)

    # if press ESC - exit
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

    # reinit of our features for the next frame
    old_gray = frame_gray.copy()
    p0 = good_new.reshape(-1, 1, 2)

# closing all windows, which were used in app
cv2.destroyAllWindows()
capture.release()