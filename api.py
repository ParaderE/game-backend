import sqlite3

from data.map import graph

from flask import Flask, request
app = Flask(__name__)


@app.route("/")
def home():
	return "running"


@app.route("/register/", methods=['POST'])
def register():
	response = {
		"is_free": True,
		'location': {
			'num': 4,
			'coords': [200, 200]
		}
	}
	req = request.json
	account = req['account']
	login = account['login']
	password = account['password']
	graph[4].update(login + " " + password, (200, 200))
	with sqlite3.connect('players.db') as con:
		cur = con.cursor()
		res = cur.execute(f"SELECT * FROM Players WHERE name={login} AND password={password}").fetchall()
		is_free = len(res) == 0
		response['is_free'] = is_free
		if is_free:
			cur.execute(f"""INSERT INTO Players (name, password, location, x, y, health)
						VALUES ({login}, {password}, {4}, {200}, {200}, {100});""")
		con.commit()
	return response


@app.route("/enter/", methods=['POST'])
def enter():
	req = request.json
	account = req['account']
	login = account['login']
	password = account['password']

	with sqlite3.connect('players.db') as con:
		cur = con.cursor()
		res = cur.execute(f"SELECT location, x, y FROM Players WHERE name={login} AND password={password}").fetchall()

	response = {
		'location': {
			'num': res[0][0],
			'coords': res[0][1:]
		}
	}
	return response

@app.route('/objects/', methods=["POST"])
def get_objects():
	req = request.json
	location = req['location']
	location_num = location['num']

	location = graph[location_num]
	response = {
		'objects': location.get_objects()
	}

	return response


@app.route("/exit/", methods=["POST"])
def exit():
	req = request.json
	account = req['account']
	login = account['login']
	password = account['password']

	location = req['location']
	location_num = location['num']
	coords = location['coords']

	del graph[location_num][login + " " + password]
	with sqlite3.connect('players.db') as con:
		cur = con.cursor()
		cur.execute(f"""UPDATE Players
		location = {location_num},
		x = {coords[0]}, y = {coords[1]}
		WHERE name = {login} AND password = {password}""")
		con.commit()
	return ""


@app.route("/update/", methods=["POST"])
def update_position():
	req = request.json
	account = req['account']
	location = req['location']
	location_num = location['num']
	coords = location['coords']

	response = {
		'players': []
	}

	location = graph[location_num]
	response['players'] = [{'name': player.name, 'coords': player.coords} for player in location.update(account, coords)]

	return response


@app.route("/stations/", methods=["POST"])
def get_station_data():
	req =  request.json
	location = req['location']
	station = req['object']
	npc = req.get('npc', 0)
	if not npc:
		response = graph[location][station].get_npc()
	else:
		response = graph[location][station][npc].get_phrases()
	return response


@app.route("/jump/gates/", methods=["POST"])
def gate_jump():
	req =  request.json
	account = req['account']
	location_num = req['location']
	gate = req['object']
	location = graph[location_num]
	del location[account]
	new_location = graph[location_num][gate].get_location()
	response = {
		'location': new_location,
		'objects': graph[new_location].get_objects()
	}
	return response


@app.route("/jump/just/", methods=["POST"])
def just_jump():
	req =  request.json
	account = req['account']
	location_num = req['location']
	new_location_num = req['new_location']
	new_location = graph[new_location_num]
	location = graph[location_num]
	del location[account]
	response = {
		'location': new_location_num,
		'objects': new_location.get_objects()
	}
	return respons
 

if __name__ == "__main__":
	app.run(port=5000)