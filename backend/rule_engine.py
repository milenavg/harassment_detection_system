import json
import os

# LOAD KEYWORDS FROM TXT
def load_keywords():
    path = os.path.join(os.path.dirname(__file__), "../data/keywords.txt")

    with open(path, "r", encoding="utf-8") as f:
        return [line.strip().lower() for line in f if line.strip()]

KEYWORDS = load_keywords()


# WEIGHTS (rule-based scoring system)
WEIGHTS = {
    "keyword": 0.5,
    "caps": 0.3,
    "repetition": 0.2
}

def analyze_text(text, c_features):
    text_lower = text.lower()

    # 1. KEYWORD MATCHING
    keyword_hits = 0
    matched_keywords = []

    for kw in KEYWORDS:
        if kw in text_lower:
            keyword_hits += 1
            matched_keywords.append(kw)

    keyword_score = min(keyword_hits / 5, 1.0)  # normalize


    # 2. C MODULE FEATURES
    caps_ratio = c_features.get("caps_ratio", 0)
    repetition_score = c_features.get("repetition_score", 0)


    # 3. WEIGHTED SCORING SYSTEM
    score = (
        keyword_score * WEIGHTS["keyword"] +
        caps_ratio * WEIGHTS["caps"] +
        repetition_score * WEIGHTS["repetition"]
    )

    # 4. CONTEXT APPROXIMATION
    context_boost = 0

    # repeated harassment style messages
    if repetition_score > 0.6:
        context_boost += 0.1

    # ALL CAPS aggression
    if caps_ratio > 0.7:
        context_boost += 0.1

    # multiple toxic keywords
    if keyword_hits >= 3:
        context_boost += 0.2

    score = min(score + context_boost, 1.0)


    # 5. FINAL LABEL DECISION
    if score >= 0.75:
        label = "TOXIC"
    elif score >= 0.45:
        label = "SUSPICIOUS"
    else:
        label = "SAFE"

    # 6. RETURN STRUCTURED RESULT
    return {
        "label": label,
        "score": round(score, 3),
        "categories": {
            "keyword_hits": keyword_hits,
            "matched_keywords": matched_keywords,
            "caps_ratio": caps_ratio,
            "repetition_score": repetition_score,
            "context_boost": round(context_boost, 3)
        }
    }