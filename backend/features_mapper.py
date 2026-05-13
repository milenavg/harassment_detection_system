import ctypes
import os
import json

MODULE_PATH = os.path.join(
    os.path.dirname(__file__),
    "../core/detector.dll"
)

# If DLL exists (Windows fallback)
if not os.path.exists(MODULE_PATH):
    MODULE_PATH = os.path.join(
        os.path.dirname(__file__),
        "../c_module/detector.dll"
    )

# Try to load library (safe fallback if not compiled yet)
try:
    detector = ctypes.CDLL(MODULE_PATH)
except Exception as e:
    print("C module not loaded, using fallback Python extractor:", e)
    detector = None


if detector:
    detector.analyze_text.argtypes = [ctypes.c_char_p]
    detector.analyze_text.restype = ctypes.c_char_p


def map_c_features(text):
    """
    Calls C module and returns extracted features.
    If C module is missing, fallback Python logic is used.
    """

    # FALLBACK MODE (if C not compiled)
    if detector is None:
        return fallback_features(text)

    try:
        result = detector.analyze_text(text.encode("utf-8"))

        # C returns JSON string
        result_str = result.decode("utf-8")

        return json.loads(result_str)

    except Exception as e:
        print("C MODULE ERROR:", e)
        return fallback_features(text)


# FALLBACK FEATURE EXTRACTION (PURE PYTHON)
def fallback_features(text):
    """
    Used when C module is not available. Ensures system still works.
    """

    if not text:
        return {
            "caps_ratio": 0,
            "repetition_score": 0,
            "keyword_hits": 0
        }

    # CAPS ratio
    caps = sum(1 for c in text if c.isupper())
    caps_ratio = caps / len(text) if len(text) > 0 else 0

    # SIMPLE repetition detection
    words = text.lower().split()
    repetition_score = 0

    if len(words) > 1:
        unique_ratio = len(set(words)) / len(words)
        repetition_score = 1 - unique_ratio

    return {
        "caps_ratio": round(caps_ratio, 3),
        "repetition_score": round(repetition_score, 3),
        "keyword_hits": 0
    }