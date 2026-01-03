from utils.patterns import PATTERNS


def normalize_text(text: str) -> list:
    lines = []

    buffer = ""

    last_ayat = 0
    last_ayat_whitespace = 0
    split_end_of_articles = False

    for raw_line in text.splitlines():
        line = raw_line.strip()
        line = PATTERNS["multi_whitespace"].sub(" ", line)
        line = PATTERNS["page_marker"].sub("", line)

        if not line:
            if split_end_of_articles:
                if buffer:
                    lines.append(buffer.strip())
                    lines.append("")
                    buffer = ""
                split_end_of_articles = False
            continue

        if PATTERNS["bab"].match(line):
            if buffer:
                lines.append(buffer.strip())
                buffer = ""
        elif PATTERNS["bagian"].match(line):
            if buffer:
                lines.append(buffer.strip())
                buffer = ""
        elif PATTERNS["paragraf"].match(line):
            if buffer:
                lines.append(buffer.strip())
                buffer = ""
        elif PATTERNS["pasal"].match(line):
            if buffer:
                lines.append(buffer.strip())
                buffer = ""
            lines.append(line)
            continue
        elif PATTERNS["ayat"].match(line):
            nomor_ayat = int(PATTERNS["ayat"].match(line).group(1))
            if not buffer and nomor_ayat == 1:
                last_ayat = nomor_ayat
                last_ayat_whitespace = count_whitespace_before(raw_line, "(")
            if nomor_ayat > 1 and last_ayat + 1 == nomor_ayat:
                ayat_whitespace = count_whitespace_before(raw_line, "(")
                if abs(last_ayat_whitespace - ayat_whitespace) <= 2:
                    lines.append(buffer.strip())
                    buffer = ""
                    last_ayat = nomor_ayat

        if buffer and not buffer.endswith("-"):
            buffer += " "
        buffer += line

        if PATTERNS["end_of_articles"].match(buffer):
            split_end_of_articles = True

    if buffer:
        lines.append(buffer.strip())

    return lines


def count_whitespace_before(s, char):
    import re

    pattern = rf"(\s*){re.escape(char)}"
    match = re.match(pattern, s)
    if match:
        return len(match.group(1))
    return 0
