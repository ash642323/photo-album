from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    files_by_year = {}
    for year in sorted(os.listdir(UPLOAD_FOLDER), reverse=True):
        year_folder = os.path.join(UPLOAD_FOLDER, year)
        if os.path.isdir(year_folder):
            files = [f for f in os.listdir(year_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.mp4', '.webm'))]
            if files:
                files_by_year[year] = files
    years = list(files_by_year.keys())
    return render_template('index.html', files_by_year=files_by_year, years=years)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    year = request.form['year']
    year_folder = os.path.join(app.config['UPLOAD_FOLDER'], year)
    os.makedirs(year_folder, exist_ok=True)
    file.save(os.path.join(year_folder, file.filename))
    return redirect(url_for('index'))

@app.route('/year/<year>')
def year_page(year):
    year_folder = os.path.join(UPLOAD_FOLDER, year)
    files = os.listdir(year_folder)
    return render_template('year.html', year=year, files=files)