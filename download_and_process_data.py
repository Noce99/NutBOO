import os
import pathlib
import requests
import csv
import json

import urllib.request
from bs4 import BeautifulSoup

version = "20241101"

if __name__ == "__main__":

    # Get File Links
    fp = urllib.request.urlopen("https://solweb.tper.it/web/tools/open-data/open-data.aspx")
    my_html_as_bytes = fp.read()

    my_html_as_str = my_html_as_bytes.decode("utf8")

    soup = BeautifulSoup(my_html_as_str, 'html.parser')
              
    files_containing_tper_data = {}
    for i in range(14):
        files_containing_tper_data[i] = {
            "file_name": soup.find(attrs={'id': f"ContentPlaceHolderMain_rptOpenData_lblNomeFile_{i}"}).text,
            "version": soup.find(attrs={'id': f"ContentPlaceHolderMain_rptOpenData_lblVersione_{i}"}).text,
            "description": soup.find(attrs={'id': f"ContentPlaceHolderMain_rptOpenData_lblDescrizione_{i}"}).text,
            "link_to_download_page": soup.find(attrs={'id': f"ContentPlaceHolderMain_rptOpenData_hlnkDettagli_{i}"})["href"],
        }
    # print(files_containing_tper_data)
    
    for element in files_containing_tper_data:
        fp = urllib.request.urlopen(f"https://solweb.tper.it/web/tools/open-data/{files_containing_tper_data[element]['link_to_download_page']}")
        my_html_as_bytes = fp.read()
        my_html_as_str = my_html_as_bytes.decode("utf8")
        soup = BeautifulSoup(my_html_as_str, 'html.parser')
        for e in soup.find_all("a"):
            if "id" in e.attrs.keys() and "ContentPlaceHolderMain_hlnkFormatoCsv" in e["id"]:
                files_containing_tper_data[element]["download_link"] = e["href"]
        if "download_link" not in files_containing_tper_data[element].keys():
            print(my_html_as_str)
            if "id" in e.attrs.keys() and "hlnkFormatoGtfs" in e["id"]:
                print("aaa")
                files_containing_tper_data[element]["download_link"] = e["href"]
        if "download_link" not in files_containing_tper_data[element].keys():
            print(f"Not able to find! {files_containing_tper_data[element]['file_name']}")
        
    print(files_containing_tper_data)
        # print("@"*150)
    exit()
    
    
    urls = {
        "list_of_the_file.csv": "https://solweb.tper.it/web/tools/open-data/open-data-download.aspx?source=solweb.tper.it&filename=opendata-versione&version=1&format=csv",
        "ticket_seller.csv": f"https://solweb.tper.it/web/tools/open-data/open-data-download.aspx?source=solweb.tper.it&filename=rivendite&version={version}&format=csv",
        "areas.csv": f"https://solweb.tper.it/web/tools/open-data/open-data-download.aspx?source=solweb.tper.it&filename=zone&version={version}&format=csv",
        "cities.csv": f"https://solweb.tper.it/web/tools/open-data/open-data-download.aspx?source=solweb.tper.it&filename=localitazone&version={version}&format=csv",
        "train_lines.csv": f"https://solweb.tper.it/web/tools/open-data/open-data-download.aspx?source=solweb.tper.it&filename=lineeferroviarie&version={version}&format=csv",
        "train_stations.csv": f"https://solweb.tper.it/web/tools/open-data/open-data-download.aspx?source=solweb.tper.it&filename=stazioniferroviarie&version={version}&format=csv",
        "arcs_buses.csv": f"https://solweb.tper.it/web/tools/open-data/open-data-download.aspx?source=solweb.tper.it&filename=archi&version={version}&format=csv",
        "bus_stops.csv": f"https://solweb.tper.it/web/tools/open-data/open-data-download.aspx?source=solweb.tper.it&filename=fermate&version={version}&format=csv",
        "bus_numbers.csv": f"https://solweb.tper.it/web/tools/open-data/open-data-download.aspx?source=solweb.tper.it&filename=linee&version={version}&format=csv",
        
        "bus_numbers_arcs_connection.csv": f"https://solweb.tper.it/web/tools/open-data/open-data-download.aspx?source=solweb.tper.it&filename=lineepercorsi&version={version}&format=csv",
        "bus_numbers_stops_connection.csv": f"https://solweb.tper.it/web/tools/open-data/open-data-download.aspx?source=solweb.tper.it&filename=lineefermate&version={version}&format=csv",
        "bus_bologna_gtfs.csv": f"https://solweb.tper.it/web/tools/open-data/open-data-download.aspx?source=solweb.tper.it&filename=gommagtfsbo&version=20241018&format=zip",
        "bus_ferrara_gtfs.csv": f"https://solweb.tper.it/web/tools/open-data/open-data-download.aspx?source=solweb.tper.it&filename=gommagtfsfe&version=20241018&format=zip",
        "people_mover_gtfs.csv": f"https://solweb.tper.it/web/tools/open-data/open-data-download.aspx?source=solweb.tper.it&filename=gtfsmex&version=20240115&format=zip",
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
    for file_to_download in files_containing_tper_data:
        response = requests.get(f"")
        with open(os.path.join(original_data, file_to_download["file_name"]), "wb") as file:
            file.write(response.content)
    """
    for filename, url in urls.items():
        response = requests.get(url)
        with open(os.path.join(original_data, filename), "wb") as file:
            file.write(response.content)
    """

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
