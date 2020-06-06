from .objects import Gate, TradeStation, QuestStation, Turret
import uuid
from .player import Player


class Map:

    def __init__(self):
        self.locations = {}
        self.players = {}

    def __getitem__(self, key):
        return self.locations[key]

    def create_location(self, id):
        self.locations[identifier] = Location(id)

    def register(self, addr, udp_port):
        player = Player(addr, udp_port)
        self.players[player.id] = player
        
        return player
    
    def join(self, id, location_id):
        player = self.players[id]
        self.players[id] = player

        self.locations[location_id].players.append(player)
    
    def leave(self, id, location_id):
        player = self.players[id]

        self.locations[location_id].leave(player)

    def update(self, identifier, location_id, data, sock):
        location = self.rooms[location_id]
        player = self.players[identifier]
        player.coords[0] += data[0]
        player.coords[1] += data[1]
        for player in location.players:
            if player.identifier != identifier:
                player.send_udp(
                    identifier,
                    {"players": [{"name": player.login, "coords": player.coords} for player in location.players]}
                )


class Location:

    def __init__(self, identifier):
        self.players = []
        self.objects = dict()
        self.identifier = identifier
    
    def add_objects(self, object):
        self.objects[object.id] = object

    def __getitem__(self, key):
        return self.objects[key]

    def join(self, player):
        self.players.append(player)

    def leave(self, player):
        if player in self.players:
            self.players.remove(player)
    
    def is_in_location(self, id):
        for player in self.players:
            if player.id == id:
                return True
        return False


graph = Map()
[graph.create_location(Location(i)) for i in range(1, 11)]

# Location 4 
graph[4].add_objects(
    Gate((120, 50), 1),
    Gate((340, 380), 2),
    TradeStation((15, 67), 3),
    QuestStation((160, 392), 4)
)
graph[4][1].link(9)
graph[4][2].link(6)
###
# Location 1
graph[1].add_objects(
    Gate((20, 376), 1),
    Turret((20, 20), 2),
    Turret((100, 100), 3),
    Turret((180, 180), 4),
    Turret((260, 260), 5),
    Turret((340, 340), 6)
)
graph[1][1].link(8)
###
# Location 6
graph[6].add_objects(
    Gate((100, 100), 1),
    Gate((376, 99), 2)
)
graph[6][1].link(4)
graph[6][2].link(10)
###
# location 10
graph[10].add_objects(
    Gate((100, 100), 1),
    Gate((376, 99), 2)
)
graph[10][1].link(6)
graph[10][2].link(9)
###
# Location 9
graph[9].add_objects(
    Gate((276, 199), 1),
)
graph[9][1].link(10)
###