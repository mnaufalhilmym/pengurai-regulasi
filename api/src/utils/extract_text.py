from pathlib import Path
import pdfplumber


def extract_text(pdf_path: Path) -> str:
    texts = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:

            text = page.extract_text(layout=True)
            if text:
                texts.append(text)
    return "\n".join(texts)
