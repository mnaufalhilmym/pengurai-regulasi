import argparse
import json
from pathlib import Path
import pandas as pd


def parse_args():
    parser = argparse.ArgumentParser(
        description="Convert JSON regulasi menjadi spreadsheet Excel"
    )

    parser.add_argument("input", type=Path, help="Path ke file JSON input")
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
    input_path = args.input

    if not input_path.exists():
        raise FileNotFoundError(f"File tidak ditemukan: {input_path}")

    if input_path.suffix.lower() != ".json":
        raise ValueError("File input harus berekstensi .json")

    output_file = args.output or input_path.with_suffix(".xlsx")

    # Load JSON
    print(f"[+] Membaca JSON: {args.pdf}")
    with input_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("Root JSON harus berupa list of objects")

    # Convert ke DataFrame
    print("[+] Parsing struktur JSON...")
    df = pd.DataFrame(data)

    # Write ke Excel
    print(f"[+] Menulis output: {output_file}")
    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name=args.sheet_name)

    print(f"[✓] Selesai. Output dibuat: {output_file.resolve()}")


if __name__ == "__main__":
    main()
