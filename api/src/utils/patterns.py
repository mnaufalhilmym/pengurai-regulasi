import re

PATTERNS = {
    "bab": re.compile(r"^BAB [IVXLC]+$"),
    "bab_alt": re.compile(r"^BAB ([IVXLC]+) +(.+)$"),
    "bagian": re.compile(r"^Bagian [A-Z]\w*$"),
    "bagian_alt": re.compile(r"^Bagian ([A-Z]\w*) +(.+)$"),
    "paragraf": re.compile(r"^Paragraf \d+$"),
    "paragraf_alt": re.compile(r"^Paragraf (\d+) +(.+)$"),
    "pasal": re.compile(r"^Pasal (\d+)$"),
    "ayat": re.compile(r"^\((\d+)\)"),
    "ayat_alt": re.compile(r"^\((\d+)\) +(.+)$"),
    "multi_whitespace": re.compile(r"\s+"),
    "page_marker": re.compile(r"-\s*\d+\s*-"),
    "end_of_articles": re.compile(
        r"""
    .+?\s+ini
    \s+mulai\s+berlaku\s+pada\s+tanggal\s+diundangkan
    .*?
    Agar\s+setiap\s+orang\s+mengetahuinya
    .*?
    memerintahkan\s+pengundangan
    .*?
    ini\s+dengan\s+penempatannya\s+dalam
    """,
        re.IGNORECASE | re.VERBOSE | re.DOTALL,
    ),
}
