import re

ROLE_PATTERNS = [
    r"team principal",
    r"managing director",
    r"chief executive",
]

BLACKLIST = [
    "driver",
    "midfielder",
    "forward",
    "striker",
    "goalkeeper",
]

def validate_evidence(question: str, text: str) -> str:
    if not text or len(text) < 50:
        return ""

    q = question.lower()

    # If question is about a role, enforce role verification
    if "team principal" in q or "who is" in q:
        good_lines = []
        for line in text.splitlines():
            line_l = line.lower()

            if any(b in line_l for b in BLACKLIST):
                continue

            if any(re.search(p, line_l) for p in ROLE_PATTERNS):
                good_lines.append(line)

        return "\n".join(good_lines[:5])

    return text[:800]
