import csv
import os
import re

from PyInquirer import style_from_dict, Token, prompt
from pyproj import Transformer

import common


def main():
    style = style_from_dict({
        Token.Selected: "#00ff00",
        Token.Pointer: "#00ff00",
        Token.Answer: "#00ff00",
    })
    
    csv_files = [
        f for f in os.listdir(".")
        if re.match(r".*\.csv", f, re.IGNORECASE)
    ]
    
    if len(csv_files) == 0:
        print("Error: No CSV input files detected in the current directory.")
        exit(1)
        
    input_question = [
        {
            "type": "list",
            "message": "Select an input file",
            "name": "input",
            "choices": [{"name": file} for file in csv_files]
        },
        {
            "type": "list",
            "message": "Select the coordinate scheme",
            "name": "scheme",
            "choices": [{"name": "Lon/Lat"}, {"name": "X/Y"}]
        }
    ]
    
    input_answer = prompt(input_question, style=style)
    
    with open(input_answer["input"], "r") as f:
        reader = csv.DictReader(f)

        if input_answer["scheme"] == "Lon/Lat":
            h_column = "longitude"
            v_column = "latitude"
            lonlat = True
        else:
            h_column = "x-coordinate"
            v_column = "y-coordinate"
            transformer = Transformer.from_crs("EPSG:3776", "EPSG:4326")
            lonlat = False
        
        process_questions = [
            {
                "type": "list",
                "message": "Select the name of the {} column".format(h_column),
                "name": "horizontal",
                "choices": [{"name": col} for col in reader.fieldnames]
            },
            {
                "type": "list",
                "message": "Select the name of the {} column".format(v_column),
                "name": "vertical",
                "choices": [{"name": col} for col in reader.fieldnames]
            },
            {
                "type": "input",
                "message": "Enter the output file name",
                "name": "output",
                "default": "output.csv"
            }
        ]

        process_answers = prompt(process_questions, style=style)

        with open(process_answers["output"], "w", newline="") as f:
            fieldnames = reader.fieldnames + ["elevation"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            h, v = process_answers["horizontal"], process_answers["vertical"]

            writer.writeheader()
            for i, row in enumerate(reader):
                if lonlat:
                    lon, lat = row[h], row[v]
                else:
                    lat, lon = transformer.transform(row[h], row[v])

                lon, lat = abs(lon), abs(lat)

                row_dict = row
                data_file = common.get_data_file(lon, lat)
                row_dict["elevation"] \
                    = common.get_elevation(data_file, lon, lat)
                writer.writerow(row_dict)


if __name__ == "__main__":
    main()
