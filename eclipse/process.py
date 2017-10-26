from skimage.transform import hough_circle, hough_circle_peaks
import scipy.ndimage as ndimage
import numpy as np
import astropy.units as u


def find_center_and_radius(im):
    """Given an image of the eclipsed Sun find the center and radius of the
    image."""

    blur_im = ndimage.gaussian_filter(im, 8)
    mask = blur_im > blur_im.mean() * 3

    # the following code limits the region to search for the circle of the Sun
    label_im, nb_labels = ndimage.label(mask)
    slice_x, slice_y = ndimage.find_objects(label_im == 1)[0]
    roi = blur_im[slice_x, slice_y]

    # take the derivative of the image to find the edges of the Sun
    sx = ndimage.sobel(roi, axis=0, mode='constant')
    sy = ndimage.sobel(roi, axis=1, mode='constant')
    sob = np.hypot(sx, sy)

    hough_radii = np.arange(np.floor(np.mean(sob.shape) / 4),
                            np.ceil(np.mean(sob.shape) / 2), 10)
    hough_res = hough_circle(sob > (sob.mean() * 5), hough_radii)

    # Select the most prominent circle
    accums, cy, cx, radius = hough_circle_peaks(hough_res, hough_radii,
                                                total_num_peaks=1)

    im_cx = (cx + slice_x.start) * u.pix
    im_cy = (cy + slice_y.start) * u.pix
    im_radius = radius * u.pix

    return im_cx, im_cy, im_radius
