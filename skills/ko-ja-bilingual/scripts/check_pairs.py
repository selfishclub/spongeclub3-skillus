#!/usr/bin/env python3
"""ko/ja 토글 HTML 검증. 0 findings 가 통과.

검출 항목
  default   : <html lang> 또는 data-lang 초기값이 ja 가 아님 / 토글 CSS 규칙이 없음
  key       : localStorage 키가 템플릿 플레이스홀더(DECK_LANG_KEY / DOC_LANG_KEY) 그대로임
  pair      : 같은 부모 안에서 .x-ja 와 .x-ko 개수가 다름
  empty     : .x-ja / .x-ko 가 비어 있음
  mixed     : .x-ko 안에 가나, 또는 .x-ja 안에 한글이 섞여 있음
  untagged  : 한글·가나 텍스트가 x-ja/x-ko 밖에 그대로 있음 (한 언어로만 보이는 텍스트)

사용:  python3 check_pairs.py file.html [--json]
"""
import json
import re
import sys
from html.parser import HTMLParser

HANGUL = re.compile(r"[가-힣]")
KANA = re.compile(r"[぀-ヿ]")
SKIP_TAGS = {"script", "style", "title", "svg", "button"}  # button: 토글 라벨 자체


class Checker(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.findings = []
        self.stack = []          # [(tag, lang or None, id)]
        self.counts = {}         # parent id -> {"ja": n, "ko": n}
        self.text = {}           # span id -> collected text
        self.skip = 0
        self.nid = 0
        self.lines = {}          # id -> line

    def _lang_of(self, attrs):
        cls = dict(attrs).get("class", "") or ""
        parts = cls.split()
        if "x-ja" in parts:
            return "ja"
        if "x-ko" in parts:
            return "ko"
        return None

    def handle_starttag(self, tag, attrs):
        if tag in SKIP_TAGS:
            self.skip += 1
        self.nid += 1
        self.lines[self.nid] = self.getpos()[0]
        lang = self._lang_of(attrs)
        if lang:
            parent = self.stack[-1][2] if self.stack else 0
            self.counts.setdefault(parent, {"ja": 0, "ko": 0})[lang] += 1
            self.text[self.nid] = ""
        self.stack.append((tag, lang, self.nid))
        if tag in ("br", "img", "meta", "link", "input", "hr"):
            self.stack.pop()

    def handle_endtag(self, tag):
        if tag in SKIP_TAGS:
            self.skip = max(0, self.skip - 1)
        for k in range(len(self.stack) - 1, -1, -1):
            if self.stack[k][0] == tag:
                _, lang, sid = self.stack[k]
                if lang:
                    t = self.text.get(sid, "").strip()
                    if not t:
                        self.findings.append(("empty", self.lines[sid], f".x-{lang} 가 비어 있음"))
                    elif lang == "ko" and KANA.search(t):
                        self.findings.append(("mixed", self.lines[sid], f".x-ko 안에 가나: {t[:40]}"))
                    elif lang == "ja" and HANGUL.search(t):
                        self.findings.append(("mixed", self.lines[sid], f".x-ja 안에 한글: {t[:40]}"))
                del self.stack[k:]
                break

    def handle_data(self, data):
        if self.skip:
            return
        inside = [s for s in self.stack if s[1]]
        if inside:
            self.text[inside[-1][2]] = self.text.get(inside[-1][2], "") + data
            return
        t = data.strip()
        if t and (HANGUL.search(t) or KANA.search(t)):
            self.findings.append(("untagged", self.getpos()[0], f"span 밖 텍스트: {t[:40]}"))


def check(path):
    src = open(path, encoding="utf-8").read()
    c = Checker()
    c.feed(src)
    f = c.findings
    for parent, n in c.counts.items():
        if n["ja"] != n["ko"]:
            f.append(("pair", c.lines.get(parent, 0), f"x-ja {n['ja']}개 / x-ko {n['ko']}개 (부모 요소 기준)"))
    if not re.search(r'<html[^>]*\blang="ja"', src):
        f.append(("default", 0, '<html lang="ja"> 가 아님'))
    if ".x-ko{display:none}" not in src.replace(" ", ""):
        f.append(("default", 0, "토글 CSS (.x-ko{display:none}) 없음"))
    if re.search(r"getItem\(KEY\)\|\|'ko'|saved='ko'", src):
        f.append(("default", 0, "JS 기본 언어가 ko"))
    for ph in ("DECK_LANG_KEY", "DOC_LANG_KEY"):
        if ph in src:
            f.append(("key", 0, f"localStorage 키가 플레이스홀더 {ph} 그대로"))
    return sorted(f, key=lambda x: (x[1], x[0]))


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    findings = check(sys.argv[1])
    if "--json" in sys.argv:
        print(json.dumps([{"type": t, "line": l, "msg": m} for t, l, m in findings], ensure_ascii=False, indent=1))
    else:
        for t, l, m in findings:
            print(f"{t:9s} L{l:<5d} {m}")
        print(f"\n{len(findings)} findings")
    sys.exit(1 if findings else 0)


if __name__ == "__main__":
    main()
