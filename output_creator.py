import pandas as pd
from fpdf import FPDF

def save_schedule_excel(schedule):
    df = pd.DataFrame(schedule)
    df.to_excel("final_schedule.xlsx", index=False)

def save_schedule_pdf(schedule):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="برنامه نهایی کلاس‌ها", ln=True, align='C')
    pdf.ln()
    for item in schedule:
        text = f"{item['درس']} - {item['استاد']} - {item['روز']} - {item['ساعت شروع']} تا {item['ساعت پایان']} - کلاس {item['کلاس']}"
        pdf.cell(200, 10, txt=text, ln=True, align='R')
    pdf.output("final_schedule.pdf")
