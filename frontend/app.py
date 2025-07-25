from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
BACKEND_URL = os.getenv('BACKEND_URL', 'http://api-gateway:8000')


@app.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        return redirect(url_for('api_signup'))
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('api_login'))
    return render_template('login.html')


@app.route('/notes', methods=['GET', 'POST'])
def notes():
    if request.method == 'POST':
        return redirect(url_for('api_notes'))
    return render_template('notes.html')


@app.route('/logout')
def logout():
    return redirect(url_for('index'))


# ========== API proxy endpoints ==========

@app.route('/api/signup', methods=['POST'])
def api_signup():
    data = request.get_json()
    response = requests.post(f"{BACKEND_URL}/api/signup", json=data)
    return jsonify(response.json()), response.status_code


@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    response = requests.post(f"{BACKEND_URL}/api/login", json=data)
    return jsonify(response.json()), response.status_code


@app.route('/api/notes', methods=['GET', 'POST'])
def api_notes():
    auth_header = request.headers.get('Authorization')
    token = auth_header.split(" ", 1)[1] if auth_header and auth_header.startswith("Bearer ") else request.cookies.get('token')
    headers = {'Authorization': f'Bearer {token}'} if token else {}

    try:
        if request.method == 'POST':
            data = request.get_json()
            response = requests.post(f"{BACKEND_URL}/api/notes", json=data, headers=headers)
        else:
            response = requests.get(f"{BACKEND_URL}/api/notes", headers=headers)

        if 'application/json' not in response.headers.get('Content-Type', ''):
            return jsonify({'error': 'Invalid response from server'}), 500

        return jsonify(response.json()), response.status_code

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    auth_header = request.headers.get('Authorization')
    token = auth_header.split(" ", 1)[1] if auth_header and auth_header.startswith("Bearer ") else request.cookies.get('token')
    headers = {'Authorization': f'Bearer {token}'} if token else {}

    try:
        response = requests.delete(f"{BACKEND_URL}/api/notes/{note_id}", headers=headers)

        if 'application/json' not in response.headers.get('Content-Type', ''):
            return jsonify({'error': 'Invalid response from server'}), 500

        return jsonify(response.json()), response.status_code

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
