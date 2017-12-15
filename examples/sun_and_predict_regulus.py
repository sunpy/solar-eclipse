# -*- coding: utf-8 -*-
# Author: Steven Christe
# License: 3-clause BSD
"""
Photo to SunPy Map
==================

This shows how to overplot a predicted location of Regulus on your eclipse
photo.
"""
import matplotlib.pyplot as plt
import astropy.units as u
from astropy.coordinates import SkyCoord

from eclipse.process import eclipse_image_to_map
from eclipse import SAMPLE_PHOTO

###############################################################################
# Create the eclipse map
m = eclipse_image_to_map(SAMPLE_PHOTO)

###############################################################################
# Using the RA and DEC for Regulus we can create a coordinate object for it.
regulus = SkyCoord(
    ra='10h08m22.311s',
    dec='11d58m01.95s',
    distance=79.3 * u.lightyear,
    frame='icrs').transform_to(m.coordinate_frame)

###############################################################################
# Now plot the map with Regulus overlaid
fig = plt.figure(figsize=(9, 9))
ax = plt.subplot(projection=m)
m.plot(axes=ax)
ax.plot_coord(regulus, '*w', label='Regulus')
m.draw_grid(axes=ax)
m.draw_limb(axes=ax)
plt.legend()
plt.show()
