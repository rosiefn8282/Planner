from flask import Flask, render_template, request, send_file
import os
from werkzeug.utils import secure_filename
from schedule_engine import run_genetic_algorithm
from output_creator import save_schedule_excel, save_schedule_pdf

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './'
app.config['ALLOWED_EXTENSIONS'] = {'xlsx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/schedule', methods=['GET', 'POST'])
def index():
    schedule = None
    score = None

    if request.method == 'POST':
        if 'file' not in request.files:
            return "فایل اکسل ارسال نشده است.", 400

        file = request.files['file']
        if file.filename == '' or not allowed_file(file.filename):
            return "فایل نامعتبر است.", 400

        # ذخیره فایل ورودی
        filename = secure_filename("input_data.xlsx")
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # اجرای الگوریتم زمان‌بندی
        try:
            schedule, score = run_genetic_algorithm(file_path)

            # تولید فایل‌های خروجی
            excel_path = save_schedule_excel(schedule)
            pdf_path = save_schedule_pdf(schedule)

            return render_template('schedule.html', schedule=schedule, score=score,
                                   excel_file=excel_path, pdf_file=pdf_path)

        except Exception as e:
            return f"خطا در پردازش فایل: {str(e)}", 500

    return render_template('upload.html')

@app.route('/download/<file_type>')
def download_file(file_type):
    if file_type == 'excel':
        path = 'output_schedule.xlsx'
    elif file_type == 'pdf':
        path = 'output_schedule.pdf'
    else:
        return "نوع فایل نامعتبر است.", 400

    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    else:
        return "فایل مورد نظر پیدا نشد.", 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
