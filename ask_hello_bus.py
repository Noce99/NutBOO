import requests
import xml.etree.ElementTree as ET


def ask_fermata_linee_time(fermata, linea="", oraHHMM=""):
    response = requests.post(
        "https://hellobuswsweb.tper.it/web-services/hello-bus.asmx/QueryHellobus", 
        data={"fermata": fermata, "linea": linea, "oraHHMM": oraHHMM},
    )
    answer = response.text

    tree = ET.ElementTree(ET.fromstring(answer))

    print(tree.getroot().text)
    

def ask_carico_bus():
    response = requests.post(
        "https://hellobuswsweb.tper.it/web-services/hello-bus.asmx/QueryAllBusLd", 
        data={},
    )
    answer = response.text
    print(answer)
    
def ask_fermata_linee_time_ivr(fermata, linea="", oraHHMM=""):
    response = requests.post(
        "https://hellobuswsweb.tper.it/web-services/hello-bus.asmx/QueryHellobus4ivr", 
        data={"fermata": fermata, "linea": linea, "oraHHMM": oraHHMM},
    )
    answer = response.text

    tree = ET.ElementTree(ET.fromstring(answer))

    print(tree.getroot().text)

def ask_fermata_linee_time_ivr_ld(fermata, linea="", oraHHMM=""):
    response = requests.post(
        "https://hellobuswsweb.tper.it/web-services/hellobus.asmx/QueryHellobus4ivrLd", 
        data={"fermata": fermata, "linea": linea, "oraHHMM": oraHHMM},
    )
    answer = response.text

    tree = ET.ElementTree(ET.fromstring(answer))

    print(tree.getroot().text)
    
def ask_fermata_linee_time_ld(fermata, linea="", oraHHMM=""):
    response = requests.post(
        "https://hellobuswsweb.tper.it/web-services/hellobus.asmx/QueryHellobusLd", 
        data={"fermata": fermata, "linea": linea, "oraHHMM": oraHHMM},
    )
    answer = response.text

    tree = ET.ElementTree(ET.fromstring(answer))

    print(tree.getroot().text)

def ask_resale(fermata):
    response = requests.post(
        "https://hellobuswsweb.tper.it/web-services/hellobus.asmx/QueryResale", 
        data={"fermata": fermata},
    )
    answer = response.text

    tree = ET.ElementTree(ET.fromstring(answer))

    print(tree.getroot().text)

    
if __name__ == "__main__":
    while True:
        ask_fermata_linee_time(2002)
    # ask_carico_bus()
    # ask_fermata_linee_time_ivr(2002)
    # ask_fermata_linee_time_ivr_ld(567)
    # ask_fermata_linee_time_ld(2002)
    # ask_resale(2002)
    
