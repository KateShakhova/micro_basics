from flask import Flask, jsonify
from hazelcast import HazelcastClient
import sys


port = int(sys.argv[1])
app = Flask(__name__)


messages = []


def on_message(message):
    msg = message.item
    messages.append(msg)
    msg_queue.remove(msg)
    print("Received message: {}".format(msg))


@app.route('/', methods=['GET'])
def handle_request():
    return jsonify(messages)


if __name__ == '__main__':
    client = HazelcastClient()
    msg_queue = client.get_queue("messages")
    msg_queue.add_listener(include_value=True, item_added_func=on_message)
    app.run(port=port)
