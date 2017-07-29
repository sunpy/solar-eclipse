"""
Implementation of the SEISS algorithm of Krista & McIntosh 2015,
Solar Physics, Volume 290, Issue 8, pp.2381-2391

DOI: 10.1007/s11207-015-0757-1

"""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from skimage.filters import sobel
from skimage.transform import hough_circle, hough_circle_peaks
from skimage.draw import circle_perimeter

import cv2

img
img = cv2.medianBlur(img,5)
cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT,1,20,
                            param1=50,param2=30,minRadius=0,maxRadius=0)

circles = np.uint16(np.around(circles))
for i in circles[0,:]:
    # draw the outer circle
    cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

cv2.imshow('detected circles',cimg)

f = '/Users/ireland/Desktop/A05-103002w.JPG'

# Read in the file
im_rgb = matplotlib.image.imread(f)
im = np.mean(im_rgb, axis=2)


img = cv2.imread(f, 0)

# Convert to greyscale


# Step 1 - Decide if the image is a non-eclipse image

##############################################################################
# Step 2 - fit circles


# Apply the edge enhancement
im_edge = sobel(im)

# Assume that the whole disk of the Sun is in the image.  Therefore the radius
# is at most half the minimum dimensional size of the original image
im_size = im.shape
max_radius = np.min(im_size) // 2
min_radius = 50

try_radii = np.arange(min_radius, max_radius)

hspaces = hough_circle(im_edge, try_radii)

accum, cx, cy, rad = hough_circle_peaks(hspaces, try_radii, total_num_peaks=5, min_xdistance=10, min_ydistance=10)

for center_y, center_x, radius in zip(cy, cx, rad):
    circy, circx = circle_perimeter(np.int(center_y), np.int(center_x), np.int(radius))
    im_edge[circy, circx] = 100

plt.ion()
plt.imshow(im_edge)
