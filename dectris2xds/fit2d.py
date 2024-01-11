import warnings

import numpy as np
from scipy.optimize import leastsq

"""
https://gist.github.com/andrewgiessel/6122739
fit of 2D data to rotated gaussian 
"""


def gaussian(height, center_x, center_y, width_x, width_y, rotation):
    """Returns a gaussian function with the given parameters"""
    width_x = float(width_x)
    width_y = float(width_y)

    rotation = np.deg2rad(rotation)
    tmp_x = center_x
    center_x = center_x * np.cos(rotation) - center_y * np.sin(rotation)
    center_y = tmp_x * np.sin(rotation) + center_y * np.cos(rotation)

    def rotgauss(x, y):
        xp = x * np.cos(rotation) - y * np.sin(rotation)
        yp = x * np.sin(rotation) + y * np.cos(rotation)
        g = height * np.exp(-(((center_x - xp) / width_x) ** 2 +
                              ((center_y - yp) / width_y) ** 2) / 2.)
        return g

    return rotgauss


def moments(data):
    """Returns (height, x, y, width_x, width_y)
    the gaussian parameters of a 2D distribution by calculating its
    moments. NaN values are replaced with zero
    """

    data = np.nan_to_num(data)
    total = data.sum()
    X, Y = np.indices(data.shape)
    x = (X * data).sum() / total
    y = (Y * data).sum() / total
    col = data[:, int(y)]
    width_x = np.sqrt(np.abs((np.arange(col.size) - y) ** 2 * col).sum() / col.sum())
    row = data[int(x), :]
    width_y = np.sqrt(np.abs((np.arange(row.size) - x) ** 2 * row).sum() / row.sum())
    height = data.max()
    return height, x, y, width_x, width_y, 0.0


def fitgaussian(data, maxfev=100000, overflow_value=-1):
    """Returns (height, x, y, width_x, width_y)
    the gaussian parameters of a 2D distribution found by a fit"""
    params = moments(data)

    # set all values marking an overflow to NaN, so we can filter it out later more easily
    data[data == overflow_value] = np.nan

    def errorfunction(p):
        diffs = np.ravel(gaussian(*p)(*np.indices(data.shape)) - data)
        return diffs[~np.isnan(diffs)]

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        p, success = leastsq(errorfunction, params, maxfev=maxfev)

    return p, success


if __name__ == "__main__":
    pass
