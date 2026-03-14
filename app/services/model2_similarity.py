def run_similarity(extracted_text: str, answer_key: str) -> dict:
    """
    MOCK: Simulates Model 2 (Sentence Transformers similarity + keyword extraction).
    Returns keywords, similarity_score, and missing_keywords.
    Replace this with the real HuggingFace API call later.
    """
    print(f"[MOCK MODEL 2] Comparing student answer with answer key...")

    # Simple keyword extraction: filter out common stop words
    STOP_WORDS = {
        "the",
        "a",
        "an",
        "and",
        "or",
        "but",
        "is",
        "it",
        "in",
        "on",
        "at",
        "to",
        "for",
        "of",
        "with",
        "as",
        "by",
        "that",
        "this",
        "are",
        "was",
        "were",
        "be",
        "been",
        "has",
        "have",
        "had",
        "do",
        "does",
        "did",
        "will",
        "would",
        "could",
        "should",
        "may",
        "might",
        "its",
        "their",
        "they",
        "we",
        "he",
        "she",
    }

    def extract_keywords(text: str) -> set:
        words = text.lower().replace(".", "").replace(",", "").split()
        return {w for w in words if w not in STOP_WORDS and len(w) > 3}

    student_keywords = extract_keywords(extracted_text)
    answer_keywords = extract_keywords(answer_key)

    # Keywords found in student answer
    found_keywords = list(student_keywords)

    # Missing: keywords in answer key but NOT in student answer
    missing = list(answer_keywords - student_keywords)

    # Similarity: ratio of matched keywords
    if answer_keywords:
        matched = answer_keywords & student_keywords
        similarity_score = round((len(matched) / len(answer_keywords)) * 100, 2)
    else:
        similarity_score = 0.0

    return {
        "keywords": found_keywords,
        "similarity_score": similarity_score,
        "missing_keywords": missing,
    }
