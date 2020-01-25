import json
from itertools import islice

from data.map import graph

from flask import Flask, request
app = Flask(__name__)


@app.route("/register/", methods=['POST'])
def register():
	response = {
		"is_free": True 
	}
	account = request.json['account']
	with open('data/players', 'r+') as f:
		if account in f.read():
			response["is_free"] = False
		else:
			f.write(account + '\n')
	return json.dumps(response)


@app.route("/exit/", methods=["POST"])
def exit():
	req = request.json
	account = req['account']
	coords = req['coords']
	# save player data to json file
	return ""


@app.route("/a/", methods=["POST"])
def update_position():
	req = request.json
	account = req['account']
	location = req['location']
	location_num = location['num']
	coords = location['coords']

	player = {
		'name': '',
		'coords': []}
	response = {
		'players': []
	}

	location = graph[location_num]
	players = location.update(account, coords)
	for player in players:
		response['players'].append({'name': player.name, 'coords': player.coords})

	return json.dumps(response)


@app.route("/stations/", method=["POST"])
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

@app.route("/jump/gates/", method=["POST"])
def gate_jump():
	req =  request.json
	account = req['account']
	location_num = req['location']
	gate = req['object']
	location = graph[location_num]
	del location[account]
	response = {
		'location': graph[location_num][gates].get_location()
	}
	return json.dumps(response)

@app.route("/jump/just/", method=["POST"])
def just_jump():
	req =  request.json
	location = req['location']
	new_location_num = req['new_location']
	new_location = graph[new_location_num]
	response = {
		'location': new_location_num
		'objects': new_location.get_objects()
	}
	return json.dumps(response)


if __name__ == "__main__":
	app.run(port=5000)