from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Ensure there's a folder to save the uploaded files
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400

    if file:
        filename = secure_filename(file.filename)  # Ensure filename is safe
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 200

    return jsonify({'error': 'Something went wrong'}), 500

@app.route('/')
def index():
    return "Hello, use /upload to upload files."

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
