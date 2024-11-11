import csv
import json


def from_csv_to_json(csv_path, json_path):
    pass

def process_bus_stops(csv_input_path, json_output_path):
    with open(csv_input_path, mode='r') as infile:
        csvFile = csv.reader(infile, delimiter=';')
        csvFile.__next__()

        bus_stops = []
        for bus_stop in csvFile:
            lat = float(bus_stop[6].replace(",", "."))
            lon = float(bus_stop[7].replace(",", "."))
            if 44.47267601010103 < lat < 44.50946314343433 and 11.256635603112843 < lon < 11.365479808365757:
                bus_stops.append(
                    {"name": bus_stop[1], "verbal_location": bus_stop[2],
                     "x": int(bus_stop[4]), "y": int(bus_stop[5]),
                     "lat": lat, "lon": lon,
                     "zone_code": bus_stop[8]}
                )


        x_tot = 0
        y_tot = 0
        for el in bus_stops:
            x_tot += el["x"]
            y_tot += el["y"]
        x_mean = x_tot / len(bus_stops)
        y_mean = y_tot / len(bus_stops)
        for el in bus_stops:
            el["x"] -= x_mean
            el["y"] -= y_mean

        # Writing to sample.json
        with open(json_output_path, "w") as outfile:
            json.dump(bus_stops, outfile)