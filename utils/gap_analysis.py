job_roles = {

"Data Analyst": ["python","sql","excel","data analysis"],

"ML Engineer": ["python","machine learning","tensorflow"],

"Web Developer": ["html","css","javascript"]

}

def analyze_gap(user_skills, role):

    required = job_roles[role]

    matched = set(user_skills) & set(required)

    missing = set(required) - set(user_skills)

    match_percent = (len(matched)/len(required))*100

    return round(match_percent,2), list(missing)
