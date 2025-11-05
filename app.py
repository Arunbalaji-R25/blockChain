from flask import Flask, render_template, jsonify, request
from blockchain import Blockchain
from rsa_utils import generate_keys, sign_message, verify_signature, export_public_key
import hashlib

app = Flask(__name__)
blockchain = Blockchain()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_data', methods=['POST'])
def add_data():
    data = request.json.get('data')
    if not data:
        return jsonify({"error": "No data received"}), 400

    # Generate RSA keys
    private_key, public_key = generate_keys()

    # Hash message
    data_hash = hashlib.sha256(data.encode()).hexdigest()

    # Sign message hash
    signature = sign_message(private_key, data_hash)

    # Verify to show it's valid
    verification = verify_signature(public_key, data_hash, signature)

    block_data = {
        "message": data,
        "hash": data_hash,
        "signature": signature,
        "public_key": export_public_key(public_key),
        "verified": verification
    }

    block = blockchain.add_block(block_data)

    response = {
        "message": "✅ Block added successfully!",
        "block": block.__dict__
    }
    return jsonify(response)

@app.route('/get_chain')
def get_chain():
    chain_data = [block.__dict__ for block in blockchain.chain]
    return jsonify(chain_data)

if __name__ == '__main__':
    app.run(debug=True)
