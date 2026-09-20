#!/usr/bin/env python3
"""docx → 마크다운. 표준 라이브러리만 사용(pandoc 불필요).

제목 스타일(Heading1~3 / 제목 1~3) → #, 번호·글머리 목록 → -/1., 표 → 마크다운 표,
굵게 → **, 이미지 → [이미지: 파일명] 자리표시. 나머지는 문단.

사용:  python3 docx2md.py input.docx > output.md
"""
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"


def run_text(r):
    out = []
    for el in r.iter():
        if el.tag == W + "t":
            out.append(el.text or "")
        elif el.tag == W + "tab":
            out.append("\t")
        elif el.tag == W + "br":
            out.append("\n")
        elif el.tag == A + "blip":
            out.append("[이미지: %s]" % el.get(R + "embed", ""))
    t = "".join(out)
    rpr = r.find(W + "rPr")
    if t.strip() and rpr is not None and rpr.find(W + "b") is not None:
        t = "**%s**" % t.strip()
    return t


def para_text(p):
    return "".join(run_text(r) for r in p.iter(W + "r")).strip()


def heading_level(p):
    ppr = p.find(W + "pPr")
    if ppr is None:
        return 0
    ps = ppr.find(W + "pStyle")
    if ps is None:
        return 0
    v = (ps.get(W + "val") or "").lower()
    m = re.search(r"(?:heading|title|제목|見出し)\s*(\d)?", v)
    if not m:
        return 0
    return int(m.group(1) or 1)


def list_info(p):
    ppr = p.find(W + "pPr")
    if ppr is None:
        return None
    num = ppr.find(W + "numPr")
    if num is None:
        return None
    lvl = num.find(W + "ilvl")
    return int(lvl.get(W + "val") or 0) if lvl is not None else 0


def table_md(tbl):
    rows = []
    for tr in tbl.iter(W + "tr"):
        cells = []
        for tc in tr.findall(W + "tc"):
            cells.append(" ".join(para_text(p) for p in tc.iter(W + "p")).replace("|", "\\|"))
        rows.append(cells)
    if not rows:
        return ""
    width = max(len(r) for r in rows)
    rows = [r + [""] * (width - len(r)) for r in rows]
    out = ["| " + " | ".join(rows[0]) + " |", "|" + "---|" * width]
    out += ["| " + " | ".join(r) + " |" for r in rows[1:]]
    return "\n".join(out)


def convert(path):
    with zipfile.ZipFile(path) as z:
        root = ET.fromstring(z.read("word/document.xml"))
    body = root.find(W + "body")
    lines = []
    for el in body:
        if el.tag == W + "p":
            t = para_text(el)
            if not t:
                continue
            h = heading_level(el)
            lv = list_info(el)
            if h:
                lines.append("#" * min(h, 6) + " " + t)
            elif lv is not None:
                lines.append("  " * lv + "- " + t)
            else:
                lines.append(t)
            lines.append("")
        elif el.tag == W + "tbl":
            lines.append(table_md(el))
            lines.append("")
    md = "\n".join(lines)
    md = re.sub(r"(\n *- [^\n]*)\n\n(?= *- )", r"\1\n", md)  # 목록 항목 사이 빈 줄 제거
    return md.strip() + "\n"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    sys.stdout.write(convert(sys.argv[1]))
