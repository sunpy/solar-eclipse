# -*- coding: utf-8 -*-
# Author: Steven Christe
# License: 3-clause BSD
"""
Photo to SunPy Map
==================

This examples shows how to convert an eclipse photograph to a coordinate-aware
SunPy map.
"""
import matplotlib.pyplot as plt

from eclipse.process import EclipseMap
from eclipse import SAMPLE_PHOTO

###############################################################################
# With the image as well as the meta data we can now create the SunPy Map
m = EclipseMap(SAMPLE_PHOTO)

###############################################################################
# Now plot the map
fig = plt.figure(figsize=(10,10))
ax = plt.subplot(projection=m)
m.plot(axes=ax)
m.draw_grid(axes=ax)
m.draw_limb(axes=ax)
plt.show()


