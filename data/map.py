from objects import Gate, TradeStation, QuestStation, Turret


class Map:
    """class for graph map"""

    def __init__(self):
        self.locations = dict()
    
    def __getitem__(self, key: int):
        """return a location with such key else return a random hidden location"""
        return self.locations[key]

    def add_location(self, location):
        """add location to the graph map"""
        self.locations[location.number] = location


class Location:

    def __init__(self, n):
        """initialize a location with """
        self.number = n
        self.players = dict()
    
    def __getitem__(self, key):
        return self.objects[key]
    
    def __delitem__(self, key):
        del self.players[key]

    def update(self, account, coords):
        """update players coords on the location"""
        self.players[account] = {'name': account, 'coords': coords}
        return [(pl['name'], pl['coords']) for pl in self.players.values()]
    
    def add_objects(self, *objects):
        self.objects = {object.number: object for object in objects}
    
    def get_objects(self):
        return [(obj.number, obj.type, obj.coords) for obj in self.objects.values]


graph = Map()
[graph.add_location(Location(i)) for i in range(1, 11)]

#%% Location 4 
graph[4].add_objects(
    Gate((340, 50), 1),
    Gate((320, 380), 2),
    TradeStation((205, 190), 3),
    QuestStation((160, 160), 4)
)
graph[4][1].link(9)
graph[4][2].link(6)
###
#%% Location 1
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
#%% Location 6
graph[6].add_objects(
    Gate((100, 100), 1),
    Gate((376, 99), 2)
)
graph[6][1].link(4)
graph[6][2].link(10)
###
#%% location 10
graph[10].add_objects(
    Gate((100, 100), 1),
    Gate((376, 99), 2)
)
graph[10][1].link(6)
graph[10][2].link(9)
###
#%% Location 9
graph[9].add_objects(
    Gate((276, 199), 1),
)
graph[9][1].link(10)
###