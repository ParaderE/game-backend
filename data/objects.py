import sqlite3 as sql

class SpaceObject:

    def __init__(self, coords, number):
        self.coords = coords
        self.number = number


class NPCObjects:

    def __init__(self, name):
        self.name = name
    
    def get_phrase(self, stage):
        with sql.connect('npc.db') as con:
            cur = con.cursor()
            phrase = cur.execute(f"""SELECT phrase FROM phrases
            WHERE npc = {self.name} AND stage = {stage}""").fetchone()
        return phrase


class TradeNPC(NPCObjects):

    def __init__(self, name):
        self.name = name
    
    def get_phrase(self):
        return super().get_phrase(0)


class Player:

    def __init__(self, name):
        self.name = name


class Gate(SpaceObject):
    type = 'gate'

    def link(self, location):
        self.linked_location = location
    
    def get_location(self):
        return self.linked_location


class TradeStation(SpaceObject):
    type = 'trade_station'

    def __init__(self, coords, number, *npcs):
        super().__init__(coords, number)
        self.npc = dict()

    def __getitem__(self, key):
        return self.npc.get(key, 0)


class QuestStation(SpaceObject):
    type = 'quest_station'

    def __init__(self, coords, number):
        super().__init__(coords, number)
    
    def add_npc(self, npc):
        self.npc = npc


class Turret(SpaceObject):
    type = 'turret'

    def __init__(self, coords, number):
        super().__init__(coords, number)
