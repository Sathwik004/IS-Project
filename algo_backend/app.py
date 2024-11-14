from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import base64
import binascii
import re
import json

from algo import generate_keys, encrypt, decrypt

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

app.secret_key = 'your_secret_key'  # Set a secret key for sessions

# MongoDB connection string

def correct_base64_padding(base64_string):
    # Add necessary padding to the Base64 string
    missing_padding = len(base64_string) % 4
    if missing_padding:
        base64_string += '=' * (4 - missing_padding)
    return base64_string

def is_base64(s):
    try:
        if isinstance(s, str):
            # If it’s a string, decode to bytes, then try to decode back to string
            return base64.b64encode(base64.b64decode(s)).decode() == s
        else:
            # If it's bytes, try to decode it
            return base64.b64encode(base64.b64decode(s)).decode() == s.decode()
    except Exception:
        return False

def convert_to_base64(data):
    """Convert a bytes-like object to a base64 string."""
    return base64.b64encode(data).decode('utf-8')

@app.route('/hello', methods=['GET'])
def hello():
    return "Hello, World!"

@app.route('/generate_keys', methods=['GET'])
def generate_keys_endpoint():
    try:
        private_key, public_key, unimodular_matrix, uni_inv1, uni_inv2 = generate_keys(10)
        
        
        # # Convert keys to base64 for easier transmission over JSON
        # if isinstance(unimodular_matrix, list):
        #     unimodular_matrix = np.array(unimodular_matrix)
        # if isinstance(uni_inv1, list):
        #     uni_inv = np.array(uni_inv1)
        # if isinstance(uni_inv2, list):
        #     uni_inv = np.array(uni_inv2)

        # Convert keys to base64 for easier transmission over JSON
        keys = {
            'private_key': base64.b64encode(private_key.tobytes()).decode('utf-8'),
            'public_key': base64.b64encode(public_key.tobytes()).decode('utf-8'),
            'unimodular_matrix': base64.b64encode(unimodular_matrix.tobytes()).decode('utf-8'),
            'uni_inv1': base64.b64encode(uni_inv1.tobytes()).decode('utf-8'),
            'uni_inv2': base64.b64encode(uni_inv2.tobytes()).decode('utf-8')
        }

        # Decode the base64-encoded strings back to bytes
        decoded_public_key_bytes = base64.b64decode(keys['public_key'])
        decoded_uni_inv1_bytes = base64.b64decode(keys['uni_inv1'])
        decoded_uni_inv2_bytes = base64.b64decode(keys['uni_inv2'])

        # Convert the bytes back to numpy arrays
        decoded_public_key = np.frombuffer(decoded_public_key_bytes, dtype=public_key.dtype)
        print(uni_inv1.dtype)
        print(uni_inv2.dtype)
        print(private_key.dtype)
        decoded_uni_inv1 = np.frombuffer(decoded_uni_inv1_bytes, dtype=uni_inv1.dtype)
        decoded_uni_inv2 = np.frombuffer(decoded_uni_inv2_bytes, dtype=uni_inv2.dtype)

        # Print the decoded arrays
        print("Decoded Public Key:", decoded_public_key)
        print("Decoded Uni Inv1:", decoded_uni_inv1)
        print("Decoded Uni Inv2:", decoded_uni_inv2)

        
        # for i in range(0,len(arr),10):
        #     print(arr[i:i+10])
        return {"success": True, "keys": keys},200
    except Exception as e:
        return {"error": str(e)}, 500



@app.route('/encrypt', methods=['POST'])
def encrypt_endpoint():
    data = request.json
    print(data)
    
    plaintext = data['message']
    public_key = data['public_key']

    
    # Decode the Base64 strings
    try:
        public_key = base64.b64decode(public_key)
        public_key = np.frombuffer(public_key, dtype=np.float64).reshape((10, 10))
    except binascii.Error as e:
        return jsonify({'error': 'Failed to extract public key ' + str(e)}), 400

    

    # Encrypt the plaintext
    print(plaintext,public_key)
    encrypted_text = encrypt(plaintext, public_key)
    print(type(encrypted_text))
    print(type(public_key))

    encrypted_text = base64.b64encode(encrypted_text.tobytes()).decode('utf-8')
    print(encrypted_text)

    return jsonify({'encrypted_text': encrypted_text}), 200


@app.route('/decrypt', methods=['GET'])
def decrypt_endpoint():
    data = request.args
    
    encrypted_text = data.get('encrypted_text')
    private_key = data.get('private_key')
    uni_upper = data.get('uni_upper')
    uni_lower = data.get('uni_lower')

    print("\n\n in decrypt")
    print(encrypted_text)
    # Decode the Base64 strings with error handling
    try:
        encrypted_text = base64.b64decode(encrypted_text)
        private_key = base64.b64decode(private_key)
        uni_upper = base64.b64decode(uni_upper)
        uni_lower = base64.b64decode(uni_lower)
    except binascii.Error as e:
        return jsonify({'error': 'Base64 decoding failed: ' + str(e)}), 400

    # Reshape keys from bytes back into matrices
    
    try:
        encrypted_text = np.frombuffer(encrypted_text, dtype=np.float64)
        private_key = np.frombuffer(private_key, dtype=np.float64).reshape((10, 10))
        uni_upper = np.frombuffer(uni_upper, dtype=np.int64).reshape((10, 10))
        uni_lower = np.frombuffer(uni_lower, dtype=np.int64).reshape((10, 10))
    except ValueError as e:
        print("Reshaping failed")
        return jsonify({'error': 'Reshaping matrices failed: ' + str(e)}), 400

    
    print(encrypted_text)

    # Decrypt the ciphertext
    print("\n\n\n\n")
    print(encrypted_text)
    decrypted_text = "Decrypted text"
    try:
        decrypted_text = decrypt(encrypted_text, private_key, uni_inv_upper=uni_upper, uni_inv_lower=uni_lower)
        print(decrypted_text)
    except Exception as e:
        print("Execption",e)
        return jsonify({'error': 'Decryption failed: ' + str(e)}), 400

    return jsonify({'decrypted_text': decrypted_text}), 200



if __name__ == '__main__':
    app.run(debug=True, port=5001)