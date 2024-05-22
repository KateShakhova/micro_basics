from flask import Flask, jsonify
from hazelcast import HazelcastClient
import sys
import consul
import uuid


port = int(sys.argv[1])
try:
    address = sys.argv[2]
except IndexError:
    address = "127.0.0.1"
app = Flask(__name__)


messages = []


def register_service(address, port):
    service_id = str(uuid.uuid4())
    c.agent.service.register(name="messages service",
                             service_id=service_id,
                             address=address,
                             port=port)


def on_message(message):
    msg = message.item
    messages.append(msg)
    msg_queue.remove(msg)
    print("Received message: {}".format(msg))


@app.route('/', methods=['GET'])
def handle_request():
    return jsonify(messages)


if __name__ == '__main__':
    c = consul.Consul()
    register_service(address, port)
    client = HazelcastClient()
    queue = c.kv.get("queue")[1]['Value'].decode()
    msg_queue = client.get_queue(queue)
    msg_queue.add_listener(include_value=True, item_added_func=on_message)
    app.run(port=port, host=address)
