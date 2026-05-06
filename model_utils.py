import joblib
import pandas as pd
from urllib.parse import urlparse

from feature_extractor import extract_features


# Load once
model = joblib.load("model/phishing_model.pkl")
features = joblib.load("model/features.pkl")


TRUSTED = ["google.com", "microsoft.com", "amazon", "wikipedia"]


def is_trusted(url):
    domain = urlparse(url).netloc.lower()
    return any(t in domain for t in TRUSTED)


def predict_url(url):

    if is_trusted(url):
        return {
            "url": url,
            "result": "Legitimate",
            "confidence": 100,
            "message": "Trusted domain override"
        }

    features_dict = extract_features(url)

    sample = pd.DataFrame([features_dict])[features]

    pred = model.predict(sample)[0]
    prob = model.predict_proba(sample)[0]

    if pred == 1:
        return {
            "url": url,
            "result": "Phishing",
            "confidence": round(prob[1] * 100, 2),
            "message": "Phishing detected"
        }

    return {
        "url": url,
        "result": "Legitimate",
        "confidence": round(prob[0] * 100, 2),
        "message": "URL looks safe"
    }