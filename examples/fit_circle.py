# -*- coding: utf-8 -*-
# Author: Steven Christe
# License: 3-clause BSD
"""
Eclipse Photo Plot
==================

This is a very simple way to to fit a circle of the Sun to your eclipse photograph.
"""
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import numpy as np

from eclipse import SAMPLE_PHOTO
from eclipse.process import find_sun_center_and_radius
###############################################################################
# read in the image and flip it so that it's correct, also remove the color
im_rgb = np.flipud(matplotlib.image.imread(SAMPLE_PHOTO))
im = np.average(im_rgb, axis=2)
###############################################################################
# next fit a circle to the Sun
im_cx, im_cy, im_radius = find_sun_center_and_radius(im)

###############################################################################
# Show the result on a plot
fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(10, 4))
circ = Circle([im_cy.value, im_cx.value], radius=im_radius.value,
              facecolor='none', edgecolor='red', linewidth=2)
ax.imshow(im)
ax.add_patch(circ)
plt.show()