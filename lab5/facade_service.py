from flask import Flask, request, jsonify
import requests
import uuid
import random
from hazelcast import HazelcastClient
import sys
import consul


port = int(sys.argv[1])
try:
    address = sys.argv[2]
except IndexError:
    address = "127.0.0.1"
app = Flask(__name__)


def register_service(address, port):
    service_id = str(uuid.uuid4())
    c.agent.service.register(name="facade service",
                             service_id=service_id,
                             address=address,
                             port=port)


def get_service(name):
    services = c.catalog.service(name)[1]
    urls = []
    for service in services:
        service_address = service['ServiceAddress']
        service_port = service['ServicePort']
        url = "http://{}:{}".format(service_address, service_port)
        urls.append(url)
    return urls


def set_map_queue():
    if c.kv.get("map")[1] is None:
        c.kv.put("map", "logging")
    if c.kv.get("queue")[1] is None:
        c.kv.put("queue", "messages")


@app.route('/', methods=['POST', 'GET'])
def handle_request():
    client = HazelcastClient()
    queue_name = c.kv.get("queue")[1]['Value'].decode()
    msg_queue = client.get_queue(queue_name).blocking()
    logging_service_url = random.choice(get_service("logging service"))
    messages_service_url = random.choice(get_service("messages service"))
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
    c = consul.Consul()
    set_map_queue()
    register_service(address, port)
    app.run(port=port, host=address)
