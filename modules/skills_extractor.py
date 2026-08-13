import pandas as pd
import spacy
import re


# Load NLP Model
nlp = spacy.load("en_core_web_sm")


# Load Skills List
skills_df = pd.read_csv("skills.csv")

skills = (
    skills_df["skill"]
    .dropna()
    .astype(str)
    .str.lower()
    .str.strip()
    .tolist()
)


def normalize_text(text):
    """
    Clean and normalize resume/job description text.
    """

    text = text.lower()

    # Replace special characters with spaces
    text = re.sub(r"[^a-zA-Z0-9+#.\- ]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def extract_skills(text):
    """
    Extract skills using NLP preprocessing
    and skills list matching.
    """

    # Normalize text
    text = normalize_text(text)

    # Process text with spaCy
    doc = nlp(text)

    # Create tokens
    tokens = {
        token.text.lower()
        for token in doc
        if not token.is_stop and not token.is_punct
    }

    found_skills = []

    # Check skills
    for skill in skills:

        skill = skill.lower().strip()

        # Multi-word skills
        if " " in skill:

            if skill in text:
                found_skills.append(skill)

        # Single-word skills
        else:

            if skill in tokens:
                found_skills.append(skill)

    return sorted(list(set(found_skills)))