CACHE = {}
CACHE_TIME = 300 #5 MIN
import requests
from esg_engine import calculate_true_esg, get_risk_level
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

import time

def fetch_news(company):
    current_time = time.time()

    # ✅ check cache
    if company in CACHE:
        cached_data, timestamp = CACHE[company]

        if current_time - timestamp < CACHE_TIME:
            return cached_data

    # 🔽 normal API call
    url = f"https://newsapi.org/v2/everything?q={company}&apiKey={API_KEY}"
    response = requests.get(url)

    if response.status_code != 200:
        return []

    data = response.json()
    articles = []

    for article in data.get("articles", []):
        text = (article.get("title", "") + " " + str(article.get("description", "")))
        articles.append(text)

    # ✅ store in cache
    CACHE[company] = (articles, current_time)

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

    # 🔁 LOOP (sirf data collect)
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

    # ✅ LOOP KE BAAD (IMPORTANT)
    official_esg = OFFICIAL_ESG.get(company.lower(), 75)

    # ✅ ESG CALCULATION
    if not results:
        true_esg = official_esg
        risk = "LOW"
        delta = 0
    else:
        true_esg = calculate_true_esg(official_esg, results)
        risk = get_risk_level(true_esg)
        delta = official_esg - true_esg

    # ✅ FINAL RESPONSE
    return {
        "company": company,
        "official_esg": official_esg,
        "true_esg": true_esg,
        "delta": delta,
        "risk_level": risk,
        "articles_analyzed": len(news_list),
        "events": results[:5],
        "timestamp": datetime.now().isoformat()
    }
@app.get("/analyze_multiple")
def analyze_multiple(companies: str):
    company_list = companies.split(",")

    output = []

    for company in company_list:
        company = company.strip().lower()

        news_list = fetch_news(company)

        if not news_list:
            news_list = ["Company involved in environmental pollution and legal violation"]

        results = []

        # 🔁 LOOP
        for text in news_list:
            event = analyze_news(text)

            if event["impact"] == "neutral":
                continue

            results.append({
                "reason": event["reason"],
                "confidence": event["severity"]
            })

        # ✅ LOOP KE BAAD
        official_esg = OFFICIAL_ESG.get(company, 75)

        if not results:
            true_esg = official_esg
        else:
            true_esg = calculate_true_esg(official_esg, results)

        output.append({
            "company": company,
            "official_esg": official_esg,
            "true_esg": true_esg
        })

    return {
        "results": output,
        "timestamp": datetime.now().isoformat()
    }