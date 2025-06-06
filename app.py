# app.py
from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename
from schedule_engine import run_genetic_algorithm
from output_creator import save_schedule_excel, save_schedule_pdf

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './'
app.config['ALLOWED_EXTENSIONS'] = {'xlsx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def index():
    schedule = None
    score = None
    if request.method == 'POST':
        if 'file' not in request.files:
            return "فایل اکسل ارسال نشده است.", 400
        file = request.files['file']
        if file.filename == '' or not allowed_file(file.filename):
            return "فایل نامعتبر است.", 400
        filename = secure_filename("input_data.xlsx")
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        best_schedule, score = run_genetic_algorithm()
        save_schedule_excel(best_schedule)
        save_schedule_pdf(best_schedule)

        return render_template('index.html', schedule=best_schedule, score=score)

    return render_template('index.html', schedule=schedule, score=score)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

