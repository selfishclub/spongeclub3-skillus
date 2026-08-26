# daily-log — Claude Code 대화·작업 로그 저장 스킬

Claude Code로 나눈 **대화·코드·명령**을 **날짜별 폴더**에 정리해
**MD / HTML / PDF** 로 저장해 주는 스킬입니다.

> Claude Code는 원래 모든 세션을 자동으로 기록합니다(`~/.claude/projects/...`).
> 이 스킬은 그 기록을 **사람이 읽기 좋은 로그 파일**로 바꿔 줍니다.

---

## 무엇이 되나요

- 🗂 **날짜별 저장**: `내프로젝트/logs/20260704/` 처럼 날짜 폴더에 정리
- 📝 **3가지 형식**: MD(글자) · HTML(브라우저용) · PDF(한글 완벽 렌더링)
- 🧑‍💻 **구분 정리**: 내 입력 / Claude 답변 / 도구 실행이 시간순으로
- ⏱ **자동 저장**: `/loop` 와 조합해 30분·1시간마다 자동 (아래 참고)

---

## 준비물 (딱 2가지)

1. **Claude Code** (이 스킬을 쓰는 프로그램)
2. **Python 3.8 이상** — 터미널에서 `python --version` 으로 확인
   - PDF를 만들 때 필요한 `reportlab` 은 **스킬이 처음 1회 자동 설치**합니다(인터넷 필요).
   - 한글 PDF 폰트는 Windows(바탕/굴림)·macOS·Linux(나눔/노토) 기본 폰트를 자동으로 찾습니다.

> MD·HTML만 쓸 거라면 `reportlab` 없이도 바로 됩니다.

---

## 설치 방법 (둘 중 하나 선택)

### 방법 A. 자동 설치 스크립트 (가장 쉬움)

내려받은 폴더 안에서:

- **Windows (PowerShell)**: `install.ps1` 파일에서 마우스 오른쪽 → "PowerShell에서 실행"
  또는 터미널에서:
  ```powershell
  powershell -ExecutionPolicy Bypass -File install.ps1
  ```
- **macOS / Linux (터미널)**:
  ```bash
  bash install.sh
  ```

스크립트가 스킬을 `~/.claude/skills/daily-log/` 로 복사합니다. 끝!

### 방법 B. 손으로 복사

`daily-log` 폴더(SKILL.md + scripts 포함)를 통째로 아래 위치에 넣습니다:

- Windows: `C:\Users\<사용자>\.claude\skills\daily-log\`
- macOS/Linux: `~/.claude/skills/daily-log/`

---

## 사용 방법 (그냥 말로 시키면 됩니다)

Claude Code 창에서:

| 이렇게 말하면 | 결과 |
|---|---|
| "오늘 로그 정리해줘" | 오늘 대화를 `logs/오늘날짜/` 에 저장 |
| "이번 세션만 저장" | 지금 대화만 |
| "전체 로그 저장" | 지금까지 전부 |
| "PDF로도 뽑아줘" | MD + HTML + PDF |
| "6월 28일 로그" | 그날 것만 |

직접 명령으로 쓰려면:
```bash
python ~/.claude/skills/daily-log/scripts/build_log.py --date today --format md,html,pdf
```

### 자동 저장 (선택)

Claude Code 기본 기능 `/loop` 와 조합:
```
/loop 30m 로그 정리해줘      # 30분마다
/loop 1h 로그 정리해줘       # 1시간마다
```
(창이 켜져 있는 동안 반복됩니다.)

---

## 자주 있는 문제

- **"python 을 찾을 수 없음"** → Python을 설치하세요(python.org). 설치 시 "Add to PATH" 체크.
- **PDF 한글이 깨짐** → 한글 폰트를 못 찾은 경우입니다. HTML을 브라우저에서 열어 `Ctrl+P → PDF로 저장` 하세요.
- **저장할 대화가 없다고 나옴** → 해당 날짜에 그 폴더에서 작업한 기록이 없는 경우입니다. `--date all` 로 확인해 보세요.

---

## 주의

로그에는 대화 전문이 담깁니다. 민감 정보가 포함될 수 있으니 공유 전 확인하세요.
