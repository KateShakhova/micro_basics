from flask import Flask, request, jsonify
from hazelcast import HazelcastClient
import os
import sys
import subprocess
import threading
import consul
import uuid


port = int(sys.argv[1])
try:
    address = sys.argv[2]
except IndexError:
    address = "127.0.0.1"
app = Flask(__name__)

hazelcast_path = "D:\\hazelcast\\bin"
os.environ['PATH'] = os.environ['PATH'] + hazelcast_path


def register_service(address, port):
    service_id = str(uuid.uuid4())
    c.agent.service.register(name="logging service",
                             service_id=service_id,
                             address=address,
                             port=port)


@app.route('/', methods=['POST', 'GET'])
def handle_request():
    client = HazelcastClient()
    logging_map = c.kv.get("map")[1]['Value'].decode()
    messages = client.get_map(logging_map).blocking()
    if request.method == 'POST':
        msg_id = request.json['id']
        msg = request.json['msg']
        messages.put(msg_id, msg)
        print(f"Received message: {msg}")
        return jsonify({'status': 'success'})
    elif request.method == 'GET':
        return jsonify(list(messages.values()))


if __name__ == '__main__':
    c = consul.Consul()
    register_service(address, port)
    logging_th = threading.Thread(target=app.run, kwargs={'debug': False, 'port': port, 'host': address})
    hazelcast_th = threading.Thread(target=subprocess.run, args=['hz-start.bat'])
    logging_th.start()
    hazelcast_th.start()
