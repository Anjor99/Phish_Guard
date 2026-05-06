from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from model_utils import predict_url


app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request
    })
    
@app.get("/healthz")
def health():
    return {"status": "healthy"}

@app.post("/predict", response_class=HTMLResponse)
def predict(request: Request, url: str = Form(...)):

    if not url.startswith("http"):
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": "Invalid URL format (include http/https)"
        })

    result = predict_url(url)

    return templates.TemplateResponse("index.html", {
        "url": result["url"],
        "request": request,
        "result": result["result"],
        "confidence": result["confidence"],
        "message": result["message"]
    })
    
@app.post("/api/predict")
def api_predict(url: str):
    return predict_url(url)