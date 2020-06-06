import socket
import json
from threading import Thread, Lock
from os import environ

from data.map import graph
from data import db


class TcpServer(Thread):

    def __init__(self, port, locations, lock):
        Thread.__init__(self)
        self.lock = lock
        self.tcp_port = int(port)
        self.locations = locations
        self.is_listening = True
        self.msg = {"succes": None, "message": None}

    def run(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('0.0.0.0', self.tcp_port))
        self.sock.setblocking(0)
        self.sock.settimeout(5)
        self.sock.listen(1)

        while self.is_listening:

            try:
                conn, addr = self.sock.accept()
            except socket.timeout:
                continue

            data = conn.recv(1024)
            try:
                data = json.loads(data)

                action = data['action']
                payload = data['payload']
                identifier = data.get('identifier', None)

                self.lock.acquire()
                try:
                    self.route(
                        conn,
                        addr,
                        action,
                        payload,
                        identifier,
                    )
                finally:
                    self.lock.release()
            except KeyError:
                conn.send("Json is invalid")
            except ValueError:
                conn.send("Message is not a valid json string")

            conn.close()

        self.stop()
    
    def route(self, sock, addr, action, payload, identifier=None):

        if action == "register":
            user = payload['user']

            client = self.locations.register(addr, int(payload['port']), user['login'])
            if not db.register(user['login'], user['password']):
                client.send_tcp(False, "User exist", sock)
                return 0
            response = {
                "id": client.id,
                "position": {
                    "location": 4,
                    "coords": [200, 200]
                }
            }
            self.locations.join(client.id, 4)
            client.send_tcp(True, response, sock)
            return 0

        elif action == "enter":
            user = payload['user']

            client = self.locations.register(addr, int(payload['port']), user['login'])
            position = db.login(user['login'], user['password'])
            if not position:
                client.send_tcp(False, "User not found", sock)
                return 0
            response = {
                "id": client.id,
                "position": position
            }
            self.locations.join(client.id, position['location'])
            client.send_tcp(True, response, sock)
            return 0
        
        if identifier is not None:

            client = self.locations.players[identifier]

            if action == "get":
                target = payload['target']

                if target == "all":
                    data = tuple(map(lambda x: x.json(), self.locations[client.location].objects.values()))
                elif target.isdigit():
                    target = int(target)
                    if target in self.locations[client.location]:
                        data = self.locations[client.location].objects[target].json()
                    else:
                        client.send_tcp(False, "Object not found", sock)
                        return 0
                client.send_tcp(True, data, sock)
                return 0
                
            elif action == "join":
                location_id = payload['location_id']
                self.locations.leave(client, client.location)
                client.location = location_id
                self.locations.join(client, location_id)
                client.send_tcp(True, location_id, sock)
            elif action == 'leave':
                user = payload['user']
                db.exit(user['login'], user['password'], client.location, client.coords)
                self.locations.leave(identifier, client.location)

    def stop(self):
        self.sock.close()
    

class UdpServer(Thread):

    def __init__(self, udp_port, rooms, lock):
        Thread.__init__(self)
        self.lock = lock
        self.udp_port = int(udp_port)
        self.locations = rooms
        self.is_listening = True
        self.msg = {"success": None, "message": None}

    def run(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('0.0.0.0', self.udp_port))
        self.sock.setblocking(0)
        self.sock.settimeout(5)

        while self.is_listening:

            try:
                data, address = self.sock.recvfrom(1024)
            except socket.timeout:
                continue

            try:
                data = json.loads(data)

                identifier = data.get('identidier', None)
                payload = data.get('payload', None)
                action = data.get('action', None)

                self.lock.acquire()
                try:
                    if action == "update":
                        self.locations.update(identifier, payload, self.sock)
                finally:
                    self.lock.release()
            except Exception:
                pass
        self.stop()

    def stop(self):
        self.sock.close()		


def main_loop(tcp_port, udp_port, rooms):
    lock = Lock()

    udp_server = UdpServer(udp_port, rooms, lock)
    tcp_server = TcpServer(tcp_port, rooms, lock)

    udp_server.start()
    tcp_server.start()

    is_running = True

    while is_running:
        if False:
            udp_server.is_listening = False
            tcp_server.is_listening = False
            is_running = False
    
    udp_server.join()
    tcp_server.join()


if __name__ == "__main__":
    main_loop(environ.get("PORT", 33500), environ.get("PORT", 33500), graph)
