from flask import request
from flask import jsonify
from flask import Flask
#just trying my hands on flask server
app = Flask(__name__)

@app.route('/hello',methods=['POST'])
def hello():
	message = request.get_json(force=True)
	name = message['name']
	response = {
		'greeting': 'Hello , ' + name + '!'
	}
	return jsonify(response)
