import joblib
import pandas as pd
import re
from urllib.parse import urlparse

# Define the feature extraction function (copied from cell 1ScU2P-ZRd2_ and adapted)
def extract_features(url):
    """Extracts selected features from a single URL string."""
    extracted_features_dict = {}
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname if parsed_url.hostname else ''

    # 1. length_url
    extracted_features_dict['length_url'] = len(url)

    # 2. length_hostname
    extracted_features_dict['length_hostname'] = len(hostname)

    # 3. ip (check if hostname is an IP address)
    extracted_features_dict['ip'] = 1 if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', hostname) else 0

    # Character counts
    extracted_features_dict['nb_dots'] = url.count('.')
    extracted_features_dict['nb_hyphens'] = url.count('-')
    extracted_features_dict['nb_at'] = url.count('@')
    extracted_features_dict['nb_qm'] = url.count('?')
    extracted_features_dict['nb_and'] = url.count('&')
    extracted_features_dict['nb_eq'] = url.count('=')
    extracted_features_dict['nb_underscore'] = url.count('_')
    extracted_features_dict['nb_percent'] = url.count('%')
    extracted_features_dict['nb_slash'] = url.count('/')
    extracted_features_dict['nb_colon'] = url.count(':')

    # 14. nb_www
    extracted_features_dict['nb_www'] = url.lower().count('www')

    # 15. nb_com
    extracted_features_dict['nb_com'] = url.lower().count('.com')

    # 16. https_token
    extracted_features_dict['https_token'] = 1 if url.startswith('https') else 0

    # 17. ratio_digits_url
    digits = sum(c.isdigit() for c in url)
    extracted_features_dict['ratio_digits_url'] = digits / len(url) if len(url) > 0 else 0

    # 18. nb_subdomains (approximate: count dots in hostname, minus 1 for TLD)
    # This is a simplification; a more robust approach would use a public suffix list.
    if hostname:
        extracted_features_dict['nb_subdomains'] = hostname.count('.') - 1
        if hostname.startswith('www.'):
            extracted_features_dict['nb_subdomains'] -= 1
        extracted_features_dict['nb_subdomains'] = max(0, extracted_features_dict['nb_subdomains'])
    else:
        extracted_features_dict['nb_subdomains'] = 0

    return extracted_features_dict

# Load model + features
model = joblib.load("model/phishing_model.pkl")
features = joblib.load("model/features.pkl")


def test_url(url):
    features_dict = extract_features(url)

    sample = pd.DataFrame([features_dict])[features]

    pred = model.predict(sample)[0]
    prob = model.predict_proba(sample)[0]

    print("\nURL:", url)

    if pred == 1:
        print("🔴 Phishing Detected")
        print(f"Confidence: {prob[1]*100:.2f}%")
    else:
        print("🟢 Legitimate")
        print(f"Confidence: {prob[0]*100:.2f}%")


# =========================
# TEST SET
# =========================

urls = [

    # Legitimate
    "https://www.google.com",
    "https://www.microsoft.com",
    "https://www.amazon.in",
    "https://www.wikipedia.org",
    "https://colab.research.google.com",

    # Suspicious
    "http://paypal-login-secure-update.com",
    "http://verify-account-security-update.net",
    "http://bank-login-confirmation-alert.com",

    # Edge cases
    "http://192.168.0.1/login",
    "http://bit.ly/secure-login",
    "http://free-money-win-now123.biz"
]

for url in urls:
    test_url(url)