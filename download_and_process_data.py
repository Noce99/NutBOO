import os
import pathlib
import requests
import csv
import json


if __name__ == "__main__":
    urls = {
        "list_of_the_file.csv": "https://solweb.tper.it/web/tools/open-data/open-data-download.aspx?source=solweb.tper.it&filename=opendata-versione&version=1&format=csv",
        "ticket_seller.csv": "https://solweb.tper.it/web/tools/open-data/open-data-download.aspx?source=solweb.tper.it&filename=rivendite&version=20241001&format=csv",
        "areas.csv": "https://solweb.tper.it/web/tools/open-data/open-data-download.aspx?source=solweb.tper.it&filename=zone&version=20241001&format=csv",
        "cities.csv": "https://solweb.tper.it/web/tools/open-data/open-data-download.aspx?source=solweb.tper.it&filename=localitazone&version=20241001&format=csv",
        "train_lines.csv": "https://solweb.tper.it/web/tools/open-data/open-data-download.aspx?source=solweb.tper.it&filename=lineeferroviarie&version=20241001&format=csv",
        "train_stations.csv": "https://solweb.tper.it/web/tools/open-data/open-data-download.aspx?source=solweb.tper.it&filename=stazioniferroviarie&version=20241001&format=csv",
        "arcs_buses.csv": "https://solweb.tper.it/web/tools/open-data/open-data-download.aspx?source=solweb.tper.it&filename=archi&version=20241001&format=csv",
        "bus_stops.csv": "https://solweb.tper.it/web/tools/open-data/open-data-download.aspx?source=solweb.tper.it&filename=fermate&version=20241001&format=csv",
        "bus_numbers.csv": "https://solweb.tper.it/web/tools/open-data/open-data-download.aspx?source=solweb.tper.it&filename=linee&version=20241001&format=csv",
        "bus_numbers_arcs_connection.csv": "https://solweb.tper.it/web/tools/open-data/open-data-download.aspx?source=solweb.tper.it&filename=lineepercorsi&version=20241001&format=csv",
        "bus_numbers_stops_connection.csv": "https://solweb.tper.it/web/tools/open-data/open-data-download.aspx?source=solweb.tper.it&filename=lineefermate&version=20241001&format=csv",
        "bus_bologna_gtfs.csv": "https://solweb.tper.it/web/tools/open-data/open-data-download.aspx?source=solweb.tper.it&filename=gommagtfsbo&version=20241018&format=zip",
        "bus_ferrara_gtfs.csv": "https://solweb.tper.it/web/tools/open-data/open-data-download.aspx?source=solweb.tper.it&filename=gommagtfsfe&version=20241018&format=zip",
        "people_mover_gtfs.csv": "https://solweb.tper.it/web/tools/open-data/open-data-download.aspx?source=solweb.tper.it&filename=gtfsmex&version=20240115&format=zip",
    }
    # Let's create the dataset folder
    current_path = pathlib.Path(__file__).parent.resolve()
    dataset_path = os.path.join(current_path, "datasets")
    if not os.path.exists(dataset_path):
        os.mkdir(dataset_path)
    # Let's create the original_data folder
    original_data = os.path.join(dataset_path, "original_data")
    if not os.path.exists(original_data):
        os.mkdir(original_data)

    # Let's download everything
    for filename, url in urls.items():
        response = requests.get(url)
        with open(os.path.join(original_data, filename), "wb") as file:
            file.write(response.content)

    # Let's create the processed_data folder
    processed_data = os.path.join(dataset_path, "processed_data")
    if not os.path.exists(processed_data):
        os.mkdir(processed_data)

    # Let's Process bus_stops
    with open(os.path.join(original_data, "bus_stops.csv"), mode='r') as infile:
        csvFile = csv.reader(infile, delimiter=';')
        csvFile.__next__()
        bus_stops = [{"name": bus_stop[1], "verbal_location": bus_stop[2],
                      "x": int(bus_stop[4]), "y": int(bus_stop[5]), "zone_code": bus_stop[8]}
                     for bus_stop in csvFile]

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
        with open(os.path.join(processed_data, "bus_stops.json"), "w") as outfile:
            json.dump(bus_stops, outfile)