import math
import sys

from pyproj import Transformer

import common


def main():
    if len(sys.argv) != 3:
        print("Error: Expected 2 arguments.")
        print("Usage: 'python process_point.py <lon/x> <lat/y>'")
        print("Example: 'python process_point.py -113.4938 53.5461'")

    horizontal = abs(float(sys.argv[1]))
    vertical = abs(float(sys.argv[2]))

    if math.log10(vertical) != 2 or math.log10(horizontal) != 3:
        transformer = Transformer.from_crs("EPSG:3776", "EPSG:4326")
        lat, lon = transformer.transform(horizontal, vertical)
    else:
        lon, lat = horizontal, vertical

    data_file = common.get_data_file(lon, lat)
    print(common.get_elevation(data_file, lon, lat))


if __name__ == "__main__":
    main()
