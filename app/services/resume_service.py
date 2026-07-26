import re
import spacy
from app.models import ResumeData

nlp = spacy.load('en_core_web_sm')

TECH_WORDS = {
    "RAG",
    "LLM",
    "MCP",
    "LangChain",
    "LangGraph",
    "LlamaIndex",
    "FastAPI",
    "Python",
    "Java",
    "JavaScript",
    "React",
    "Node",
    "NodeJS",
    "Express",
    "Docker",
    "Kubernetes",
    "TensorFlow",
    "PyTorch",
    "AWS",
    "Azure",
    "GCP",
    "Gemini",
    "ChromaDB",
    "Redis",
    "MongoDB",
    "PostgreSQL",
    "Git",
    "REST",
    "API",
}

BAD_WORDS = {
    "Resume",
    "Curriculum",
    "Vitae",
    "CV",
    "Engineer",
    "Developer",
    "Intern",
    "Manager",
    "Portfolio",
    "Github",
    "GitHub",
    "LinkedIn",
    "India",
}

def extract_email(text):

    email = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,7}", text)
    if email:
        # print(email)
        # print(email.group())
        # print(email.start())
        # print(email.end())
        # print(type(email))
        return email.group()
    return None

def extract_phone_number(text):
    ph_number = re.search(r"(?<!\w)\+?\d{10,15}(?!\w)", text)
    if ph_number:
        return ph_number.group()
    return None


def extract_resume_information(text: str) -> ResumeData:
    return ResumeData(
        name=extract_name(text),
        email=extract_email(text),
        phone=extract_phone_number(text)
    )

def clean_text(text: str) -> str:
    return " ".join(text.split())


def get_header(text: str) -> str:
    """
    Use only first 8 non-empty lines.
    Most resumes contain the name here.
    """
    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    return "\n".join(lines[:8])


def score_candidate(candidate: str, header: str) -> int:

    score = 0

    candidate = clean_text(candidate)

    words = candidate.split()

    # ----------------------------------
    # Position
    # ----------------------------------

    if candidate in header:
        score += 10

    # ----------------------------------
    # Word Count
    # ----------------------------------

    if 1 <= len(words) <= 3:
        score += 5
    else:
        score -= 10

    # ----------------------------------
    # Numbers
    # ----------------------------------

    if any(ch.isdigit() for ch in candidate):
        score -= 20

    # ----------------------------------
    # Email
    # ----------------------------------

    if "@" in candidate:
        score -= 20

    # ----------------------------------
    # Alphabetic
    # ----------------------------------

    if all(word.replace(".", "").isalpha() for word in words):
        score += 5

    # ----------------------------------
    # Tech Stack
    # ----------------------------------

    for word in words:
        if word.upper() in {w.upper() for w in TECH_WORDS}:
            score -= 50

    # ----------------------------------
    # Resume Keywords
    # ----------------------------------

    for word in words:
        if word in BAD_WORDS:
            score -= 25

    # ----------------------------------
    # ALL CAPS Bonus
    # Many resumes have uppercase names.
    # ----------------------------------

    if candidate.isupper():
        score += 3

    return score


def extract_name(text: str) -> str | None:

    header = get_header(text)

    doc = nlp(header)

    candidates = []

    for ent in doc.ents:

        if ent.label_ != "PERSON":
            continue

        candidate = clean_text(ent.text)

        # Remove locations accidentally attached
        mini_doc = nlp(candidate)

        person_tokens = []

        for token in mini_doc.ents:

            if token.label_ == "PERSON":
                person_tokens.append(token.text)

        if person_tokens:
            candidate = " ".join(person_tokens)

        candidates.append(candidate)

    if not candidates:
        return None

    best_candidate = None
    best_score = float("-inf")

    for candidate in candidates:

        score = score_candidate(candidate, header)

        print(f"{candidate} -> {score}")

        if score > best_score:
            best_score = score
            best_candidate = candidate

    return best_candidate