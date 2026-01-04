from utils.patterns import PATTERNS


def parse_articles(lines: list) -> list:
    results = []

    state = {
        "bab": None,
        "judul_bab": None,
        "bagian": None,
        "judul_bagian": None,
        "paragraf": None,
        "judul_paragraf": None,
        "pasal": None,
        "ayat": None,
    }

    for line in lines:
        text = ""

        if PATTERNS["bab_alt"].match(line):
            bab = PATTERNS["bab_alt"].match(line)
            state["bab"] = bab.group(1)
            state["judul_bab"] = bab.group(2)
            continue

        if PATTERNS["bagian_alt"].match(line):
            bagian = PATTERNS["bagian_alt"].match(line)
            state["bagian"] = bagian.group(1)
            state["judul_bagian"] = bagian.group(2)
            continue

        if PATTERNS["paragraf_alt"].match(line):
            paragraf = PATTERNS["paragraf_alt"].match(line)
            state["paragraf"] = paragraf.group(1)
            state["judul_paragraf"] = paragraf.group(2)
            continue

        if PATTERNS["pasal"].match(line):
            pasal = PATTERNS["pasal"].match(line)
            state["pasal"] = pasal.group(1)
            state["ayat"] = None
            continue

        if PATTERNS["ayat_alt"].match(line):
            ayat = PATTERNS["ayat_alt"].match(line)
            state["ayat"] = ayat.group(1)
            text = ayat.group(2)

        if not text:
            text = line

        text = add_newline_before_points(text)

        if state["bab"] and state["pasal"]:
            results.append(
                {
                    "bab": state["bab"],
                    "judul_bab": state["judul_bab"],
                    "bagian": state["bagian"],
                    "judul_bagian": state["judul_bagian"],
                    "paragraf": state["paragraf"],
                    "judul_paragraf": state["judul_paragraf"],
                    "pasal": state["pasal"],
                    "ayat": state["ayat"],
                    "teks": text,
                }
            )

        if PATTERNS["end_of_articles"].match(line):
            break

    return results


def add_newline_before_points(text: str) -> str:
    import regex

    patterns = [
        r"(?<!huruf)\s(?=[a-z]\.)",  # a. b. c.
        r"(?<!(pasal|nomor|rp))\s(?=\d+\.)",  # 1. 2. 3.
        r"(?<!huruf)\s(?=[a-z]\))",  # a) b)
        r"(?<!(pasal|nomor))\s(?=\d+\))",  # 1) 2)
    ]

    for p in patterns:
        text = regex.sub(p, "\n", text, flags=regex.I)

    return text
