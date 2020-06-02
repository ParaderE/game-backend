import uuid
import json
import socket


class Player:

    def __init__(self, addr, port, login):
        self.login = login
        self.location = 4
        self.coords = (200, 200)
        self.id = str(uuid.uuid4)
        self.addr = addr
        self.udp_addr = (addr[0], int(port))

    def send_tcp(self, success, data, sock):
        result = False
        if success:
            result = True
        message = json.dumps({"success": result, "message": data})
        sock.send(message.encode())
    
    def send_udp(self, id, message):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(json.dumps({id: message}), self.udp_addr)
