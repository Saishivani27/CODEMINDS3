from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import datetime
import random
import requests
import pdfkit

# ✅ Hugging Face API Details
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/bert-base-uncased"
HUGGINGFACE_API_KEY = "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"  # ❗ Add your API key

HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

app = FastAPI()

# ✅ Enable CORS for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Define Input Format
class StudyPlanRequest(BaseModel):
    hard_subjects: list
    intermediate_subjects: list
    easy_subjects: list
    study_hours: int
    deadline: str

# ✅ AI Study Plan Generator
def get_ai_study_plan(prompt):
    response = requests.post(HUGGINGFACE_API_URL, headers=HEADERS, json={"inputs": prompt})
    if response.status_code == 200:
        return response.json()[0]['summary_text']
    else:
        return "Error fetching AI-generated plan."

# ✅ Generate Study Plan Logic
@app.post("/generate_plan")
def generate_study_plan(request: StudyPlanRequest):
    today = datetime.date.today()
    deadline_date = datetime.datetime.strptime(request.deadline, "%Y-%m-%d").date()
    days_left = (deadline_date - today).days

    if days_left <= 0:
        return {"error": "Invalid deadline! Choose a future date."}

    subjects = request.hard_subjects * 3 + request.intermediate_subjects * 2 + request.easy_subjects * 1
    random.shuffle(subjects)

    study_plan = []
    start_time = 9  # Start at 9 AM

    for i in range(days_left):
        study_date = today + datetime.timedelta(days=i)
        day_name = study_date.strftime("%A")
        time_slot = start_time

        for hour in range(request.study_hours):
            subject = subjects[hour % len(subjects)]
            end_time = time_slot + 1
            formatted_time = f"{time_slot}:00 - {end_time}:00 {'AM' if end_time < 12 else 'PM'}"

            study_plan.append({
                "Date": str(study_date) if hour == 0 else "",
                "Day": day_name if hour == 0 else "",
                "Time Slot": formatted_time,
                "Subject": subject,
                "Duration": "1 hour"
            })

            time_slot += 1

    # ✅ AI-Generated Summary
    prompt = f"Create a {days_left}-day study plan focusing more on hard subjects: {request.hard_subjects}. Include intermediate: {request.intermediate_subjects} and easy: {request.easy_subjects}. Study {request.study_hours} hours daily."
    ai_summary = get_ai_study_plan(prompt)

    return {"plan": study_plan, "summary": ai_summary}

# ✅ Convert Study Plan to PDF
@app.post("/download_pdf")
def download_pdf(study_plan: dict):
    html_content = "<h1>StudBud - AI Study Plan</h1><table border='1'><tr><th>Date</th><th>Day</th><th>Time Slot</th><th>Subject</th></tr>"
    
    for row in study_plan['plan']:
        html_content += f"<tr><td>{row['Date']}</td><td>{row['Day']}</td><td>{row['Time Slot']}</td><td>{row['Subject']}</td></tr>"
    
    html_content += "</table>"
    
    pdfkit.from_string(html_content, "study_plan.pdf")
    
    return {"message": "PDF generated successfully"}
