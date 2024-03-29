from flask import Flask, request, jsonify

app = Flask(__name__)
messages = {}

@app.route('/', methods=['POST', 'GET'])
def handle_request():
    if request.method == 'POST':
        msg_id = request.json['id']
        msg = request.json['msg']
        messages[msg_id] = msg
        print(f"Received message: {msg}")
        return jsonify({'status': 'success'})
    elif request.method == 'GET':
        return jsonify(list(messages.values()))

if __name__ == '__main__':
    app.run(port=5001)
