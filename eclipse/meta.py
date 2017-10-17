"""Procedures to gather meta data from the photograph"""
import exifread # to read information from the image
import astropy.wcs
import numpy as np
import scipy.ndimage as ndimage
from skimage.transform import hough_circle, hough_circle_peaks

import astropy.wcs
from astropy.coordinates import EarthLocation, SkyCoord
import astropy.units as u

import sunpy
import sunpy.map
import sunpy.coordinates

import exifread # to read information from the image


def _convert_to_degress(value):
    """
    Helper function to convert the GPS coordinates stored in the EXIF to degress in float format
    :param value:
    :type value: exifread.utils.Ratio
    :rtype: float
    """
    d = float(value.values[0].num) / float(value.values[0].den)
    m = float(value.values[1].num) / float(value.values[1].den)
    s = float(value.values[2].num) / float(value.values[2].den)

    return d + (m / 60.0) + (s / 3600.0)


def get_exif_location(exif_data):
    """
    Returns the latitude and longitude, if available, from the provided
    exif_data (obtained through get_exif_data above)
    """
    lat = None
    lon = None

    gps_latitude = exif_data.get('GPS GPSLatitude', None)
    gps_latitude_ref = exif_data.get('GPS GPSLatitudeRef', None)
    gps_longitude = exif_data.get('GPS GPSLongitude', None)
    gps_longitude_ref = exif_data.get('GPS GPSLongitudeRef', None)

    if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
        lat = _convert_to_degress(gps_latitude)
        if gps_latitude_ref.values[0] != 'N':
            lat = 0 - lat

        lon = _convert_to_degress(gps_longitude)
        if gps_longitude_ref.values[0] != 'E':
            lon = 0 - lon

    return lat, lon


def get_meta_from_exif(exif_data):
    """Gather meta header from the EXIF data."""

    if "EXIF ExposureTime" in tags:
        exposure_tag = tags['EXIF ExposureTime']
        exposure_time = exposure_tag.values[0].num / exposure_tag.values[
            0].den * u.s
    if "Image Artist" in tags:
        author_str = tags['Image Artist'].values
    if "EXIF DateTimeOriginal" in tags:
        datetime_str = tags['EXIF DateTimeOriginal'].values.replace(' ',
                                                                    ':').split(
            ':')
        time = datetime(int(datetime_str[0]), int(datetime_str[1]),
                        int(datetime_str[2]), int(datetime_str[3]),
                        int(datetime_str[4]), int(datetime_str[5]))
    if "Image Model" in tags:
        camera_model_str = tags['Image Model'].values
    lat, lon = get_exif_location(tags)
    if ((lat != None) and (lon != None)):
        gps = [lat, lon] * u.deg

    result = {}
    result.update({'AUTHOR': author_str})
    result.update({'EXPTIME': exposure_time.to('s').value})
    result.update({'TELECOP': camera_model_str})
    result.update({'LAT': gps[0]})
    result.update({'LON': gps[1]})
    result.update({'DATEOBS': time.isoformat()})
    return result


def find_sun_center(im):
    """Given an image which contains the Sun, find the circle of the Sun
    and return the position as well as the radius."""
    blur_im = ndimage.gaussian_filter(im, 8)
    mask = blur_im > blur_im.mean() * 3
    label_im, nb_labels = ndimage.label(mask)
    slice_x, slice_y = ndimage.find_objects(label_im == 1)[0]
    roi = blur_im[slice_x, slice_y]
    sx = ndimage.sobel(roi, axis=0, mode='constant')
    sy = ndimage.sobel(roi, axis=1, mode='constant')
    sob = np.hypot(sx, sy)
    hough_radii = np.arange(np.floor(np.mean(sob.shape) / 4),
                            np.ceil(np.mean(sob.shape) / 2), 10)
    hough_res = hough_circle(sob > (sob.mean() * 5), hough_radii)

    # Select the most prominent circle
    accums, cy, cx, radii = hough_circle_peaks(hough_res, hough_radii,
                                               total_num_peaks=1)
    im_cx = (cx + slice_x.start) * u.pix
    im_cy = (cy + slice_y.start) * u.pix
    im_radius = radii * u.pix

    return im_cx, im_cy, im_radius


def get_plate_scale(time, im_radius):
    dsun = sunpy.coordinates.get_sunearth_distance(time.isoformat())
    rsun_obs = np.arctan(sunpy.sun.constants.radius / dsun).to('arcsec')
    plate_scale = rsun_obs / im_radius
    return plate_scale


def build_wcs(im_cx, im_cy, plate_scale):

    w = astropy.wcs.WCS(naxis=2)
    w.wcs.crpix = [im_cy[0].value, im_cx[0].value]
    w.wcs.cdelt = np.ones(2) * plate_scale.to('arcsec/pix').value
    w.wcs.crval = [0, 0]
    w.wcs.ctype = ['TAN', 'TAN']
    w.wcs.cunit = ['arcsec', 'arcsec']
    return w


def build_meta(wcs, exif_data):
    wcs.wcs.dateobs = time.isoformat()
    header = dict(wcs.wcs.to_header())

    dsun = sunpy.coordinates.get_sunearth_distance(time.isoformat())
    lat = exif_data.get('lat')
    lon = exif_data.get('lon')
    time = exif_data.get('DATEOBS')
    solar_rotation_angle = get_solar_rotation_angle(lat, lon, time)
    header = dict(w.to_header())
    header.update({'CROTA2': solar_rotation_angle.to('deg').value})
    header.update({'DSUN_OBS': dsun.to('m').value})
    header.update({'HGLN_OBS': hgln_obs.to('deg').value})
    header.update({'HGLT_OBS': hglt_obs.to('deg').value})
    header.update({'CTYPE1': 'HPLN-TAN'})
    header.update({'CTYPE2': 'HPLT-TAN'})
    header.update({'RSUN': dsun.to('m').value})
    header.update({'RSUN_OBS': np.arctan(sunpy.sun.constants.radius / dsun).to(
        'arcsec').value})
    return header


def get_solar_rotation_angle(lat, lon, time, fudge_angle=0):
    """Get the solar rotation angle"""
    loc = EarthLocation(lat=gps[0], lon=gps[1])
    solar_rotation_angle = sunpy.coordinates.get_sun_orientation(loc, time)
    return solar_rotation_angle + fudge_angle

