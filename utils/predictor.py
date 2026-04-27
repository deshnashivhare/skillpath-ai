
import joblib

model = joblib.load("models/job_model.pkl")

def predict_job(skill_match,test_score,projects,experience):

    result = model.predict_proba(
        [[skill_match,test_score,projects,experience]]
    )

    probability = result[0][1] * 100

    return round(probability,2)
