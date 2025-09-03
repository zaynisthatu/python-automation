#!/usr/bin/env python3
"""
split_lectures.py

Splits a large text file into separate files at "Lesson # X" headings.
Heuristics try to skip TOC entries.
"""

import re
import os
import argparse
import sys

def looks_like_toc(line: str) -> bool:
    """Return True if a line looks like a Table-of-Contents entry."""
    if not line:
        return False
    # Common TOC pattern: a run of dots followed by a page number at end
    if re.search(r'\.{3,}\s*\d+\s*$', line):
        return True
    # Long lines with many dots are likely TOC
    if re.search(r'\.{5,}', line) and len(line) > 60:
        return True
    # explicit table-of-content header
    if re.search(r'table of cont', line, flags=re.IGNORECASE):
        return True
    return False

def safe_filename(s: str, maxlen: int = 80) -> str:
    s = s.strip()
    s = re.sub(r'[\\/*?:"<>|]', '_', s)      # replace illegal chars
    s = re.sub(r'\s+', ' ', s)              # collapse whitespace
    return s[:maxlen].rstrip()

def find_lecture_matches(text: str, pattern: str, allow_toc: bool=False):
    """Return list of (start_index, lecture_number, match_obj) for accepted lecture headers."""
    matches = list(re.finditer(pattern, text, flags=re.IGNORECASE | re.MULTILINE))
    accepted = []
    for m in matches:
        # Extract the whole line where the match sits
        line_start = text.rfind('\n', 0, m.start())
        if line_start == -1:
            line_start = 0
        else:
            line_start += 1
        line_end = text.find('\n', m.start())
        if line_end == -1:
            line_end = len(text)
        line = text[line_start:line_end].strip()

        if not allow_toc and looks_like_toc(line):
            # skip likely TOC entry
            continue

        accepted.append((m.start(), m.group(1), m))
    return accepted

def split_into_files(text: str, matches, outdir: str):
    os.makedirs(outdir, exist_ok=True)
    matches.sort(key=lambda x: x[0])

    for i, (startpos, lecnum, match_obj) in enumerate(matches):
        endpos = matches[i+1][0] if i+1 < len(matches) else len(text)
        segment = text[startpos:endpos].rstrip()

        # find first non-empty line after the header line to use as title
        header_line_end = text.find('\n', match_obj.end())
        if header_line_end == -1:
            header_line_end = match_obj.end()
        after_header = text[header_line_end+1:endpos]
        title = None
        for line in after_header.splitlines():
            if line.strip():
                title = line.strip()
                break
        if not title:
            title = f'Lesson {lecnum}'

        safe_title = safe_filename(title, maxlen=60)
        try:
            lec_int = int(lecnum)
            lec_fmt = f"{lec_int:02d}"
        except Exception:
            lec_fmt = lecnum.zfill(2)

        # <-- CHANGED FILENAME TO USE "Lesson" INSTEAD OF "Lecture"
        filename = f"Lesson_{lec_fmt} - {safe_title}.txt"
        filepath = os.path.join(outdir, filename)
        with open(filepath, "w", encoding="utf-8") as out:
            out.write(segment)
        print(f"WROTE: {filepath}")

def main():
    parser = argparse.ArgumentParser(description="Split a big text into Lesson files by 'Lesson # X' headings.")
    parser.add_argument("input", help="input text file (e.g. full_book.txt)")
    parser.add_argument("-o", "--outdir", default="Split_Lectures", help="output directory")
    parser.add_argument("--allow-toc", action="store_true",
                        help="do not try to skip TOC-like matches")
    parser.add_argument("--pattern", default=None,
                        help="custom regex pattern")
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print("ERROR: input file not found:", args.input)
        sys.exit(1)

    with open(args.input, "r", encoding="utf-8") as f:
        text = f.read()

    # <-- CHANGED PATTERN TO MATCH "Lesson # 01", "lesson # 2", etc.
    default_pattern = r'^[ \t]*Lesson\s+#\s*(\d{1,3})\b'
    pattern = args.pattern if args.pattern else default_pattern

    matches = find_lecture_matches(text, pattern, allow_toc=args.allow_toc)

    if not matches:
        print("No lesson headings found. Try adjusting the --pattern argument.")
        sys.exit(1)

    split_into_files(text, matches, args.outdir)
    print("Done. Files are in:", args.outdir)

if __name__ == "__main__":
    main()