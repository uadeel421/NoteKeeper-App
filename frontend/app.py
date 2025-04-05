from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)
BACKEND_URL = os.getenv('BACKEND_URL', 'http://backend:8000')

@app.route('/', methods=['GET', 'POST'])
def index():
    notes = []
    try:
        if request.method == 'POST':
            note = request.form.get('note')
            if note:
                try:
                    requests.post(f"{BACKEND_URL}/notes", 
                                json={'note': note},
                                timeout=5)
                except requests.exceptions.RequestException as e:
                    app.logger.error(f"Failed to create note: {str(e)}")

        try:
            response = requests.get(f"{BACKEND_URL}/notes", timeout=5)
            if response.status_code == 200:
                notes = response.json().get('notes', [])
            else:
                app.logger.error(f"Backend returned {response.status_code}")
        except requests.exceptions.RequestException as e:
            app.logger.error(f"Failed to fetch notes: {str(e)}")
            
    except Exception as e:
        app.logger.error(f"Unexpected error: {str(e)}")
        
    return render_template('index.html', notes=notes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
