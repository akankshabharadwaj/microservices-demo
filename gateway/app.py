from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/create-order', methods=['POST'])
def create_order():
    response = requests.post(
        "http://order-service:5001/order",
        json=request.json
    )
    return jsonify(response.json())

@app.route('/')
def home():
    return "Gateway running"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)