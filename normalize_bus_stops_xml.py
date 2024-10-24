import xml.etree.ElementTree as Et
import pathlib
import os
import json


if __name__ == "__main__":
    nut_bus_main_folder = pathlib.Path(__file__).parent.resolve()
    datasets_folder = os.path.join(nut_bus_main_folder, "datasets")
    tree = Et.parse(os.path.join(datasets_folder, "bus_stops.xml"))
    bus_stop_dataset = tree.getroot()
    bus_stops = [{"name": bus_stop[1].text, "verbal_location": bus_stop[2].text,
                  "x": int(bus_stop[4].text), "y": int(bus_stop[5].text), "zone_code": bus_stop[8].text}
                 for bus_stop in bus_stop_dataset]

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
    with open(os.path.join(datasets_folder, "bus_stops_normalized.json"), "w") as outfile:
        json.dump(bus_stops, outfile)
