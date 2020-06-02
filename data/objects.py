import sqlite3 as sql

class SpaceObject:

    def __init__(self, coords, id):
        self.coords = coords
        self.id = id


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


class Gate(SpaceObject):
    type = 'gate'

    def link(self, location):
        self.linked_location = location
    
    def get_location(self):
        return self.linked_location


class TradeStation(SpaceObject):
    type = 'trade_station'

    def __init__(self, coords, id, *npcs):
        super().__init__(coords, id)
        self.npc = dict()

    def __getitem__(self, key):
        return self.npc.get(key, 0)


class QuestStation(SpaceObject):
    type = 'quest_station'

    def __init__(self, coords, id):
        super().__init__(coords, id)
    
    def add_npc(self, npc):
        self.npc = npc


class Turret(SpaceObject):
    type = 'turret'

    def __init__(self, coords, number):
        super().__init__(coords, number)
