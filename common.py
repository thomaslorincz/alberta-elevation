import math
import os

import numpy as np

ELEVATION_DICT = {}
SAMPLES = 3601


def get_elevation(filename, lon, lat):
    """
    Get the elevation at the provided lat/lon in meters. The resolution of the
    data is 1 arc-second (~30m). For SRTM data with 3 arc-second resolution,
    change the number of samples from 3601 to 1201.
    Credit: Aatish Neupane
    Link: https://librenepal.com/article/reading-srtm-data-with-python/
    :param filename: The name of the HGT file to use
    :param lat: The latitude of the desired point.
    :param lon: The longitude of the desired point.
    :return: The elevation of the desired point (in meters).
    """
    if filename in ELEVATION_DICT:
        elevations = ELEVATION_DICT[filename]
    else:
        with open(os.path.join("data", filename), "rb") as file:
            # HGT is 16bit signed integer(i2) - big endian(>)
            elevations = np.fromfile(file, np.dtype('>i2'), SAMPLES**2)\
                .reshape((SAMPLES, SAMPLES))
            ELEVATION_DICT[filename] = elevations

    lat_row = int(round((lat - int(lat)) * (SAMPLES - 1), 0))
    lon_row = int(round((lon - int(lon)) * (SAMPLES - 1), 0))
    return elevations[SAMPLES - 1 - lat_row, lon_row].astype(int)


def get_data_file(lon, lat):
    """
    Returns the correct HGT data file to get elevation from.
    Credit: Aatish Neupane
    Link: https://librenepal.com/article/reading-srtm-data-with-python/
    :param lat: The latitude of the desired point.
    :param lon: The longitude of the desired point.
    :return: The name of the data file.
    :raise: ValueError: If lat/lon are not within supported bounds.
    """

    if 48 <= math.floor(lat) < 60 and 110 < math.floor(lon) <= 121:
        return "N{}W{}.hgt".format(math.floor(lat), math.floor(lon))
    else:
        raise ValueError("Point does not fall within supported bounds")
