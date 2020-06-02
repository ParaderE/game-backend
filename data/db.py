import sqlite3


def hash_password(f):
    def wrapper(login, password, *args, **kwargs):
        password = str(hash(password))
        return f(login, password, *args, **kwargs)
    return wrapper


@hash_password
def register(login, password):
    with sqlite3.connect('data/players.db') as conn:
        cur = conn.cursor()
        res = cur.execute(f"""SELECT * FROM Players
                          WHERE name = '{login}' AND password = '{password}'""").fetchall()
        is_free = len(res) == 0
        if is_free:
            cur.execute(f"""INSERT INTO Players (name, password, location, x, y, health)
                        VALUES ('{login}', '{password}', 4, 200, 200, 100);""")
            conn.commit()
    return is_free


@hash_password
def login(login, password):
    with sqlite3.connect('data/players.db') as conn:
        cur = conn.cursor()
        data = cur.execute("""SELECT location, x, y FROM Players
                           WHERE name = '{login}' AND password = '{password}'""").fetchone()
        if not data:
            return False
        return {'location': data[0], 'coords': data[1:]}


@hash_password
def exit(login, password, location, coords):
    with sqlite3.connect('players.db') as conn:
        cur = conn.cursor()
        cur.execute(f"""UPDATE Players SET
                    location = {location},
                    x = {coords[0]}, y = {coords[1]}
                    WHERE name = '{login}' AND password = '{password}'""")
        conn.commit()
    return True
