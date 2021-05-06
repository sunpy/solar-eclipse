"""Procedures to gather meta data from a photograph."""
import astropy.wcs
import numpy as np

import astropy.wcs
from astropy.coordinates import EarthLocation, SkyCoord
import astropy.units as u
from datetime import datetime

import sunpy
import sunpy.map
import sunpy.coordinates
from sunpy.util import MetaDict

import exifread # to read information from the image

__all__ = ['get_exif_location', 'get_meta_from_exif']


def _convert_to_degress(value):
    """
    Helper function to convert the GPS coordinates stored in the EXIF to
    degress in float format
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


def get_image_time(exif_data):
    """Get the time from the photograph."""
    if "EXIF DateTimeOriginal" in exif_data:
        datetime_str = exif_data['EXIF DateTimeOriginal'].values.replace(' ',
                                                                    ':').split(
            ':')
        time = datetime(int(datetime_str[0]), int(datetime_str[1]),
                        int(datetime_str[2]), int(datetime_str[3]),
                        int(datetime_str[4]), int(datetime_str[5]))
    return time


def get_meta_from_exif(exif_data):
    """Gather meta header from the EXIF data."""

    if "EXIF ExposureTime" in exif_data:
        exposure_tag = exif_data['EXIF ExposureTime']
        exposure_time = exposure_tag.values[0].num / exposure_tag.values[
            0].den * u.s
    if "Image Artist" in exif_data:
        author_str = exif_data['Image Artist'].values

    if "Image Model" in exif_data:
        camera_model_str = exif_data['Image Model'].values
    lat, lon = get_exif_location(exif_data)
    if ((lat != None) and (lon != None)):
        gps = [lat, lon] * u.deg

    time = get_image_time(exif_data)

    result = {}
    result.update({'AUTHOR': author_str})
    result.update({'EXPTIME': exposure_time.to('s').value})
    result.update({'TELECOP': camera_model_str})
    result.update({'LAT': gps[0].to_value(u.deg)})
    result.update({'LON': gps[1].to_value(u.deg)})
    result.update({'DATEOBS': time.isoformat()})
    return result


def get_plate_scale(time, im_radius):
    dsun = sunpy.coordinates.sun.earth_distance(time.isoformat())
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
    time = get_image_time(exif_data)
    wcs.wcs.dateobs = time.isoformat()
    header = MetaDict(dict(wcs.to_header()))

    header.update(get_meta_from_exif(exif_data))
    dsun = sunpy.coordinates.sun.earth_distance(time.isoformat())
    lat = header.get('LAT') * u.deg
    lon = header.get('LON') * u.deg
    solar_rotation_angle = get_solar_rotation_angle(lat, lon, time)
    header.update({'crota2': solar_rotation_angle.to('deg').value})
    header.update({'dsun_obs': dsun.to('m').value})
    hgln_obs = 0 * u.deg
    hglt_obs = sunpy.coordinates.sun.B0(time)
    header.update({'hgln_obs': hgln_obs.to('deg').value})
    header.update({'hglt_obs': hglt_obs.to('deg').value})
    header.update({'ctype1': 'HPLN-TAN'})
    header.update({'ctype2': 'HPLT-TAN'})
    header.update({'rsun': dsun.to('m').value})
    header.update({'rsun_obs': np.arctan(sunpy.sun.constants.radius / dsun).to(
        'arcsec').value})
    return header


def get_solar_rotation_angle(lat, lon, time, fudge_angle=0):
    """Get the solar rotation angle"""
    loc = EarthLocation(lat=lat, lon=lon)
    solar_rotation_angle = sunpy.coordinates.sun.orientation(loc, time)
    return solar_rotation_angle + fudge_angle

