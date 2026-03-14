def run_ocr(image_path: str) -> str:
    """
    MOCK: Simulates Model 1 (TrOCR OCR).
    Returns a hardcoded extracted text to test the full pipeline.
    Replace this with the real HuggingFace API call later.
    """
    print(f"[MOCK OCR] Would process image: {image_path}")
    return (
        "The operating system manages hardware resources "
        "and provides services to applications. "
        "It acts as an interface between the user and the hardware."
    )
