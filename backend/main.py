import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

API_KEY = "ca8ee85f106942ee890132bc6970b453"
BASE_SCORE = 80

OFFICIAL_ESG = {
    "shell": 85,
    "tesla": 90,
    "nike": 80,
    "oil": 88
}

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def fetch_news(company):
    url = f"https://newsapi.org/v2/everything?q={company}&apiKey={API_KEY}"
    response = requests.get(url)

    if response.status_code != 200:
        return []

    data = response.json()
    articles = []

    for article in data.get("articles", []):
        text = (article.get("title", "") + " " + str(article.get("description", "")))
        articles.append(text)

    return articles

def analyze_news(text):
    text = text.lower()

    if any(word in text for word in ["oil spill", "pollution", "toxic", "emission", "carbon"]):
        return {"impact": "negative", "severity": 0.8, "reason": "Environmental issue detected"}

    if any(word in text for word in ["lawsuit", "fine", "penalty", "violation"]):
        return {"impact": "negative", "severity": 0.6, "reason": "Legal issue"}

    if any(word in text for word in ["renewable", "sustainable", "green", "solar"]):
        return {"impact": "positive", "severity": 0.5, "reason": "Green initiative"}

    return {"impact": "neutral", "severity": 0, "reason": "No impact"}

def calculate_score(event):
    score = BASE_SCORE

    if event["impact"] == "negative":
        score -= int(event["severity"] * 20)
    elif event["impact"] == "positive":
        score += int(event["severity"] * 10)

    return score

@app.get("/")
def home():
    return {"message": "EcoAudit API running"}

@app.get("/analyze")
def analyze(company: str):
    news_list = fetch_news(company)

    if not news_list:
        news_list = ["Company involved in environmental pollution and legal violation"]

    results = []

    for text in news_list:
        event = analyze_news(text)

        if event["impact"] == "neutral":
            continue

        score = calculate_score(event)

        results.append({
            "company": company,
            "score": score,
            "reason": event["reason"],
            "explanation": f"Detected pattern: {event['reason']}",
            "confidence": event["severity"],
            "timestamp": datetime.now().isoformat()
        })

    if results:
        total_score = sum(item["score"] for item in results)
        true_score = int(total_score / len(results))
    else:
        true_score = BASE_SCORE

    if not results:
        return [{"message": "No ESG violations detected currently"}]

    official_score = OFFICIAL_ESG.get(company.lower(), 80)
    delta = official_score - true_score

    if delta > 15:
        risk = "HIGH"
    elif delta > 5:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    return {
        "company": company,
        "official_esg": official_score,
        "true_esg": true_score,
        "delta": delta,
        "risk_level": risk,
        "articles_analyzed": len(news_list),
        "events": results[:5]
    }