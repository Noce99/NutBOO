import socket


class GpsLivelox:
    def __init__(self):
        host = "0.0.0.0"
        port = 10999

        self.server_socket = socket.socket()
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((host, port))
        self.lon = None
        self.lat = None

    def listen_forever(self):
        while True:
            self.server_socket.listen(2)
            conn, address = self.server_socket.accept()
            print("Connection from: " + str(address))
            conn.recv(1280)
            message = '\x01'
            message = message.encode('utf-8')
            conn.send(message)
            data = conn.recv(1280)
            self.lon = self.coordinate_formater(data.hex()[38:46])
            self.lat = self.coordinate_formater(data.hex()[46:54])
            print(f"{self.lat} N  {self.lon} E")
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
