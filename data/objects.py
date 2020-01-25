import sqlite3


class SpaceObject:

    def __init__(self, coords, number):
        self.coords = coords
        self.number = number


class NPCObjects:

    def __init__(self, name):
        self.name
    
    def get_phrases(self, stage):
        pass


class Player:

    def __init__(self, name):
        self.name = name


class Gates(SpaceObject):
    type = 'gate'

    def __init__(self, coords, number):
        super().__init__(coords)
    
    def link(self, location):
        self.linked_location = location


class TradeStation(SpaceObject):
    type = 'trade_station'

    def __init__(self, coords, number, *npcs):
        super().__init__(coords, number)
        self.npc = dict()

    def __getitem__(self, key):
        return self.npc.get(key, 0)


class QuestStation:
    type = 'quest_station'

    def __init__(self, coords, number, npc):
        super().__init__(coords, number)
        self.npc = npc


class Turret(SpaceObject):
    pass
