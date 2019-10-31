# Alberta Elevation
Easy-to-use scripts for getting the elevations of geographic points within Alberta
## Support
- Python 3.x is supported
- Input points can be Lon/Lat [(EPSG:4326)](https://spatialreference.org/ref/epsg/wgs-84/) or X/Y [(EPSG:3776)](https://spatialreference.org/ref/epsg/nad83-alberta-3tm-ref-merid-114-w/)
- All input points within Alberta are supported:
    - Longitude Bounds: [120° W, 110° W)
    - Latitude Bounds: [49° N, 60° N)
## Data
- This project uses HGT files from the Shuttle Radar Topography Mission [(SRTM)](https://en.wikipedia.org/wiki/Shuttle_Radar_Topography_Mission) with 30 meter resolution.
- HGT files are binary files with all samples stored as signed 16-bit integers (big endian byte order).
- All data files can be found in the data directory.
## Setup
```
git clone https://github.com/thomaslorincz/alberta-elevation
cd alberta-elevation
pip install -r requirements.txt
```
Note: It is recommended to use a [virtual environment](https://docs.python.org/3/library/venv.html)
## process_point.py
### Usage
```
python process_point.py <lon/x> <lat/y>
```
Parameters:
- lon: The West longitude of the point (positive/negative floating point number)
- lat: The North latitude of the point (positive/negative floating point number)

Output:
- This script prints its output to standard output.
### Example
```
python process_point.py -113.4938 53.5461 
```
## process_file.py
### Usage
Use the interactive CLI:
```
python process_file.py
```
Or, use command line arguments:
```
python process_file.py <input> <coordinate system> <horizontal> <vertical> <output>
```
Arguments:
- input: The path to the input file
- coordinate system: Either "lonlat" or "xy"
- horizontal: The name of the column with horizontal coordinate data
- vertical: The name of the column with vertical coordinate data
- output (optional): The path to the output file (default = "output.csv")
Example:
```
python process_file.py input.csv xy x-coord y-coord elevation_data.csv
```
Output:
- This script will output a new file according to the options specified.
