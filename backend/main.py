from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# App init
app = FastAPI()

# CORS (IMPORTANT for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sample data
NEWS_DATA = [
    {"company": "Shell", "text": "Shell caused major oil spill in ocean"},
    {"company": "Tesla", "text": "Tesla invests in renewable energy expansion"},
    {"company": "Nike", "text": "Nike faces lawsuit over labor exploitation"},
]

BASE_SCORE = 80

# Analyze news
def analyze_news(text):
    text = text.lower()

    if "oil spill" in text or "pollution" in text:
        return {
            "impact": "negative",
            "severity": 0.9,
            "reason": "Environmental damage"
        }

    if "lawsuit" in text:
        return {
            "impact": "negative",
            "severity": 0.6,
            "reason": "Legal issue"
        }

    if "renewable" in text:
        return {
            "impact": "positive",
            "severity": 0.4,
            "reason": "Green initiative"
        }

    return {
        "impact": "neutral",
        "severity": 0,
        "reason": "No impact"
    }

# Score calculator
def calculate_score(event):
    score = BASE_SCORE

    if event["impact"] == "negative":
        score -= int(event["severity"] * 20)

    elif event["impact"] == "positive":
        score += int(event["severity"] * 10)

    return score

# Root route (optional but helpful)
@app.get("/")
def home():
    return {"message": "EcoAudit API running"}

# MAIN API
@app.get("/analyze")
def analyze():
    results = []

    for item in NEWS_DATA:
        event = analyze_news(item["text"])
        score = calculate_score(event)

        results.append({
            "company": item["company"],
            "score": score,
            "reason": event["reason"]
        })

    return results