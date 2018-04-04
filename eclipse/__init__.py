# Licensed under a 3-clause BSD style license - see LICENSE.rst

# Packages may add whatever they like to this file, but
# should keep this content at the top.
# ----------------------------------------------------------------------------
from ._sunpy_init import *
# ----------------------------------------------------------------------------

if not _ASTROPY_SETUP_:
    import os
    _package_directory = os.path.dirname(os.path.abspath(__file__))
    _data_directory = os.path.abspath(os.path.join(_package_directory, 'sample_photos'))
    SAMPLE_PHOTO = os.path.join(_data_directory, 'total_solar_eclipse2017.jpg')
