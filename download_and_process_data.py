import os
import pathlib
import requests

import urllib.request
from bs4 import BeautifulSoup
from tqdm import tqdm
import zipfile

from process_functions import process_bus_stops


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
                files_containing_tper_data[element]["file_extension"] = ".csv"
            if "download_link" not in files_containing_tper_data[element].keys():
                if "id" in e.attrs.keys() and "ContentPlaceHolderMain_hlnkFormatoGtfs" in e["id"]:
                    files_containing_tper_data[element]["download_link"] = e["href"]
                    files_containing_tper_data[element]["file_extension"] = ".zip"
        if "download_link" not in files_containing_tper_data[element].keys():
            print(f"Not able to find! {files_containing_tper_data[element]['file_name']}")
        
    print(files_containing_tper_data)

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
    list_of_original_data_path = []
    for file_to_download in tqdm(files_containing_tper_data):
        url_end = files_containing_tper_data[file_to_download]["download_link"]
        file_name = files_containing_tper_data[file_to_download]["file_name"]
        file_extension = files_containing_tper_data[file_to_download]["file_extension"]
        response = requests.get(f"https://solweb.tper.it/web/tools/open-data/{url_end}")
        with open(os.path.join(original_data, file_name + file_extension), "wb") as file:
            file.write(response.content)
        list_of_original_data_path.append(os.path.join(original_data, file_name + file_extension))

    # Let's create the processed_data folder
    processed_data = os.path.join(dataset_path, "processed_data")
    if not os.path.exists(processed_data):
        os.mkdir(processed_data)

    # Let's Process data
    preferred_file_name = {
        "fermate": "bus_stops",
        "gommagtfsbo": "busses_bologna",
        "gommagtfsfe": "busses_ferrara",
    }
    process_functions = {
        "bus_stops" : process_bus_stops,
    }
    for original_data_path in list_of_original_data_path:
        file_name = original_data_path[:-4].split("/")[-1]
        extension = original_data_path[-4:]
        # Let's check if we have a preferred name for it
        if file_name in preferred_file_name.keys():
            file_name = preferred_file_name[file_name]
        # If it's a zip file let's extract it
        if extension == ".zip":
            extracted_folder_path = os.path.join(dataset_path, "processed_data", file_name)
            with zipfile.ZipFile(original_data_path, 'r') as zip_ref:
                zip_ref.extractall(extracted_folder_path)
        # If it's a csv let's translate into a json
        elif extension == ".csv":
            if file_name in process_functions.keys():
                json_path = os.path.join(dataset_path, "processed_data", file_name + ".json")
                process_functions[file_name](original_data_path, json_path)
        else:
            raise Exception(f"Unsupported file extension! It must be in [\".csv\", \".zip\"] but it's: {extension}")
    exit()
