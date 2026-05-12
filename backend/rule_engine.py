import os
from config import WEIGHTS, SAFE_THRESHOLD, SUSPICIOUS_THRESHOLD, CONTEXT_BOOST, MAX_KEYWORD_HITS

# LOAD KEYWORDS FROM TXT
def load_keywords():
    path = os.path.join(os.path.dirname(__file__), "../data/keywords.txt")

    with open(path, "r", encoding="utf-8") as f:
        return [line.strip().lower() for line in f if line.strip()]

KEYWORDS = load_keywords()


def analyze_text(text, c_features):

    text_lower = text.lower()

    # KEYWORD MATCHING
    keyword_hits = 0
    matched_keywords = []

    for kw in KEYWORDS:
        if kw in text_lower:
            keyword_hits += 1
            matched_keywords.append(kw)

    # normalize keyword score
    keyword_score = min(keyword_hits / MAX_KEYWORD_HITS, 1.0)


    # C MODULE FEATURES
    caps_ratio = c_features.get("caps_ratio", 0)
    repetition_score = c_features.get("repetition_score", 0)


    # BASE WEIGHTED SCORE
    score = (
        keyword_score * WEIGHTS["keyword"] +
        caps_ratio * WEIGHTS["caps"] +
        repetition_score * WEIGHTS["repetition"]
    )

    # CONTEXT APPROXIMATION BOOSTING
    context_boost = 0

    if caps_ratio > 0.7:
        context_boost += CONTEXT_BOOST["high_caps"]

    if repetition_score > 0.6:
        context_boost += CONTEXT_BOOST["high_repetition"]

    if keyword_hits >= 3:
        context_boost += CONTEXT_BOOST["multiple_keywords"]

    score = min(score + context_boost, 1.0)


    # FINAL CLASSIFICATION
    if score >= SUSPICIOUS_THRESHOLD:
        label = "TOXIC"
    elif score >= SAFE_THRESHOLD:
        label = "SUSPICIOUS"
    else:
        label = "SAFE"

    # RESPONSE FORMAT
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