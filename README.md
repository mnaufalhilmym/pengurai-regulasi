# Pengurai Regulasi _(Regulation Parser)_

Parser ini dirancang untuk mengekstrak struktur dan isi peraturan perundang-undangan Indonesia secara otomatis dari file PDF menjadi JSON atau spreadsheet. Program ini membantu analisis hukum, penyusunan ringkasan, dan pembuatan database regulasi.

_(This parser is designed to automatically extract the structure and content of Indonesian laws and regulations from PDF file into JSON or spreadsheets. The program assists in legal analysis, summary preparation, and the creation of regulatory databases.)_

## Fitur

- Mendukung parsing dokumen PDF peraturan Indonesia.
- Mendeteksi struktur hierarki regulasi:
  - Bab, Bagian, Pasal, Ayat
  - Sub-poin (a., b., c., 1., 2., 3.)
- Menyimpan hasil output ke format JSON atau spreadsheet.
- Bersih dari noise seperti penanda halaman atau double space.

## Instalasi

1. Clone repository:

```bash
git clone git@github.com:mnaufalhilmym/pengurai-regulasi.git
cd pengurai-regulasi
```

2. Buat virtual environment (opsional tapi disarankan):

```bash
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Penggunaan

### Menggunakan CLI

Program mendukung argparser sehingga bisa dijalankan langsung dari terminal:

```bash
python -m scripts.extract_articles_to_json file_peraturan.pdf --output file_peraturan.json
```

### Contoh Output

Struktur JSON hasil parsing:

```json
[
  {
    "bab": "II",
    "judul_bab": "KETENTUAN PELINDUNGAN KONSUMEN DAN MASYARAKAT DI SEKTOR JASA KEUANGAN",
    "bagian": "Kedua",
    "judul_bagian": "Perilaku Dasar PUJK",
    "paragraf": "1",
    "judul_paragraf": "Umum",
    "pasal": "4",
    "ayat": "1",
    "teks": "PUJK wajib beriktikad baik dalam melakukan kegiatan usaha dan/atau memberikan produk dan/atau layanan kepada calon Konsumen dan/atau Konsumen."
  }
]
```
