# -*- coding: utf-8 -*-
"""
브리프 → 웹 인터랙티브 덱 자동 생성기.
같은 렌더러(index.html)에 deck.config.js(데이터)만 갈아끼워, 브리프마다 다른 덱을 만든다.

사용:
  python3 generate_deck.py brief.json 출력폴더        # 브리프 파일로 생성
  python3 generate_deck.py                            # 인자 없으면 물빛 데모 생성 (프루프)

브리프(JSON) 구조 = window.DECK 와 동일. 단, 이미지 필드는 '원본 절대경로'를 넣으면
생성기가 출력폴더/assets 로 복사하고 상대경로(assets/파일명)로 바꿔준다.
  - type 'kv' 슬라이드: images: ["/abs/a.png", ...]
  - type 'ba' 슬라이드: before, after: "/abs/x.png"
"""
import os, sys, json, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
RENDERER = os.path.join(HERE, "index.html")


def _relink(path, assets_dir, seen):
    """원본 이미지를 assets_dir로 복사하고 상대경로(assets/파일명) 반환."""
    if not path or path.startswith("assets/"):
        return path  # 이미 상대경로면 그대로
    src = path if os.path.isabs(path) else os.path.join(HERE, path)
    base = os.path.basename(src)
    # 이름 충돌 방지
    name, ext = os.path.splitext(base)
    final = base; i = 1
    while final in seen and seen[final] != src:
        final = f"{name}_{i}{ext}"; i += 1
    seen[final] = src
    dst = os.path.join(assets_dir, final)
    if os.path.abspath(src) != os.path.abspath(dst):
        shutil.copy(src, dst)
    return "assets/" + final


def generate(brief, out_dir):
    assets = os.path.join(out_dir, "assets")
    os.makedirs(assets, exist_ok=True)
    seen = {}
    for s in brief.get("slides", []):
        if s.get("type") == "kv" and "images" in s:
            s["images"] = [_relink(p, assets, seen) for p in s["images"]]
        if s.get("type") == "ba":
            if "before" in s: s["before"] = _relink(s["before"], assets, seen)
            if "after" in s:  s["after"] = _relink(s["after"], assets, seen)
        if s.get("type") == "grid" and "items" in s:
            for it in s["items"]:
                if "img" in it: it["img"] = _relink(it["img"], assets, seen)
        if "video" in s:
            s["video"] = _relink(s["video"], assets, seen)
        if s.get("type") == "cover" and "img" in s:
            s["img"] = _relink(s["img"], assets, seen)
        if s.get("type") == "feature" and "img" in s:
            s["img"] = _relink(s["img"], assets, seen)
        if s.get("type") == "showcase" and "shot" in s:
            s["shot"] = _relink(s["shot"], assets, seen)
        if "poster" in s:
            s["poster"] = _relink(s["poster"], assets, seen)
        if "bgimg" in s:
            s["bgimg"] = _relink(s["bgimg"], assets, seen)
    # deck.config.js
    with open(os.path.join(out_dir, "deck.config.js"), "w", encoding="utf-8") as f:
        f.write("window.DECK = " + json.dumps(brief, ensure_ascii=False, indent=2) + ";\n")
    # 렌더러 복사
    shutil.copy(RENDERER, os.path.join(out_dir, "index.html"))
    return out_dir


# ---- 데모 브리프 (이미지 없이 텍스트만으로 스타일 증명 · 어디서든 크래시 없이 실행) ----
# 실제 사용 땐 brief.json을 만들어 인자로 넘긴다. 이 데모는 "잘 도나?" 확인용 샘플일 뿐.
DEMO_BRIEF = {
    "title": "샘플 제안서 웹 덱",
    "theme": {"bg": "#0f1620", "accent": "#7fc7e8", "red": "#3a86c8"},
    "slides": [
        {"type": "core", "bg": "hero", "kicker": "SAMPLE · 표지",
         "lines": [["말 한마디면,", False], ["제안서 한 벌.", True]],
         "sub": "이미지 없이 텍스트·타이포·애니만으로도 이만큼 나온다"},
        {"type": "core", "kicker": "SECTION 01 · 문제",
         "lines": [["파워포인트,", False], ["아직도 그거예요?", True]],
         "sub": "무겁고, 안 열리고, 안 움직인다"},
        {"type": "stat", "kicker": "WHY WEBDECK", "product": "webdeck", "to": 100,
         "label": "% 브라우저면 어디서든 열림"},
        {"type": "contrast", "kicker": "CREATIVE CONCEPT",
         "leftHead": "PPT", "rightHead": "WEBDECK",
         "rows": [["무거운", "→", "가벼운"],
                  ["멈춘", "→", "움직이는"],
                  ["설치 필요", "→", "링크 하나"]],
         "footer": "HTML 한 파일로 끝"},
        {"type": "ending", "kicker": "THE END",
         "lines": [["당신 브리프로,", False], ["이렇게.", True]],
         "foot": "webdeck · 이건 샘플입니다 (brief.json을 넘겨 당신 덱을 만드세요)"}
    ]
}


if __name__ == "__main__":
    if len(sys.argv) >= 3:
        brief = json.load(open(sys.argv[1], encoding="utf-8"))
        out = sys.argv[2]
    else:
        brief = DEMO_BRIEF
        out = os.path.normpath(os.path.join(HERE, "..", "web_deck_demo"))
    generate(brief, out)
    print("GENERATED:", out)
    print("  index.html + deck.config.js + assets/")
