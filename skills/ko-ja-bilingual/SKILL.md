---
name: ko-ja-bilingual
description: Use when a Korean document already exists and the user wants a Japanese version attached to it with a ko/ja toggle button, delivered as a scrolling web page (claude.ai Artifact) or a 16:9 slide deck (local HTML). Triggers on 일본어로도 만들어줘, 일본어 버전, 일본어 토글, 한일 병기, 한/일 전환 버튼, 日本語版にして, 日韓切り替え, "이거 일본 팀에 보낼 수 있게", "이 문서 아티팩트로 일본어까지", "16:9로 일본어 덱" — with input as markdown/text, an existing HTML page or deck, .docx, PDF, or a Notion page. Do NOT use when building a document from raw numbers or a memo with no Korean document yet (that is a deck-building job, not this), when the user only wants translated text with no HTML output, or for Japanese → Korean direction.
---

# ko-ja-bilingual

이미 있는 한국어 문서에 일본어를 붙여서 **한/일 토글이 달린 HTML 한 파일**로 만든다. 기본 표시는 일본어, 버튼으로 한국어 전환. 템플릿·디자인 토큰·레이아웃은 이 폴더 안에 다 들어 있어서 다른 스킬이 필요 없다. 흐름은 **입력 정규화 → 번역 → 토글 주입 → 검증**.

레이아웃·컴포넌트는 `references/layouts.md`(덱), `references/report.md`(문서)를 따른다. 거기 없는 마크업은 스타일이 안 입혀진다. 토큰(색·폰트)은 템플릿 `:root`에만 있으니 인라인 hex나 font-family를 쓰지 않는다 — 브랜드를 바꾸려면 `:root`의 `--green`·`--font-display`와 report-base의 `.brandmark` 텍스트만 바꾸면 된다.

## 워크플로

### 1. 입력을 마크다운 한 벌로 정규화

| 입력 | 방법 |
|---|---|
| .md / .txt / 채팅에 붙인 글 | 그대로 |
| 기존 HTML | h1~h3·문단·리스트·표를 추출. 이 스킬(또는 같은 템플릿)로 만든 덱이면 `<section class="slide">` 경계를, 문서면 섹션 경계를 그대로 유지 |
| .docx | `python3 scripts/docx2md.py in.docx > in.md` |
| .pdf | Read 도구(`pages`)로 읽어 제목 계층을 복원 |
| Notion | `notion-fetch`로 페이지 마크다운 획득 |

중간 산출물은 스크래치에 두고 사용자에게 보이지 않는다. 이미지는 `[이미지: …]` 자리를 남긴다.

### 2. 문서인가 덱인가

| 신호 | 형식 | 전달 |
|---|---|---|
| "아티팩트", "문서", "읽을 수 있게", "링크로 공유" | 스크롤 문서 | Artifact 발행 + 로컬 저장 |
| "16:9", "덱", "슬라이드", "발표", "회의" | 16:9 덱 | 로컬 HTML, Finder로 폴더 열기 |
| 입력이 `.slide` 섹션으로 된 덱 HTML | 덱 | |
| 입력이 `.masthead`가 있는 문서 HTML | 문서 | |

둘 다 없으면 회의 여부로 추정하고 AskUserQuestion으로 한 번만 확인한다.

### 3. 번역

`references/translation.md`를 읽고 따른다. 핵심은 세 가지 — 문장이 아니라 주장을 옮기고, 숫자 단위를 일본 관행(百万円·万人·ポイント)으로 바꾸고, 미달 서술은 원인에 귀속시킨다. 검토 단계는 없다. 바로 HTML까지 만들고 사용자가 토글로 대조한다.

### 4. 빌드

모든 텍스트 자리는 이 쌍으로 쓴다. **ja가 먼저다.**

```html
<h1><span class="x-ja">客単価+23%、セット構成が牽引</span><span class="x-ko">객단가 +23%, 세트 구성이 견인</span></h1>
```

- **문서** — `assets/report-base.html` 복사. 토글이 내장되어 있고 기본값이 `ja`다. `DOC_LANG_KEY`를 파일 고유 키(예: `lang:2026q2-review`)로 바꾼다.
- **덱** — `assets/deck-base.html` 복사 → `assets/deck-toggle.html`의 세 블록을 표시된 위치(`</style>` 앞, `<div id="hud">` 앞, 마지막 `</script>` 앞)에 넣는다. `DECK_LANG_KEY`도 파일 고유 키로. `file://`에서는 모든 로컬 파일이 localStorage를 공유하므로 키가 겹치면 다른 덱의 언어 선택이 새어 들어온다.
- `<html lang="ja">` 유지. 토글 JS가 `lang`을 같이 바꿔서 템플릿의 `html[lang="ko"]` 타이포 오버라이드(줄간격·자간·폰트)가 따라온다.
- `<title>`은 span을 못 쓰므로 일본어 하나로.
- 영문 eyebrow·페이지 번호·숫자만 있는 셀은 span 없이 둬도 된다. 검증기는 한글·가나가 있는 텍스트만 본다.
- 이미지는 `scripts/box.css`의 규칙대로 고정 높이 박스에 넣는다(사진이 박스를 못 벗어나게).

### 5. 검증 — 0 findings가 통과

```bash
python3 ~/.claude/skills/ko-ja-bilingual/scripts/check_pairs.py out.html
```

`pair`(ja/ko 개수 불일치), `empty`, `mixed`(ko 안에 가나·ja 안에 한글), `untagged`(span 밖 한글·가나), `default`(기본 언어가 ja가 아님), `key`(플레이스홀더 키) 를 잡는다. `mixed`는 고유명사 때문에 의도된 경우가 있으니 읽고 판단한다.

덱은 추가로 — **일본어 화면부터** 오버플로를 본다(일본어가 1.2~1.4배 길다). 넘치면 문장을 자르지 말고 주장을 줄인다. 그다음 `L` 키로 한국어로 넘겨 다시 본다. 이미지가 있으면 `python3 ~/.claude/skills/ko-ja-bilingual/scripts/check_images.py out.html`.

마지막으로 일본어 h1만 위에서 아래로 읽어 논지가 서는지 확인한다.

### 6. 전달

- 파일명 `<원본이름>_jako.html`, 원본과 같은 폴더.
- 문서: Artifact 발행(`favicon`, 한 줄 `description`) → 링크와 로컬 경로를 함께 알린다.
- 덱: `open "<폴더>"`로 Finder를 열고, PDF는 브라우저 `Cmd+P`(가로, 여백 0)라고 한 줄 안내.

## 자주 틀리는 것

| 증상 | 원인 |
|---|---|
| 한국어로 먼저 열림 | JS `saved` 기본값이 `ko`거나 다른 덱의 localStorage 키를 공유 |
| 토글 누르면 슬라이드가 넘어감 | 덱 조각의 `stopPropagation` 블록을 빠뜨림 |
| 한 언어에서만 글이 보임 | span 쌍이 아니라 한쪽만 씀 → `check_pairs.py`의 `pair`/`untagged` |
| 일본어가 슬라이드 밖으로 나감 | 한국어 기준으로 레이아웃을 잡음. 일본어부터 맞춘다 |
| 일본어 자간·줄간격이 한국어처럼 좁음 | `<html lang>`이 토글과 함께 안 바뀜 → 조각의 `root.setAttribute('lang',l)` 확인 |
| 억 원 그대로 「億ウォン」 | 단위 관행 미적용 → translation.md 대조표 |

## 파일

```
assets/deck-base.html       16:9 덱 템플릿 (토큰·네비게이션·인쇄 CSS 내장)
assets/report-base.html     스크롤 문서 템플릿 (토글 내장, 기본 ja)
assets/deck-toggle.html     덱에 주입하는 토글 CSS·HTML·JS 세 블록
references/layouts.md       덱 레이아웃·컴포넌트 (필수)
references/report.md        문서 구조·컴포넌트 (필수)
references/language.md      ko/ja 타이포·단위·톤 원칙
references/translation.md   한→일 옮기기 규칙과 대조표
scripts/docx2md.py          docx → 마크다운 (pandoc 불필요)
scripts/check_pairs.py      span 쌍·기본 언어·키 검증
scripts/check_images.py     이미지 박스 이탈 검사
scripts/box.css             이미지 박스 CSS
evals/                      트리거 테스트 (python3 evals/trigger-check.py evals/trigger-cases.json)
```
