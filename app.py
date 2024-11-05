from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload folders if they don't exist
CATEGORIES = ['documents', 'images', 'videos', 'audio', 'others']
for category in CATEGORIES:
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], category), exist_ok=True)

def get_file_category(filename):
    extension = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    
    if extension in ['txt', 'pdf', 'doc', 'docx']:
        return 'documents'
    elif extension in ['jpg', 'jpeg', 'png', 'gif']:
        return 'images'
    elif extension in ['mp4', 'avi', 'mov']:
        return 'videos'
    elif extension in ['mp3', 'wav']:
        return 'audio'
    else:
        return 'others'

@app.route('/')
def index():
    files = {}
    for category in CATEGORIES:
        category_path = os.path.join(app.config['UPLOAD_FOLDER'], category)
        files[category] = os.listdir(category_path)
    return render_template('index.html', files=files, categories=CATEGORIES)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    if file:
        filename = secure_filename(file.filename)
        category = get_file_category(filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], category, filename))
    
    return redirect(url_for('index'))

@app.route('/download/<category>/<filename>')
def download_file(category, filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], category), filename)

@app.route('/delete/<category>/<filename>')
def delete_file(category, filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], category, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)