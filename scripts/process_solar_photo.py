import astropy.units as u
from astropy.coordinates import EarthLocation
import matplotlib.image
import astropy.wcs
import sunpy.map
import numpy as np
import matplotlib.pyplot as plt
import sunpy.coordinates
import sunpy.time
import sunpy.sun
from sunpy.net import hek
from astropy.coordinates import SkyCoord
from datetime import timedelta

f = '../sample-photos/Sun_with_one_AR.jpg'


def get_timestamp(filename):
    """
    Read the EXIF information and get the time at which the image was
    taken

    Returns
    =======
    time : datetime
    """
    time_str = '2017-07-16 14:34'
    return sunpy.time.parse_time(time_str)


def get_gps_coordinates(filename):
    """
    Read the EXIF information and get the GPS coordination where the image
    was taken.

    Returns
    =======
    location : astropy.Quantity
    """

    result = [38.885294, -77.001745] * u.deg
    return result


def get_sun_center(filename):
    """
    Process the image to find the center of the Sun.

    Returns
    =======
    pixel_coords : astropy.Quantity
    """
    return ([468, 734] * u.pix)


def get_plate_scale(filename, sun_center):
    """
    Find the plate scale of the image by finding the size of the Sun.

    Returns
    =======
    plate_scale : astropy.Quantity
    """
    return (0.5 * u.deg / (800 * u.pix))


# image meta data
time = get_timestamp(f)
latlon = get_gps_coordinates(f)
sun_center = get_sun_center(f)
plate_scale = get_plate_scale(f, sun_center)

w = astropy.wcs.WCS(naxis=2)
w.wcs.crpix = [2944, 1955] * u.pixel
w.wcs.cdelt = np.ones(2) * plate_scale.to('arcsec/pix').value
w.wcs.crval = [0, 0]
w.wcs.ctype = ['TAN', 'TAN']
w.wcs.cunit = ['arcsec', 'arcsec']
w.wcs.dateobs = time.isoformat()
header = dict(w.to_header())

gps = EarthLocation(lat=latlon[0], lon=latlon[1])
solar_rotation_angle = sunpy.coordinates.get_sun_orientation(gps, time)
dsun = sunpy.coordinates.get_sunearth_distance(time.isoformat())

header.update({'CROTA2': solar_rotation_angle.to('deg').value})
header.update({'DSUN_OBS': dsun.to('m').value})
header.update({'HGLN_OBS': sunpy.coordinates.get_sun_L0(time).to('deg').value})
header.update({'HGLT_OBS': sunpy.coordinates.get_sun_B0(time).to('deg').value})
header.update({'CTYPE1': 'HPLN-TAN'})
header.update({'CTYPE2': 'HPLT-TAN'})
header.update({'RSUN': dsun.to('m').value})
header.update({'TELESCOP': 'CANON 70D'})
header.update({
    'RSUN_OBS':
    np.arctan(sunpy.sun.constants.radius / dsun).to('arcsec').value
})
print(header)

# read in the image
im_rgb = matplotlib.image.imread(f)
# remove color info
im = np.average(im_rgb, axis=2)

m = sunpy.map.Map((im, header))

# get the location of Active regions from the HEK.
hek_client = hek.HEKClient()
tr = sunpy.time.TimeRange(time, timedelta(days=1))
responses = hek_client.query(hek.attrs.Time(tr.start, tr.end), hek.attrs.AR)

fig = plt.figure()
ax = plt.subplot(projection=m)
m.plot(axes=ax)
coord = SkyCoord(0 * u.arcsec, 0 * u.arcsec, frame=m.coordinate_frame)
ax.plot_coord(coord, color='b')
m.draw_grid(axes=ax)
m.draw_limb(axes=ax)
for resp in responses:
    coord = SkyCoord(
        resp['hpc_x'] * u.arcsec,
        resp['hpc_y'] * u.arcsec,
        frame=m.coordinate_frame)
    print(coord)
    ax.plot_coord(coord, color='b')
plt.savefig('solar_photo_map.pdf', dpi=300)

# now make a submap with a zoom in of the Sun
top_right = SkyCoord(950 * u.arcsec, 950 * u.arcsec, frame=m.coordinate_frame)
bottom_left = SkyCoord(
    -900 * u.arcsec, -900 * u.arcsec, frame=m.coordinate_frame)
m_submap = m.submap(bottom_left, top_right)

fig = plt.figure()
ax = plt.subplot(projection=m_submap)
m_submap.plot(axes=ax)
m_submap.draw_grid()
m_submap.draw_limb()
for resp in responses:
    plt.scatter(resp['hpc_x'] * u.arcsec, resp['hpc_y'] * u.arcsec)
    coord = SkyCoord(
        resp['hpc_x'] * u.arcsec,
        resp['hpc_y'] * u.arcsec,
        frame=m_submap.coordinate_frame)
    ax.plot_coord(coord, color='c')
    print(resp['hpc_x'])
plt.savefig('solar_photo_smap.pdf', dpi=300)
