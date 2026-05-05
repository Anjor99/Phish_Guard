# =========================
# 1. IMPORTS
# =========================

import pandas as pd
import numpy as np
import joblib

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


# =========================
# 2. LOAD DATA
# =========================

df = pd.read_csv("dataset\dataset_phishing.csv")

print("Dataset loaded")
print("Shape:", df.shape)


# =========================
# 3. CLEAN DATA
# =========================

df = df.drop_duplicates()
df = df.dropna()

print("After cleaning:", df.shape)


# =========================
# 4. LABEL ENCODING
# =========================

# Convert "legitimate"/"phishing" → 0/1
le = LabelEncoder()
df["status"] = le.fit_transform(df["status"])

print("\nLabel mapping:")
print(dict(zip(le.classes_, le.transform(le.classes_))))


# =========================
# 5. FEATURE SELECTION
# =========================

FEATURES = [

    "length_url",
    "length_hostname",

    "ip",
    "nb_dots",
    "nb_hyphens",
    "nb_at",
    "nb_qm",
    "nb_and",
    "nb_eq",
    "nb_underscore",
    "nb_percent",
    "nb_slash",
    "nb_colon",

    "nb_www",
    "nb_com",

    "https_token",

    "ratio_digits_url",

    "nb_subdomains"

]

X = df[FEATURES]
y = df["status"]

print("\nFeature count:", len(FEATURES))


# =========================
# 6. TRAIN-TEST SPLIT
# =========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# =========================
# 7. MODEL PIPELINE
# =========================

model = Pipeline([
    ("scaler", StandardScaler()),
    ("random_forest", RandomForestClassifier(
        n_estimators=200,
        max_depth=15,
        min_samples_split=5,
        min_samples_leaf=3,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    ))
])


# =========================
# 8. TRAIN MODEL
# =========================

print("\nTraining model...")
model.fit(X_train, y_train)


# =========================
# 9. EVALUATION
# =========================

y_pred = model.predict(X_test)

print("\n--- RESULTS ---")

print("Accuracy:", accuracy_score(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))


# =========================
# 10. CROSS VALIDATION
# =========================

cv_scores = cross_val_score(
    model,
    X,
    y,
    cv=5,
    scoring="accuracy"
)

print("\nCV Scores:", cv_scores)
print("Mean CV Accuracy:", cv_scores.mean())


# =========================
# 11. FEATURE IMPORTANCE
# =========================

rf = model.named_steps["random_forest"]

importance_df = pd.DataFrame({
    "Feature": FEATURES,
    "Importance": rf.feature_importances_
}).sort_values(by="Importance", ascending=False)

print("\nFeature Importance:")
print(importance_df)


# =========================
# 12. SAVE MODEL
# =========================

joblib.dump(model, "model/phishing_model.pkl")
joblib.dump(FEATURES, "model/features.pkl")

print("\nModel and features saved successfully!")


# =========================
# 13. QUICK TEST
# =========================

sample = X_test.iloc[:1]

print("\nTest sample prediction:")
print("Prediction:", model.predict(sample))
print("Probabilities:", model.predict_proba(sample))