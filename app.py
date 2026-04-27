import pdfkit
from flask import make_response

config = pdfkit.configuration(
    wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
)
from database.db import get_skills_by_domain
from flask import Flask, render_template, request, redirect, session
import PyPDF2
import psycopg2
from datetime import timedelta
import smtplib
from email.mime.text import MIMEText

# -------------------- DB CONNECTION --------------------
conn = psycopg2.connect(
    host="localhost",
    database="skillpath_db",
    user="postgres",
    password="123456789"
)
cursor = conn.cursor()

# -------------------- IMPORTS --------------------
from utils.course_recommender import recommend_courses
from utils.company_recommender import recommend_companies
from utils.preprocess import preprocess_text
from utils.skill_extractor import extract_skills
from utils.predictor import predict_job
from utils.resume_validator import is_resume

# -------------------- FLASK APP --------------------
app = Flask(__name__)
app.secret_key = "secret123"
app.permanent_session_lifetime = timedelta(days=10)

@app.before_request
def make_session_permanent():
    session.permanent = True

# -------------------- HELPER FUNCTIONS --------------------


def get_domain_confidence(user_skills):
    cursor.execute("SELECT name FROM domains1")
    domains = [row[0] for row in cursor.fetchall()]

    user_skills_lower = [s.lower() for s in user_skills]
    domain_scores = {}

    for domain in domains:
        db_skills = get_skills_by_domain(domain)

        match_count = sum(
            1 for skill in db_skills
            if skill.lower() in user_skills_lower
        )

        total = len(db_skills)
        score = (match_count / total) * 100 if total > 0 else 0

        domain_scores[domain] = round(score, 2)

    return domain_scores

def get_recommendations(role, missing):
    suggestions = []

    if len(missing) > 3:
        suggestions.append("You are missing important core skills.")

    if role == "Frontend":
        suggestions.append("Learn React and build UI projects.")

    if role == "Backend":
        suggestions.append("Work on APIs and databases.")

    if role == "App Development":
        suggestions.append("Build mobile apps using Flutter or Kotlin.")

    if role == "Data Science":
        suggestions.append("Practice ML models and data analysis.")

    suggestions.append("Add 2-3 strong projects.")

    return suggestions

def send_email(to_email, skills, missing, role, probability):
    sender_email = "your_email@gmail.com"
    app_password = "your_app_password"

    body = f"""
Domain: {role}
Skills: {', '.join(skills)}
Missing: {', '.join(missing)}
Probability: {probability}%
"""

    msg = MIMEText(body)
    msg['Subject'] = "Career Report"
    msg['From'] = sender_email
    msg['To'] = to_email

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, app_password)
        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()
    except Exception as e:
        print("Email error:", e)

# -------------------- ROUTES --------------------
@app.route('/')
def index():
    if 'user' not in session:
        return render_template("index.html")
    return render_template("upload.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        if username.lower() == "admin" and password == "1234":
            session['user'] = username
            return redirect('/')
        else:
            return render_template('login.html', error="Invalid credentials")

    return render_template('login.html')
# -------------------- HELPER FUNCTIONS --------------------
def normalize(skill):
    return skill.lower().replace(".", "").replace(" ", "")

@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        cursor = get_cursor()

        cursor.execute("""
            INSERT INTO users (username, email, password)
            VALUES (%s, %s, %s)
        """, (username, email, password))

        conn.commit()

        return redirect('/login')

    return render_template("signup.html")
@app.route('/analyze', methods=['POST'])
def analyze():

    if 'user' not in session:
        return redirect('/login')

    if 'resume' not in request.files:
        return render_template("upload.html", error="No file uploaded.")

    file = request.files['resume']

    if file.filename == "":
        return render_template("upload.html", error="Please select a file.")

    try:
        reader = PyPDF2.PdfReader(file)
        text = ""

        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted

    except:
        return render_template("upload.html", error="Invalid file format.")

    if not is_resume(text):
        return render_template("upload.html", error="Invalid document.")

    print("RAW TEXT:\n", text[:1000])

    tokens = preprocess_text(text)
    skills = extract_skills(tokens)

    if not skills:
        skills = ["No major skills detected"]

    # ================= DOMAIN =================
    domain_scores = get_domain_confidence(skills)
    role = max(domain_scores, key=domain_scores.get)

    user_skills_lower = [s.lower() for s in skills]

    if role == "Frontend" and "react" in user_skills_lower:
        role = "Full Stack"

    if any(s in user_skills_lower for s in ["android", "kotlin", "flutter"]):
        role = "App Development"

    # ================= MATCHING =================
# 🔥 HANDLE FULL STACK CASE
    if role == "Full Stack":
      required_skills = get_skills_by_domain("Frontend") + get_skills_by_domain("Backend")
    else:
     required_skills = get_skills_by_domain(role)
     required_skills = list(set(required_skills))
    # 🔥 NORMALIZATION FUNCTION
    def normalize(skill):
        return skill.lower().replace(".", "").replace(" ", "").replace("-", "")

    # 🔥 HANDLE FULL STACK CASE
    if role == "Full Stack":
        required_skills = get_skills_by_domain("Frontend") + get_skills_by_domain("Backend")
    else:
        required_skills = get_skills_by_domain(role)

    required_skills = list(set(required_skills))

    # 🔥 NORMALIZE SKILLS
    user_skills_clean = [normalize(s) for s in skills]
    required_skills_clean = [normalize(s) for s in required_skills]

    print("USER SKILLS:", user_skills_clean)
    print("ROLE:", role)
    print("REQUIRED SKILLS:", required_skills_clean)

    # 🔥 MATCHING LOGIC
    matched = []

    for req in required_skills_clean:
        for usr in user_skills_clean:
            if req in usr or usr in req:
                matched.append(req)
                break

    # 🔥 FIND MISSING SKILLS
    missing = [
        required_skills[i]
        for i, r in enumerate(required_skills_clean)
        if r not in matched
    ]

    # 🔥 CALCULATE MATCH %
    total = len(required_skills_clean)
    match_percentage = (len(matched) / total) * 100 if total > 0 else 0

    print("MATCHED:", matched)
    print("MISSING:", missing)
    print("MATCH %:", match_percentage)

    # ================= RECOMMENDATIONS =================

    courses = recommend_courses(missing)
    companies = recommend_companies(skills)

    if not companies:
        companies = ["No matching companies found"]

    recommendations = get_recommendations(role, missing)

    # 🔥 TEMP PROBABILITY FIX (better output)
    probability = round(match_percentage + 20, 2)

    email = request.form.get("email")
    if email:
        send_email(email, skills, missing, role, probability)
    session['report_data'] = {
    "skills": skills,
    "match": round(match_percentage, 2),
    "missing": missing,
    "role": role,
    "probability": probability,
    "courses": courses,
    "companies": companies
}
    session['report_data'] = {
    "skills": skills,
    "match": round(match_percentage, 2),
    "missing": missing,
    "role": role,
    "probability": probability,
    "courses": courses,
    "companies": companies
}
    return render_template(
        "dashboard.html",
        skills=skills,
        match=round(match_percentage, 2),
        missing_skills=missing,
        role=role,
        job_probability=probability,
        courses=courses,
        companies=companies,
        domain_scores=domain_scores,
        recommendations=recommendations
    )
@app.route('/download_pdf')
def download_pdf():

    if 'report_data' not in session:
        return "No report available"

    data = session['report_data']

    rendered = render_template(
        "report_template.html",
        skills=data['skills'],
        match=data['match'],
        missing=data['missing'],
        role=data['role'],
        probability=data['probability'],
        courses=data['courses'],
        companies=data['companies']
    )

    pdf = pdfkit.from_string(rendered, False, configuration=config)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=SkillPath_Report.pdf'

    return response

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

# -------------------- RUN --------------------
if __name__ == "__main__":
    app.run(debug=True)
