import argparse
from pathlib import Path
import pandas as pd

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
        help="File output spreadsheet (default: <nama_json>.xlsx)",
    )
    parser.add_argument(
        "--sheet-name", default="data", help="Nama sheet Excel (default: data)"
    )

    return parser.parse_args()


def main():
    args = parse_args()
    input_path = args.pdf

    if not input_path.exists():
        raise FileNotFoundError(f"File tidak ditemukan: {input_path}")

    if input_path.suffix.lower() != ".pdf":
        raise ValueError("File input harus berekstensi .pdf")

    output_file = args.output or input_path.with_suffix(".xlsx")

    print(f"[+] Membaca PDF: {input_path}")
    raw_text = extract_text(input_path)

    print("[+] Normalisasi teks...")
    normalized_lines = normalize_text(raw_text)

    print("[+] Parsing struktur regulasi...")
    parsed = parse_articles(normalized_lines)

    # Convert ke DataFrame
    df = pd.DataFrame(parsed)

    # Write ke Excel
    print(f"[+] Menulis output: {output_file}")
    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name=args.sheet_name)

    print(f"[✓] Selesai. Output dibuat: {output_file.resolve()}")


if __name__ == "__main__":
    main()
