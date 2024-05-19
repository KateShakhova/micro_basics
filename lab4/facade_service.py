from flask import Flask, request, jsonify
import requests
import uuid
import random
from hazelcast import HazelcastClient


app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def handle_request():
    client = HazelcastClient()
    msg_queue = client.get_queue("messages").blocking()
    log_port = random.randint(1, 3)
    msg_port = random.randint(4, 5)
    logging_service_url = "http://localhost:500{}".format(log_port)
    messages_service_url = "http://localhost:500{}".format(msg_port)
    if request.method == 'POST':
        msg = request.json['msg']
        msg_id = str(uuid.uuid4())
        requests.post(logging_service_url, json={'id': msg_id, 'msg': msg})
        msg_queue.offer(msg)
        return jsonify({'id': msg_id})
    elif request.method == 'GET':
        logging_response = requests.get(logging_service_url).json()
        messages_response = requests.get(messages_service_url).text
        return jsonify({'messages': logging_response, 'additional_message': messages_response})


if __name__ == '__main__':
    app.run(port=5000)

