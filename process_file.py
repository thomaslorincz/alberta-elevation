import csv
import os
import re
import sys

from PyInquirer import style_from_dict, Token, prompt
from pyproj import Transformer

import common


def interactive_cli():
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

    input_questions = [
        {
            "type": "list",
            "message": "Select an input file",
            "name": "input",
            "choices": [{"name": file} for file in csv_files]
        },
        {
            "type": "list",
            "message": "Select the coordinate system",
            "name": "system",
            "choices": [
                {"name": "Lon/Lat (EPSG 4326)"},
                {"name": "X/Y (EPSG 3776)"}
            ]
        }
    ]

    input_answers = prompt(input_questions, style=style)

    with open(input_answers["input"], "r") as in_file:
        reader = csv.DictReader(in_file)

        if input_answers["system"] == "Lon/Lat (EPSG 4326)":
            h_column, v_column = "longitude", "latitude"
            system = "lonlat"
        else:
            h_column, v_column = "x-coordinate", "y-coordinate"
            system = "xy"

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

        return [
            input_answers["input"],
            system,
            process_answers["horizontal"],
            process_answers["vertical"],
            process_answers["output"]
        ]


def main():
    if len(sys.argv) == 5 or len(sys.argv) == 6:
        input_file = sys.argv[1]
        system = sys.argv[2].lower()
        if system != "lonlat" and system != "xy":
            print("Error: Argument 2 must be 'lonlat' or 'xy'.")
            exit(1)
        horizontal = sys.argv[3]
        vertical = sys.argv[4]
        if len(sys.argv) == 6:
            output_file = sys.argv[5]
        else:
            output_file = "output.csv"
    else:
        interactive_answers = interactive_cli()
        input_file = interactive_answers[0]
        system = interactive_answers[1]
        horizontal = interactive_answers[2]
        vertical = interactive_answers[3]
        output_file = interactive_answers[4]

    transformer = Transformer.from_crs("EPSG:3776", "EPSG:4326")

    with open(input_file, "r") as in_file, \
            open(output_file, "w", newline="") as out_file:
        reader = csv.DictReader(in_file)
        fieldnames = reader.fieldnames + ["elevation"]
        writer = csv.DictWriter(out_file, fieldnames=fieldnames)

        writer.writeheader()
        for row in reader:
            if system == "lonlat":
                lon, lat = row[horizontal], row[vertical]
            else:
                lat, lon = transformer.transform(row[horizontal], row[vertical])

            lon, lat = abs(lon), abs(lat)

            row_dict = row
            data_file = common.get_data_file(lon, lat)
            row_dict["elevation"] = common.get_elevation(data_file, lon, lat)
            writer.writerow(row_dict)


if __name__ == "__main__":
    main()
