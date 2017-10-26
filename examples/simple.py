# -*- coding: utf-8 -*-
# Author: Steven Christe
# License: 3-clause BSD
"""
Eclipse Photo Plot
==================

This is a very simple way to plot your eclipse photograph.
"""
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from eclipse import SAMPLE_PHOTO
###############################################################################
# read in the image and flip it so that it's correct
im_rgb = np.flipud(matplotlib.image.imread(SAMPLE_PHOTO))
###############################################################################
# remove color info and plot it
im = np.average(im_rgb, axis=2)
plt.imshow(im, origin='lower')
plt.show()
