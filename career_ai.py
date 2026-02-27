import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# ------------------------------
# 1. Load Dataset
# ------------------------------
data = pd.read_csv("career_dataset.csv")

# Encode categorical columns
label_encoders = {}
for col in data.columns:
    if data[col].dtype == 'object':
        le = LabelEncoder()
        data[col] = le.fit_transform(data[col])
        label_encoders[col] = le

# Features and target
X = data.drop("Career", axis=1)
y = data["Career"]

# ------------------------------
# 2. Train ML Model
# ------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# Save model
joblib.dump(model, "model.pkl")
print("Model trained and saved successfully!")

# ------------------------------
# 3. Career Skill Database
# ------------------------------
career_skills = {
    "Data Scientist": ["Python", "Statistics", "Machine Learning"],
    "Software Engineer": ["Programming", "DSA", "Problem Solving"],
    "Business Analyst": ["Excel", "SQL", "Communication"],
    "UI Designer": ["Creativity", "Design", "UX"]
}

# ------------------------------
# 4. Roadmap Database
# ------------------------------
roadmap = {
    "Data Scientist": ["Python Basics", "Data Analysis", "Machine Learning Projects"],
    "Software Engineer": ["DSA Practice", "Build Projects", "System Design"],
    "Business Analyst": ["Excel", "SQL", "Business Case Studies"],
    "UI Designer": ["Figma", "UX Research", "Portfolio"]
}

# ------------------------------
# 5. User Input
# ------------------------------
print("\n==== AI Career Guidance Tool ====")

user_input = {}

for col in X.columns:
    val = input(f"Enter {col}: ")
    user_input[col] = val

user_df = pd.DataFrame([user_input])

# Encode user input
for col in user_df.columns:
    if col in label_encoders:
        user_df[col] = label_encoders[col].transform(user_df[col])

# ------------------------------
# 6. Prediction
# ------------------------------
prediction = model.predict(user_df)[0]
confidence = np.max(model.predict_proba(user_df)) * 100

# Decode career
career_name = label_encoders["Career"].inverse_transform([prediction])[0]

print("\nRecommended Career:", career_name)
print("Confidence Score: {:.2f}%".format(confidence))

# ------------------------------
# 7. Skill Gap Analysis
# ------------------------------
print("\nSkill Gap Analysis:")
for skill in career_skills.get(career_name, []):
    print("-", skill)

# ------------------------------
# 8. Learning Roadmap
# ------------------------------
print("\nLearning Roadmap:")
for step in roadmap.get(career_name, []):
    print("-", step)

print("\nThank you for using CareerAI!")
