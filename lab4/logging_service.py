from flask import Flask, request, jsonify
from hazelcast import HazelcastClient
import os
import sys
import subprocess
import threading


port = int(sys.argv[1])
app = Flask(__name__)

hazelcast_path = "D:\\hazelcast\\bin"
os.environ['PATH'] = os.environ['PATH'] + hazelcast_path


@app.route('/', methods=['POST', 'GET'])
def handle_request():
    client = HazelcastClient()
    messages = client.get_map('logging').blocking()
    if request.method == 'POST':
        msg_id = request.json['id']
        msg = request.json['msg']
        messages.put(msg_id, msg)
        print(f"Received message: {msg}")
        return jsonify({'status': 'success'})
    elif request.method == 'GET':
        return jsonify(list(messages.values()))


if __name__ == '__main__':
    logging_th = threading.Thread(target=app.run, kwargs={'debug': False, 'port': port})
    hazelcast_th = threading.Thread(target=subprocess.run, args=['hz-start.bat'])
    logging_th.start()
    hazelcast_th.start()
