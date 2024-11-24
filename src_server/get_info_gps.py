import socket
from threading import Thread


class GpsLivelox:
    def __init__(self):
        host = "0.0.0.0"
        port = 10999

        self.server_socket = socket.socket()
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((host, port))
        self.lon = None
        self.lat = None

        self.thread = Thread(target=self.listen_forever)

    def listen_forever(self):
        while True:
            self.server_socket.listen(2)
            conn, address = self.server_socket.accept()
            print("Connection from: " + str(address))
            gps_id = conn.recv(1280)
            message = '\x01'
            message = message.encode('utf-8')
            conn.send(message)
            data = conn.recv(1280)

            preamble = data[:4]
            data_field_lenght = data[4:8]
            codec_id = data[8:9]
            number_of_data = data[9:10]
            print(preamble)
            print(data_field_lenght)
            print(codec_id)
            print(int.from_bytes(number_of_data, "big"))
            num_of_data = int.from_bytes(number_of_data, "big")
            timestamp = data[10:18]
            priority = data[18:19]
            lon = data[19:23]
            lat = data[23:25]
            print(f"{timestamp} {priority} {lon} {lat}")
            self.lon = self.coordinate_formater(data.hex()[38:46])
            self.lat = self.coordinate_formater(data.hex()[46:54])
            print(f"{self.lat} N  {self.lon} E")
            message = '\x01'
            message = message.encode('utf-8')
            conn.send(message)
            conn.close()

    @staticmethod
    def coordinate_formater(hex_coordinate):
        coordinate = int(hex_coordinate, 16)
        if coordinate & (1 << 31):
            new_int = coordinate - 2 ** 32
            dec_coordinate = new_int / 1e7
        else:
            dec_coordinate = coordinate / 10000000
        return dec_coordinate
