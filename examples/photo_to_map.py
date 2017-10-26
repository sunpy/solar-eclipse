# -*- coding: utf-8 -*-
# Author: Steven Christe
# License: 3-clause BSD
"""
Photo to SunPy Map
==================

This examples shows how to convert an eclipse photograph to a coordinate-aware
SunPy map.
"""
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

import sunpy.map

from eclipse import SAMPLE_PHOTO
from eclipse.process import find_center_and_radius
import eclipse.meta as m
import exifread

###############################################################################
# read in the image and flip it so that it's correct, also remove the color
im_rgb = np.flipud(matplotlib.image.imread(SAMPLE_PHOTO))
im = np.average(im_rgb, axis=2)
###############################################################################
# next fit a circle to the Sun
im_cx, im_cy, im_radius = find_center_and_radius(im)

###############################################################################
# Next get some metadata from the photo. First grab the EXIF data
tags = exifread.process_file(open(SAMPLE_PHOTO, 'rb'))
###############################################################################
# Next get the exact time the photo was taken.
time = m.get_image_time(tags)

###############################################################################
# With the time and the radius of the solar disk we can calculate the plate
# scale.
plate_scale = m.get_plate_scale(time, im_radius)

###############################################################################
# We can now build a WCS object and a meta dictionary. We then append a few
# more meta tags to the meta dictionary.
wcs = m.build_wcs(im_cx, im_cy, plate_scale)
meta = m.build_meta(wcs, tags)

###############################################################################
# With the image as well as the meta data we can now create the SunPy Map
m = sunpy.map.Map((im, meta))

###############################################################################
# Now plot the map
fig = plt.figure(figsize=(10,10))
ax = plt.subplot(projection=m)
m.plot(axes=ax)
m.draw_grid(axes=ax)
m.draw_limb(axes=ax)
plt.show()