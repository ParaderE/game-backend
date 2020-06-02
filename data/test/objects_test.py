from ..objects import Moving

def moving_test():
    coords = (12, 12)
    move = Moving(coords)
    move.update((-2, -2))
    assert move.coords == (10, 10)
