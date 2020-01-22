import json

from flask import Flask, request
app = Flask(__name__)

@app.route("/", methods=['POST'])
def home():
	return request.json
