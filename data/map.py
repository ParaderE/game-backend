from random import choice
from objects import Gates, TradeStation, QuestStation


class Map:
    """class for graph map"""

    def __init__(self):
        self.locations = dict()
        self.secret_locations = list()
    
    def __getitem__(self, key: int):
        """return a location with such key else return a random hidden location"""
        return self.locations.get(key, choice(self.secret_locations))

    def add_location(self, location):
        """add location to the graph map"""
        self.locations[location.number] = location
    
    def connect_locations_with_jump(self, key, *locations):
        """connect locations using jumps"""
        self.locations[key].set_directions(0, *[self.locations[i] for i in locations])
    
    def connect_locations_with_gates(self, key, *locations):
        """connect locations using gates"""
        self.locations[key].set_directions(1, *[self.locations[i] for i in locations])

    def add_secret_location(self, location):
        self.secret_locations.append(location)

    # def update(self, data):
    #     for record in data:
    #         location = self.locations[record['location']]
    #         location.update()

class Location:

    def __init__(self, n,  *objects):
        """initialize a location with """
        self.number = n
        self.objects = {object.number: object for object in objects}
        self.players = list()
    
    def __getitem__(self, key):
        return self.objects[key]
    
    def __delitem__(self, key):
        del self.players[key]

    def update(self, account, coords):
        self.players[account] = {'name': account, 'coords': coords}
        return [(pl['name'], pl['coords']) for pl in self.players.values()]

    def set_directions(self, connection_method: int = 0, *locations):
        """connect locations using given method
        connection_method = 0 -> connection with jump
        connection_method = 1 -> connection with gate
        If connection_method = 1 random free gates are selected for connection
        """
    
    def get_objects(self):
        return [(obj.number, obj.type, obj.coords) for obj in self.objects.values]
    
    @property
    def directions(self) -> dict:
        """return a dict where keys is a connection method and values connected locations"""


graph = Map()

