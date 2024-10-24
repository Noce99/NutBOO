import os
import pathlib
import requests


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
    # Let's create the csv folder
    csv_path = os.path.join(dataset_path, "original_data")
    if not os.path.exists(csv_path):
        os.mkdir(csv_path)

    # Let's download everything
    for filename, url in urls.items():
        response = requests.get(url)
        with open(os.path.join(csv_path, filename), "wb") as file:
            file.write(response.content)