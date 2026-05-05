# PhishGuard

PhishGuard is a machine learning-based web application for detecting phishing URLs using structural and statistical analysis.

---

## Links

* Repository: https://github.com/Anjor99/Phish_Guard.git
* Dataset: https://www.kaggle.com/datasets/shashwatwork/web-page-phishing-detection-dataset

---

## Overview

PhishGuard analyzes URLs using engineered features such as length, character distribution, and domain structure. A trained Random Forest model is used to classify URLs as either phishing or legitimate, with an associated confidence score.

The application includes both a web interface and an API endpoint for predictions.

---

## Features

* URL classification using a trained machine learning model
* Confidence scoring for predictions
* Feature-based URL analysis (length, symbols, subdomains, etc.)
* FastAPI backend with both UI and API support
* Trusted domain override mechanism

---

## Project Structure

```
Phish_Guard/
│
├── main.py                  # FastAPI application
├── model_utils.py           # Prediction logic
├── feature_extractor.py     # Feature engineering
├── script.py                # Model training script
├── test.py                  # Testing script
│
├── model/
│   ├── phishing_model.pkl
│   └── features.pkl
│
├── templates/
│   └── index.html
│
├── static/
│   └── style.css
│
├── requirements.txt
└── dataset/                 # Dataset (not included in repository)
```

---

## Installation

1. Clone the repository:

```
git clone https://github.com/Anjor99/Phish_Guard.git
cd Phish_Guard
```

2. Create a virtual environment:

```
python -m venv .venv
```

Activate it:

* Windows:

```
.venv\Scripts\activate
```

* macOS/Linux:

```
source .venv/bin/activate
```

3. Install dependencies:

```
pip install -r requirements.txt
```

---

## Running the Application

Start the FastAPI server:

```
uvicorn main:app --reload
```

Open in browser:

```
http://127.0.0.1:8000
```

---

## API Usage

### Endpoint

```
POST /api/predict
```

### Example Request

```
curl -X POST "http://127.0.0.1:8000/api/predict" \
     -d "url=https://example.com"
```

### Example Response

```
{
  "url": "https://example.com",
  "result": "Legitimate",
  "confidence": 97.25,
  "message": "URL looks safe"
}
```

---

## Model Details

* Algorithm: Random Forest Classifier
* Preprocessing: StandardScaler
* Training: Supervised learning with labeled phishing dataset

### Selected Features

* URL length
* Hostname length
* Number of special characters
* Subdomain count
* HTTPS usage
* Digit ratio

---

## Training the Model

1. Download the dataset from:
   https://www.kaggle.com/datasets/shashwatwork/web-page-phishing-detection-dataset

2. Place the dataset file at:

```
dataset/dataset_phishing.csv
```

3. Run the training script:

```
python script.py
```

This will train the model and save:

* `model/phishing_model.pkl`
* `model/features.pkl`

---

## Testing

Run:

```
python test.py
```

This script evaluates sample URLs and prints predictions with confidence scores.

---

## Notes

* The dataset is not included in the repository and must be downloaded separately
* Trusted domains are defined in `model_utils.py`
* Model performance depends on dataset quality and feature engineering

---

## License

MIT License
