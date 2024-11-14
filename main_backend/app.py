from flask import Flask, request, jsonify, session
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

app.secret_key = 'your_secret_key'  # Set a secret key for sessions


# MongoDB connection string
load_dotenv()  # Load environment variables from .env file

app.config["MONGO_URI"] = os.getenv("MONGO_URI")
client = MongoClient(app.config["MONGO_URI"])
db = client['my_database']
users_collection = db['users']
emails_collection = db['emails']


def check_database_connection():
    try:
        # Perform a simple operation to check the connection
        db.list_collection_names()
        print("Database connection successful!")
    except Exception as e:
        print("Database connection failed:", str(e))


@app.route('/register', methods=['POST'])
def register():
    try:
        username = request.json['username']
        email = request.json['email']
        password = request.json['password']
        public_key = request.json['public_key']
        
        # Check if user already exists
        if users_collection.find_one({'email': email}):
            return jsonify({"message": "User already exists!"}), 409
        
        if not public_key or public_key.strip() == '':  # Check if public key is empty
            return jsonify({"message": "Public key is required"}), 400

        # Hash the password
        hashed_password = generate_password_hash(password)
        
        # Store user details along with generated keys
        users_collection.insert_one({
            'username': username,
            'email': email,
            'password': hashed_password,
            'pkey': public_key
        })

        return jsonify({"message": "User registered successfully!", "userId" : email}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Registration failed", "error": str(e)}), 500


@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        print(username,password)
        
        # Find the user by email
        user = users_collection.find_one({'username': username})
        if user and check_password_hash(user['password'], password):
            session['username'] = user['username']  # Save username in session
            userId = user['email']
            return jsonify({"success": True, "message": "Login successful!", "userId": userId}), 200
        
        else:
            return jsonify({"message": "Invalid credentials!"}), 401
    except Exception as e:
        return jsonify({"message": "Login failed", "error": str(e)}), 500
    

@app.route('/get_public_key', methods=['GET'])
def get_public_key():
    email = request.args.get('email')
    if email:
        user = db.users.find_one({'email': email}, {'pkey': 1})
        if user:
            return jsonify({"public_key": user['pkey']}), 200
        return jsonify({"message": "User not found"}), 404
    return jsonify({"message": "Email is required"}), 400

@app.route('/send_email', methods=['POST'])
def send_email():
    try:
        data = request.get_json()
        email = data.get('reveiver')
        subject = data.get('subject')
        encrypted_email_body = data.get('body')
        sender = data.get('sender')

        print(data)

        if not email or not subject or not encrypted_email_body:
            print(email, subject)
            return jsonify({"message": "Email, subject, and encrypted email body are required"}), 400

        email_data = {
            'sender': sender,
            'reveiver': email,
            'subject': subject,
            'body': encrypted_email_body
        }

        emails_collection.insert_one(email_data)
        return jsonify({"message": "Email stored successfully!"}), 200
    except Exception as e:
        return jsonify({"message": "Failed to store email", "error": str(e)}), 500
  

@app.route('/fetch_emails', methods=['GET'])
def fetchEmails():
    try:
        email = request.args.get('email')
        if email:
            emails = emails_collection.find({'reveiver': email}, {'_id': 0, 'sender': 1, 'subject': 1, 'body': 1})
            print(emails)
            return jsonify({"emails": list(emails)}), 200
        return jsonify({"message": "Email is required"}), 400
    except Exception as e:
        return jsonify({"message": "Failed to fetch emails", "error": str(e)}), 500

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return jsonify({"message": "Logged out successfully!"}), 200


# @app.route('/protected', methods=['GET'])
# def protected():
#     if 'username' in session:
#         return jsonify({"message": f"Welcome, {session['username']}!"}), 200
#     else:
#         return jsonify({"message": "Unauthorized access!"}), 401


if __name__ == "__main__":
    check_database_connection()
    app.run(debug=True, port=5000)