import re

PATTERNS = [
    r"ignore previous instructions",
    r"bypass safety",
    r"override policy",
    r"disregard system prompt",
]

def detect_injection(text):

    for p in PATTERNS:
        if re.search(p, text, re.IGNORECASE):
            return True

    return False
