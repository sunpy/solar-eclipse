# -*- coding: utf-8 -*-
# Author: Steven Christe
# License: 3-clause BSD
"""
AIA Plot Example
================

This is a very simple way to plot a sample AIA image.
asdfasdfasd
asdf
asdf
asdf
asdf
asd
fads
"""
from __future__ import print_function, division

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from eclipse import SAMPLE_PHOTO
###############################################################################
# read in the image and flip it so that it's correct
im_rgb = np.flipud(matplotlib.image.imread(SAMPLE_PHOTO))
# remove color info
im = np.average(im_rgb, axis=2)
plt.imshow(im, origin='lower')
plt.show()
