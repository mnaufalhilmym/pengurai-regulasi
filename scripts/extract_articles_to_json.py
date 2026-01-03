import argparse
import json
from pathlib import Path

from utils.extract_text import extract_text
from utils.normalize_text import normalize_text
from utils.parse_articles import parse_articles


def parse_args():
    parser = argparse.ArgumentParser(
        description="Parser Regulasi Indonesia (BAB, Bagian, Paragraf, Pasal, Ayat, Poin)"
    )
    parser.add_argument("pdf", type=Path, help="Path ke file PDF regulasi")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="File output JSON (default: <nama_pdf>.json)",
    )

    return parser.parse_args()


def main():
    args = parse_args()
    input_path = args.pdf

    if not input_path.exists():
        raise FileNotFoundError(f"File tidak ditemukan: {input_path}")

    if input_path.suffix.lower() != ".pdf":
        raise ValueError("File input harus berekstensi .pdf")

    output_file = args.output or input_path.with_suffix(".json")

    print(f"[+] Membaca PDF: {input_path}")
    raw_text = extract_text(input_path)

    print("[+] Normalisasi teks...")
    normalized_lines = normalize_text(raw_text)

    print("[+] Parsing struktur regulasi...")
    parsed = parse_articles(normalized_lines)

    print(f"[+] Menulis output: {output_file}")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(parsed, f, indent=2, ensure_ascii=False)

    print(f"[✓] Selesai. Total record: {len(parsed)}")


if __name__ == "__main__":
    main()
