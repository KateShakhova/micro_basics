from flask import Flask, request, jsonify
import requests
import uuid
import random

app = Flask(__name__)
messages_service_url = "http://localhost:5001"


@app.route('/', methods=['POST', 'GET'])
def handle_request():
    port = random.randint(2, 4)
    logging_service_url = "http://localhost:500{}".format(port)
    if request.method == 'POST':
        msg = request.json['msg']
        msg_id = str(uuid.uuid4())
        requests.post(logging_service_url, json={'id': msg_id, 'msg': msg})
        return jsonify({'id': msg_id})
    elif request.method == 'GET':
        logging_response = requests.get(logging_service_url).json()
        messages_response = requests.get(messages_service_url).text
        return jsonify({'messages': logging_response, 'additional_message': messages_response})


if __name__ == '__main__':
    app.run(port=5000)

