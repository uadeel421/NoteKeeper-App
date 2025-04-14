from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
# BACKEND_URL = os.getenv('BACKEND_URL', 'http://backend:8000')
#BACKEND_URL = os.getenv('BACKEND_URL', 'http://auth-service:8001')
# ✅ Correct → Routes both /api/signup, /api/login, /api/notes through gateway
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

# API proxy endpoints


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
    # Get token from Authorization header (strip 'Bearer ' if present)
    auth_header = request.headers.get('Authorization', '')
    token = auth_header.replace('Bearer ', '') if auth_header.startswith('Bearer ') else auth_header
    
    if not token:
        return jsonify({'error': 'Authorization token required'}), 401

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    try:
        if request.method == 'POST':
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No data provided'}), 400
                
            response = requests.post(
                f"{BACKEND_URL}/api/notes",
                json=data,
                headers=headers,
                timeout=10  # Add timeout
            )
        else:
            response = requests.get(
                f"{BACKEND_URL}/api/notes",
                headers=headers,
                timeout=10  # Add timeout
            )

        # Handle non-200 responses
        if response.status_code >= 400:
            error_msg = response.json().get('detail', response.text)
            return jsonify({'error': error_msg}), response.status_code

        return jsonify(response.json()), response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Backend request failed: {str(e)}'}), 502
    except ValueError as e:  # JSON decode error
        return jsonify({'error': 'Invalid response from backend'}), 502

        return jsonify(response.json()), response.status_code

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
