def pdf_to_json(pdf_bytes: bytes):
    from utils.normalize_text import normalize_text
    from utils.parse_articles import parse_articles

    def extract_text_from_bytes(pdf_bytes: bytes) -> str:
        import fitz  # PyMuPDF

        texts = []
        with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
            for page in doc:
                text = page.get_text("text")
                if text:
                    texts.append(text)
        return "\\n".join(texts)

    raw_text = extract_text_from_bytes(pdf_bytes)
    normalized_lines = normalize_text(raw_text)
    parsed = parse_articles(normalized_lines)

    return parsed
