#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
daily-log 빌더
Claude Code 세션 원본(.jsonl transcript)을 읽어
날짜별 폴더에 사람이 읽기 좋은 MD / HTML (선택적으로 PDF) 로그로 저장한다.

의존성 없음(순수 표준 라이브러리). Windows/Mac/Linux 공용.

사용 예:
  python build_log.py                         # 현재 프로젝트, 오늘 날짜, md+html
  python build_log.py --date all              # 전체 기간
  python build_log.py --date 20260704         # 특정 날짜
  python build_log.py --session latest        # 가장 최근 세션만
  python build_log.py --format md,html,pdf    # PDF까지 시도
  python build_log.py --out "D:/backup/logs"  # 저장 위치 지정
"""
import argparse
import glob
import html as htmllib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

HOME = os.path.expanduser("~")
PROJECTS_BASE = os.path.join(HOME, ".claude", "projects")

# Windows 콘솔(cp949)에서도 이모지/한글이 깨지지 않도록 UTF-8 강제
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def log(msg):
    print(msg, flush=True)


def find_transcripts_dir(target_cwd):
    """~/.claude/projects 하위에서 target_cwd에 해당하는 세션 폴더를 찾는다."""
    if not os.path.isdir(PROJECTS_BASE):
        return None
    target_norm = os.path.normcase(os.path.normpath(target_cwd))
    candidates = []
    for name in os.listdir(PROJECTS_BASE):
        d = os.path.join(PROJECTS_BASE, name)
        if not os.path.isdir(d):
            continue
        # 폴더 안 아무 .jsonl 한 줄에서 cwd를 읽어 매칭
        for jf in glob.glob(os.path.join(d, "*.jsonl")):
            cwd = _peek_cwd(jf)
            if cwd:
                if os.path.normcase(os.path.normpath(cwd)) == target_norm:
                    return d
                candidates.append((d, cwd))
                break
    # 정확 매칭 실패 시, 인코딩 규칙으로 추정
    guess = _encode_path(target_cwd)
    gdir = os.path.join(PROJECTS_BASE, guess)
    if os.path.isdir(gdir):
        return gdir
    return None


def _peek_cwd(jsonl_path):
    try:
        with open(jsonl_path, "r", encoding="utf-8") as f:
            for _ in range(30):
                line = f.readline()
                if not line:
                    break
                try:
                    obj = json.loads(line)
                except Exception:
                    continue
                if isinstance(obj, dict) and obj.get("cwd"):
                    return obj["cwd"]
    except Exception:
        return None
    return None


def _encode_path(p):
    out = []
    for ch in p:
        out.append(ch if (ch.isalnum()) else "-")
    return "".join(out)


def parse_timestamp(ts):
    if not ts:
        return None
    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return dt.astimezone()  # 로컬 시간대로 변환
    except Exception:
        return None


def extract_blocks(content):
    """message.content(문자열 또는 블록 리스트)에서 (kind, text) 조각들을 뽑는다."""
    pieces = []
    if content is None:
        return pieces
    if isinstance(content, str):
        t = content.strip()
        if t:
            pieces.append(("text", t))
        return pieces
    if isinstance(content, list):
        for b in content:
            if not isinstance(b, dict):
                continue
            bt = b.get("type")
            if bt == "text":
                t = (b.get("text") or "").strip()
                if t:
                    pieces.append(("text", t))
            elif bt == "tool_use":
                name = b.get("name", "tool")
                inp = b.get("input", {})
                summary = _summarize_tool_input(name, inp)
                pieces.append(("tool_use", f"🔧 {name}{summary}"))
            elif bt == "tool_result":
                pieces.append(("tool_result", "↳ (도구 실행 결과)"))
            elif bt == "thinking":
                pass  # 사고 과정은 로그에서 생략
    return pieces


def _summarize_tool_input(name, inp):
    if not isinstance(inp, dict):
        return ""
    for key in ("command", "file_path", "path", "pattern", "query", "prompt", "url"):
        if key in inp and isinstance(inp[key], str):
            v = inp[key].replace("\n", " ")
            if len(v) > 100:
                v = v[:100] + "…"
            return f" — {v}"
    return ""


def load_events(transcripts_dir, session_filter):
    """세션 파일들에서 user/assistant 이벤트를 시간순으로 모은다."""
    files = sorted(glob.glob(os.path.join(transcripts_dir, "*.jsonl")))
    if session_filter == "latest" and files:
        files = [max(files, key=lambda p: os.path.getmtime(p))]
    events = []
    for jf in files:
        sid = os.path.splitext(os.path.basename(jf))[0]
        try:
            with open(jf, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        obj = json.loads(line)
                    except Exception:
                        continue
                    if not isinstance(obj, dict):
                        continue
                    typ = obj.get("type")
                    if typ not in ("user", "assistant"):
                        continue
                    msg = obj.get("message") or {}
                    role = msg.get("role", typ)
                    content = msg.get("content")
                    pieces = extract_blocks(content)
                    if not pieces:
                        continue
                    # 사람이 실제 입력한 user만 선명하게 표시(도구 결과 user턴은 축약)
                    origin = obj.get("origin") or {}
                    is_human = (role == "user") and (
                        isinstance(content, str) or origin.get("kind") == "human"
                    )
                    dt = parse_timestamp(obj.get("timestamp"))
                    events.append({
                        "session": sid,
                        "role": role,
                        "is_human": is_human,
                        "pieces": pieces,
                        "dt": dt,
                    })
        except Exception as e:
            log(f"  (경고) {os.path.basename(jf)} 읽기 실패: {e}")
    events.sort(key=lambda e: (e["dt"] or datetime.min.replace(tzinfo=timezone.utc)))
    return events


def filter_by_date(events, date_sel):
    if date_sel == "all":
        return events
    if date_sel == "today":
        target = datetime.now().astimezone().strftime("%Y%m%d")
    else:
        target = date_sel
    out = []
    for e in events:
        if e["dt"] and e["dt"].strftime("%Y%m%d") == target:
            out.append(e)
    return out


def role_label(e):
    if e["role"] == "user":
        return "🧑 나" if e["is_human"] else "🧑 나(도구결과)"
    return "🤖 Claude"


def render_md(events, title):
    lines = [f"# {title}", ""]
    lines.append(f"- 생성: {datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"- 대화 수: {len(events)}개 메시지")
    lines.append("")
    lines.append("---")
    lines.append("")
    cur_session = None
    for e in events:
        if e["session"] != cur_session:
            cur_session = e["session"]
            lines.append(f"\n## 🗂 세션 `{cur_session[:8]}`\n")
        ts = e["dt"].strftime("%H:%M:%S") if e["dt"] else "--:--:--"
        lines.append(f"### {role_label(e)}  ·  {ts}")
        lines.append("")
        for kind, text in e["pieces"]:
            if kind == "text":
                lines.append(text)
                lines.append("")
            elif kind == "tool_use":
                lines.append(f"> {text}")
                lines.append("")
            elif kind == "tool_result":
                lines.append(f"> {text}")
                lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_html(events, title):
    def esc(s):
        return htmllib.escape(s)
    rows = []
    cur_session = None
    for e in events:
        if e["session"] != cur_session:
            cur_session = e["session"]
            rows.append(f'<h2 class="sess">🗂 세션 <code>{esc(cur_session[:8])}</code></h2>')
        ts = e["dt"].strftime("%H:%M:%S") if e["dt"] else "--:--:--"
        cls = "user" if e["role"] == "user" else "assistant"
        body = []
        for kind, text in e["pieces"]:
            if kind == "text":
                body.append(f'<p>{esc(text).replace(chr(10), "<br>")}</p>')
            else:
                body.append(f'<p class="tool">{esc(text)}</p>')
        rows.append(
            f'<div class="msg {cls}"><div class="meta">{esc(role_label(e))} '
            f'<span class="ts">{ts}</span></div><div class="content">{"".join(body)}</div></div>'
        )
    now = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S")
    return f"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<style>
:root {{ color-scheme: light dark; }}
* {{ box-sizing: border-box; }}
body {{ font-family: -apple-system, "Segoe UI", "Malgun Gothic", sans-serif;
  max-width: 860px; margin: 0 auto; padding: 24px; line-height: 1.6;
  background: #f7f7f8; color: #1a1a1a; }}
h1 {{ font-size: 22px; }}
.head {{ color: #666; font-size: 13px; margin-bottom: 20px; }}
.sess {{ font-size: 15px; color: #555; border-bottom: 1px solid #ddd;
  padding-bottom: 6px; margin-top: 32px; }}
.msg {{ margin: 14px 0; padding: 12px 16px; border-radius: 12px; }}
.msg.user {{ background: #e7f0ff; }}
.msg.assistant {{ background: #fff; border: 1px solid #eee; }}
.meta {{ font-weight: 600; font-size: 13px; margin-bottom: 6px; }}
.ts {{ color: #999; font-weight: 400; margin-left: 8px; }}
.content p {{ margin: 6px 0; white-space: normal; word-break: break-word; }}
.content p.tool {{ color: #7a5; font-family: monospace; font-size: 13px; }}
code {{ background: #eee; padding: 1px 5px; border-radius: 4px; }}
@media print {{ body {{ background: #fff; }} .msg.assistant {{ border-color: #ccc; }} }}
</style></head>
<body>
<h1>{esc(title)}</h1>
<div class="head">생성 {now} · 메시지 {len(events)}개</div>
{"".join(rows)}
</body></html>
"""


def _ensure_reportlab():
    """reportlab가 없으면 자동으로 pip 설치를 시도한다. 성공 시 True."""
    try:
        import reportlab  # noqa
        return True
    except Exception:
        pass
    log("   📦 PDF 엔진(reportlab)이 없어 자동 설치를 시도합니다… (처음 1회, 30~60초)")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", "reportlab"],
                       timeout=180)
        import importlib
        importlib.invalidate_caches()
        import reportlab  # noqa
        return True
    except Exception:
        log("   ⚠️ reportlab 자동 설치 실패. 인터넷 연결을 확인하거나 "
            "'pip install reportlab' 를 직접 실행하세요.")
        return False


def _register_korean_font():
    """한글 TTF를 PDF에 임베드용으로 등록. 성공 시 폰트명 반환, 없으면 None."""
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    # (파일경로, subfontIndex) — Windows batang이 reportlab 임베드에 가장 안정적
    candidates = [
        # Windows
        (r"C:\Windows\Fonts\batang.ttc", 0),
        (r"C:\Windows\Fonts\gulim.ttc", 0),
        (r"C:\Windows\Fonts\malgun.ttf", None),
        # macOS
        ("/System/Library/Fonts/Supplemental/AppleGothic.ttf", None),
        ("/Library/Fonts/AppleGothic.ttf", None),
        ("/System/Library/Fonts/AppleSDGothicNeo.ttc", 0),
        # Linux (나눔/노토)
        ("/usr/share/fonts/truetype/nanum/NanumGothic.ttf", None),
        ("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", 1),
        ("/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc", 1),
    ]
    for path, idx in candidates:
        if os.path.exists(path):
            try:
                if idx is None:
                    pdfmetrics.registerFont(TTFont("KFont", path))
                else:
                    pdfmetrics.registerFont(TTFont("KFont", path, subfontIndex=idx))
                return "KFont"
            except Exception:
                continue
    return None


def _pdf_role_label(e):
    # PDF용: 이모지 제거(임베드 폰트에 이모지 글리프가 없음)
    if e["role"] == "user":
        return "[나]" if e["is_human"] else "[나·도구결과]"
    return "[Claude]"


def try_pdf_reportlab(events, title, pdf_path):
    """reportlab로 한글 폰트를 임베드하여 PDF 직접 생성. 성공 시 True."""
    if not _ensure_reportlab():
        return False
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import mm
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    except Exception:
        return False
    font = _register_korean_font()
    if not font:
        log("   ⚠️ 한글 폰트를 찾지 못해 PDF의 한글이 깨질 수 있습니다. "
            "HTML을 대신 사용하세요.")
        return False

    def esc(s):
        s = "".join(ch for ch in s if ord(ch) < 0x1F000)  # 이모지 제거
        s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        return s.replace("\n", "<br/>")

    st_title = ParagraphStyle("t", fontName=font, fontSize=16, leading=20, spaceAfter=4)
    st_head = ParagraphStyle("h", fontName=font, fontSize=9, textColor="#777", spaceAfter=10)
    st_sess = ParagraphStyle("s", fontName=font, fontSize=12, textColor="#444",
                             spaceBefore=14, spaceAfter=6)
    st_meta = ParagraphStyle("m", fontName=font, fontSize=10, textColor="#222",
                             spaceBefore=8, spaceAfter=2)
    st_text = ParagraphStyle("x", fontName=font, fontSize=9.5, leading=14, leftIndent=10)
    st_tool = ParagraphStyle("o", fontName=font, fontSize=9, leading=13, leftIndent=10,
                             textColor="#3a8a3a")
    now = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S")

    story = [Paragraph(esc(title), st_title),
             Paragraph(f"생성 {now} · 메시지 {len(events)}개", st_head)]
    cur = None
    for e in events:
        if e["session"] != cur:
            cur = e["session"]
            story.append(Paragraph(f"■ 세션 {esc(cur[:8])}", st_sess))
        ts = e["dt"].strftime("%H:%M:%S") if e["dt"] else "--:--:--"
        story.append(Paragraph(f"<b>{esc(_pdf_role_label(e))}</b>  {ts}", st_meta))
        for kind, text in e["pieces"]:
            story.append(Paragraph(esc(text), st_text if kind == "text" else st_tool))
    try:
        doc = SimpleDocTemplate(pdf_path, pagesize=A4,
                                leftMargin=18 * mm, rightMargin=18 * mm,
                                topMargin=16 * mm, bottomMargin=16 * mm,
                                title=title)
        doc.build(story)
        return os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 0
    except Exception:
        return False


def try_pdf_from_html(html_path, pdf_path):
    """Chrome/Edge 헤드리스로 HTML→PDF 시도. 성공 시 True."""
    browsers = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        shutil.which("chrome") or "",
        shutil.which("chromium") or "",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    ]
    file_url = "file:///" + os.path.abspath(html_path).replace("\\", "/")
    for b in browsers:
        if not b or not os.path.exists(b):
            continue
        prof = tempfile.mkdtemp(prefix="dl_chrome_")
        try:
            subprocess.run(
                [b, "--headless=new", "--disable-gpu", "--no-first-run",
                 "--no-pdf-header-footer", f"--user-data-dir={prof}",
                 f"--print-to-pdf={os.path.abspath(pdf_path)}", file_url],
                timeout=20, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )
        except Exception:
            pass
        finally:
            shutil.rmtree(prof, ignore_errors=True)
        if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 0:
            return True
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cwd", default=os.getcwd())
    ap.add_argument("--transcripts-dir", default=None)
    ap.add_argument("--out", default=None, help="로그 저장 루트 (기본: <cwd>/logs)")
    ap.add_argument("--date", default="today", help="today | all | YYYYMMDD")
    ap.add_argument("--session", default="all", help="all | latest")
    ap.add_argument("--format", default="md,html", help="md,html,pdf 조합")
    args = ap.parse_args()

    tdir = args.transcripts_dir or find_transcripts_dir(args.cwd)
    if not tdir or not os.path.isdir(tdir):
        log("❌ 세션 기록 폴더를 찾지 못했습니다. --transcripts-dir 로 직접 지정해 주세요.")
        log(f"   (찾은 위치 예상: {PROJECTS_BASE})")
        sys.exit(1)
    log(f"📂 세션 기록 폴더: {tdir}")

    events = load_events(tdir, args.session)
    events = filter_by_date(events, args.date)
    if not events:
        log(f"⚠️  '{args.date}' 범위에 저장할 대화가 없습니다.")
        sys.exit(0)

    date_tag = (datetime.now().astimezone().strftime("%Y%m%d")
                if args.date == "today" else args.date)
    out_root = args.out or os.path.join(args.cwd, "logs")
    out_dir = os.path.join(out_root, date_tag if date_tag != "all" else "all")
    os.makedirs(out_dir, exist_ok=True)
    title = f"작업 로그 · {date_tag}"

    formats = [f.strip().lower() for f in args.format.split(",") if f.strip()]
    made = []

    md_path = os.path.join(out_dir, f"log-{date_tag}.md")
    html_path = os.path.join(out_dir, f"log-{date_tag}.html")

    if "md" in formats or "pdf" in formats:
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(render_md(events, title))
        if "md" in formats:
            made.append(md_path)
    if "html" in formats or "pdf" in formats:
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(render_html(events, title))
        if "html" in formats:
            made.append(html_path)
    if "pdf" in formats:
        pdf_path = os.path.join(out_dir, f"log-{date_tag}.pdf")
        log("🖨  PDF 변환 시도 중…")
        ok = try_pdf_reportlab(events, title, pdf_path)
        if not ok:
            log("   (reportlab 없음/실패 → 브라우저 방식 시도)")
            ok = try_pdf_from_html(html_path, pdf_path)
        if ok:
            made.append(pdf_path)
        else:
            log("   ⚠️ 자동 PDF 변환 실패. 대신 HTML을 브라우저에서 열고 "
                "Ctrl+P → '대상: PDF로 저장'을 쓰거나, pdf 스킬을 이용하세요.")
            if os.path.exists(html_path) and html_path not in made:
                made.append(html_path)

    log("")
    log(f"✅ 완료! 저장 위치: {out_dir}")
    for m in made:
        log(f"   • {m}")


if __name__ == "__main__":
    main()
