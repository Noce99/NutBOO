import socket
from threading import Thread
import crcmod
from datetime import datetime
import time
from pymongo import MongoClient

YEAR=2024

socket.setdefaulttimeout(5)
crc16 = crcmod.mkCrcFun(0x18005, rev=False, initCrc=0xFFFF, xorOut=0x0000)
client = MongoClient('mongodb://localhost:27017/')
db = client[f"boo{YEAR}"]
GPS = db["gps"]


class GpsLivelox:
    def __init__(self):
        host = "0.0.0.0"
        port = 10999

        self.server_socket = socket.socket()
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((host, port))
        self.lon = None
        self.lat = None
        self.time = None

        self.thread = Thread(target=self.listen_forever)

    def listen_forever(self):
        while True:
            self.server_socket.listen(2)
            try:
                conn, address = self.server_socket.accept()
            except TimeoutError:
                continue
            print("Accepted!")
            Thread(target=self.deal_with_a_new_connection, args=[conn, address]).start()
            print("Continuing!")


    @staticmethod
    def coordinate_formater(hex_coordinate):
        coordinate = int(hex_coordinate, 16)
        if coordinate & (1 << 31):
            new_int = coordinate - 2 ** 32
            dec_coordinate = new_int / 1e7
        else:
            dec_coordinate = coordinate / 10000000
        return dec_coordinate

    @staticmethod
    def deal_with_a_new_connection(conn, address):
        print("Connection from: " + str(address))

        # Ask the GPS some data
        try:
            gps_id = conn.recv(1280)
        except TimeoutError:
            exit()

        imei_length = int.from_bytes(gps_id[:2])
        imei = int.from_bytes(gps_id[2:2 + imei_length])
        print(f"GPS ID: {imei} [imei_length={imei_length}, total_message_length={len(gps_id)}]")
        answer = 1
        answer = answer.to_bytes(1, 'big')
        # print(f"{answer}")
        conn.send(answer)

        # Received Data
        try:
            data = conn.recv(2000)
        except TimeoutError:
            answer = 0
            answer = answer.to_bytes(1, 'big')
            conn.send(answer)
            exit()
        # print(len(data))

        preamble = int.from_bytes(data[:4])
        # print(f"Preamble = {preamble}")
        data_field_length = int.from_bytes(data[4:8])
        # print(f"data_field_length = {data_field_length} [should be={len(data)-12}]")
        codec_id = int.from_bytes(data[8:9])
        # print(f"codec_id = {codec_id} [should be=142]")
        number_of_data_1 = int.from_bytes(data[9:10])
        number_of_data_2 = int.from_bytes(data[-5:-4])
        # print(f"number_of_data = {number_of_data_1} [should be={number_of_data_2}]")
        crc = int.from_bytes(data[-4:])
        # print(f"crc = {crc} [should be={crc16(data[8:-4])}]")

        """
        READ ALL DATA:
        if number_of_data_1 != 0:
            avl_data_length = len(data) - 15
            per_data_length = avl_data_length // number_of_data_1
            start = 10
            for i in range(number_of_data_1):
                timestamp = int.from_bytes(data[start:start + 8])
                gps_element = data[start + 9:start + 9 + 15]
                lon = int.from_bytes(gps_element[:4])
                lat = int.from_bytes(gps_element[4:8])
                speed = int.from_bytes(gps_element[-2:])
                print(f"[{datetime.fromtimestamp(timestamp / 1000)}] [{lon} E; {lat} N] {speed}")
                start += per_data_length
        """
        start = 10
        timestamp = int.from_bytes(data[start:start + 8])
        gps_element = data[start + 9:start + 9 + 15]
        lon = int.from_bytes(gps_element[:4])
        lat = int.from_bytes(gps_element[4:8])
        speed = int.from_bytes(gps_element[-2:])
        print(f"[{datetime.fromtimestamp(timestamp / 1000)}] [{lon} E; {lat} N] {speed}")

        result = GPS.update_one(
        {"gps_id": str(imei)},
        {"$set": {"last_location": {"time": timestamp / 1000, "lat": lat / 10000000, "lon": lon / 10000000}}}
        )
        if result.modified_count == 0:
            print(f"Unknown GPS: {imei}")
        else:
            print("Pushed GPS data in the dataset!")

        answer = number_of_data_1
        answer = answer.to_bytes(1, 'big')
        conn.send(answer)
        conn.close()