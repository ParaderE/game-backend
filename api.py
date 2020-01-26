import json

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
			'location_num': 4,
			'coords': [200, 200]
		}
	}
	req = request.json
	account = req['account']
	graph[4].update(account, (200, 200))
	with open('data/players', 'r+') as f, open('data/players_coords.json', 'r+') as json_f:
		if account in f.read():
			response["is_free"] = False
			response['location'] = None
		else:
			f.write(account + '\n')
			data = json.load(json_f)
			data[account] = [4, [200, 200]]
			json_f.seek(0)
			json.dump(data, json_f)
	return response


@app.route("/enter/", methods=['POST'])
def enter():
	req = request.json
	account = req['account']
	with open('data/players_coords.json') as f:
		location, coords = json.load(f)[account]
	response = {
		'location': {
			'num': location,
			'coords': coords
		}
	}
	return response


@app.route("/exit/", methods=["POST"])
def exit():
	req = request.json
	account = req['account']
	location = req['location']
	location_num = location['num']
	coords = location['coords']
	del graph[location_num][account]
	with open('data/players_coords.json', 'r+') as json_f:
		data = json.load(json_f)
		data[account] = [location_num, coords]
		json_f.seek(0)
		json.dump(data, json_f)
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
	players = location.update(account, coords)
	for player in players:
		response['players'].append({'name': player.name, 'coords': player.coords})

	return json.dumps(response)


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
	return json.dumps(response)


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
	return json.dumps(response)


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
	return json.dumps(response)


if __name__ == "__main__":
	app.run(port=5000)