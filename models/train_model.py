import pandas as pd
from sklearn.linear_model import LogisticRegression
import joblib

data = pd.read_csv("dataset/dataset.csv")

X = data[['skill_match','test_score','projects','experience']]
y = data['selected']

model = LogisticRegression()

model.fit(X,y)

joblib.dump(model,"models/job_model.pkl")

print("Model trained successfully")
