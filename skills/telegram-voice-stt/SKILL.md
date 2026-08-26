---
name: telegram-voice-stt
description: 텔레그램에 보낸 음성 녹음을, 내 맥(또는 맥미니) 안에서 whisper.cpp로 받아써서 "타이핑한 메시지처럼" 처리하게 만드는 셋업 스킬. 완전 오프라인·무료·프라이버시. 사용자가 "텔레그램 음성", "음성 받아쓰기", "말로 메모", "음성으로 명령", "voice", "STT", "whisper 설치", "음성 메모 자동", "녹음해서 보내면", "받아쓰기 만들자", "음성 인식 붙이자"처럼 텔레그램/봇에 음성을 붙이는 걸 언급하면 이 스킬을 사용한다. 이미 깔린 걸 고치거나(정확도·모델 교체·안 됨) 새로 세팅할 때 모두 참고한다.
---

# 텔레그램 음성 → 로컬 받아쓰기 (whisper.cpp)

텔레그램 봇에게 **음성을 녹음해 보내면**, 서버(맥/맥미니)가 **자기 안에서** 텍스트로 받아쓴 뒤, 마치 사용자가 **손으로 타이핑한 것처럼** 처리하는 셋업. 그래서 음성 하나로 메모 저장·일정 등록·브리핑·아무 지시가 다 된다.

> 공유용 배포본입니다. 경로/봇/헬퍼는 **본인 환경에 맞게** 바꿔 쓰세요. 아래는 실제로 돌아가는 참조 구현(한정재 맥미니)입니다.

## 왜 이 방식인가 (설계 철학)

1. **받아쓰기는 로컬에서 한다 — 클라우드로 음성을 보내지 않는다.** whisper.cpp가 맥 CPU로 돌아서 유료 API가 필요 없고(무료), 음성이 외부로 안 나가서 프라이버시가 지켜진다.
2. **전사 결과는 "그냥 사용자의 메시지"다.** 받아쓴 텍스트를 별도 특별 취급하지 않고, 텍스트 메시지와 똑같은 처리 파이프라인에 태운다. 그래서 `#메모`, 일정 변경, 브리핑 등 **모든 기존 기능이 음성으로도 자동으로 된다** — 음성용 로직을 따로 만들 필요가 없다.

이 두 축이 핵심이다. 음성을 특별 케이스로 만들기 시작하면 유지보수가 무너진다.

## 전체 흐름

```
폰(텔레그램) ──음성 녹음──▶ 봇
      │
      ▼  (공식 telegram 플러그인이 attachment_kind="voice"로 전달 — 파일만, 전사 안 함)
받는 창(Claude Code, 맥미니)
      │  1) download_attachment → .oga/.ogg/.opus 로컬 저장
      │  2) transcribe.sh <경로>  →  ffmpeg(16kHz mono wav) → whisper-cli → 한국어 텍스트
      │  3) 그 텍스트를 "일반 메시지"로 간주해 기존 규칙(A/B/C…)대로 처리
      ▼
답장: 🎙 "받아쓴 내용" + 처리 결과
```

**중요:** 텔레그램 플러그인 자체에는 전사 기능이 없다. 플러그인은 음성 **파일만** 세션에 넘긴다. 실제 받아쓰기는 **CLAUDE.md의 지시 + transcribe.sh**가 담당한다. (그래서 이 스킬이 필요하다.)

## 셋업 (처음 까는 경우)

### 1) whisper.cpp + ffmpeg 설치
```bash
brew install whisper-cpp ffmpeg
# 설치 확인
which whisper-cli ffmpeg   # /opt/homebrew/bin/… 나오면 OK
```

### 2) 언어 모델 내려받기
whisper 모델은 크기별로 정확도/속도가 다르다. 한국어는 **small 이상**을 권장.

| 모델 | 용량 | 특징 |
|---|---|---|
| `ggml-base.bin` | ~150MB | 빠름·정확도 낮음 |
| `ggml-small.bin` | ~465MB | **균형(기본 추천)** |
| `ggml-medium.bin` | ~1.5GB | 정확도↑·느림 |
| `ggml-large-v3.bin` | ~3GB | 최고 정확도·가장 느림 |

```bash
mkdir -p ~/claude-telegram/models
cd ~/claude-telegram/models
curl -L -o ggml-small.bin \
  https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.bin
```
(전문용어·사람 이름을 더 잘 잡고 싶으면 `ggml-medium.bin`으로. URL의 small을 medium으로 바꾸면 됨.)

### 3) 받아쓰기 스크립트 `~/claude-telegram/transcribe.sh`
```bash
#!/bin/bash
# 텔레그램 음성 메시지 → 텍스트 (whisper.cpp 로컬, 오프라인)
# 사용: transcribe.sh <audio_path> [lang]   (lang 기본 ko)
set -euo pipefail
AUDIO="${1:?audio path required}"
LANG="${2:-ko}"
HERE="$(cd "$(dirname "$0")" && pwd)"
MODEL="${WHISPER_MODEL:-$HERE/models/ggml-small.bin}"
WHISPER="$(command -v whisper-cli || echo /opt/homebrew/bin/whisper-cli)"
FFMPEG="$(command -v ffmpeg || echo /opt/homebrew/bin/ffmpeg)"
[ -f "$AUDIO" ] || { echo "[err] no audio: $AUDIO" >&2; exit 1; }
[ -f "$MODEL" ] || { echo "[err] no model: $MODEL" >&2; exit 1; }
TMPWAV="$(mktemp -t stt_XXXX).wav"; trap 'rm -f "$TMPWAV"' EXIT
# 어떤 포맷(ogg/opus/oga/m4a…)이든 16kHz mono wav 로 변환
"$FFMPEG" -nostdin -hide_banner -loglevel error -y -i "$AUDIO" -ar 16000 -ac 1 -c:a pcm_s16le "$TMPWAV"
# 받아쓰기(타임스탬프 없이 본문만: -nt 타임스탬프끔, -np 진행바끔)
"$WHISPER" -m "$MODEL" -f "$TMPWAV" -l "$LANG" -nt -np 2>/dev/null \
  | sed 's/^[[:space:]]*//' | sed '/^$/d'
```
```bash
chmod +x ~/claude-telegram/transcribe.sh
# 단독 테스트: 아무 음성파일로
bash ~/claude-telegram/transcribe.sh ~/some_voice.m4a
```

### 4) 받는 창 규칙 `~/claude-telegram/CLAUDE.md` 에 추가
받는 창(텔레그램 채널로 도는 Claude Code) 작업폴더의 CLAUDE.md에 아래 규칙을 넣는다. 이게 있어야 음성이 자동 전사된다.

```markdown
## 음성 메시지 처리 (자동 받아쓰기)
메시지가 음성(`attachment_kind="voice"`)이면 로컬 whisper.cpp로 받아쓴 뒤,
그 텍스트를 **사용자가 보낸 일반 메시지처럼** 처리한다.
1. `download_attachment`로 음성 파일(.oga/.ogg/.opus)을 내려받아 경로를 얻는다.
2. 받아쓰기: `bash /Users/<계정>/claude-telegram/transcribe.sh "<음성경로>"` → stdout 한국어 텍스트.
   - 다른 언어면 두 번째 인자로: `transcribe.sh "<경로>" en`.
3. 나온 텍스트를 그대로 사용자 메시지로 간주해 처리한다(#메모 저장·일정·브리핑·일반 작업 규칙 그대로).
4. 받아쓰기 결과가 비었거나 깨졌으면 사용자에게 텍스트로 다시 보내달라고 요청한다.
5. 답장 첫 줄에 받아쓴 내용을 짧게 확인차 붙인다 — 예: `🎙 "…받아쓴 내용…"` 그다음 처리 결과.
```
> CLAUDE.md를 바꾸면 받는 창 세션을 재시작해야 반영된다: `screen -S claudetg -X quit` (래퍼가 새로 띄움). `launchctl kickstart`만으론 기존 screen 세션이 살아 안 읽힌다.

## 관리 · 문제해결

| 증상 | 원인/해결 |
|---|---|
| 받아쓰기가 안 됨(반응 없음) | CLAUDE.md 음성 규칙 반영 안 됨 → 세션 재시작(`screen -S claudetg -X quit`) |
| `[err] no model` | 모델 경로/다운로드 확인. `ls ~/claude-telegram/models/` |
| `whisper-cli: command not found` | `brew install whisper-cpp`. 경로 `/opt/homebrew/bin/whisper-cli` |
| 변환 실패(ffmpeg 에러) | `brew install ffmpeg`. 텔레그램 음성은 opus(.oga)라 ffmpeg 디코딩 필수 |
| 받아쓰기 부정확(이름·전문용어) | 모델을 `small → medium`(또는 large)로 교체. transcribe.sh의 MODEL만 바꾸면 됨 |
| 특정 언어가 자꾸 틀림 | `transcribe.sh <경로> <lang>` 2번째 인자로 언어 강제 |
| 너무 느림 | 모델을 작게(small→base) 또는 맥 사양 확인. large는 CPU에서 수십 초 걸릴 수 있음 |

## 응용

- **음성으로 일정 등록**: "내일 3시 김철수님 스케일링" 같은 음성 → 전사 → 일정 파싱 파이프라인으로 자동 등록(날짜·시간 파서와 연결).
- **음성 메모**: "#메모 오늘 원장님이 …" → 전사 → 메모 앱 저장 헬퍼로.
- 핵심은 **전사 후 텍스트를 기존 기능에 그대로 흘려보내는 것** — 음성 전용 기능을 새로 만들지 말 것.

## 본인 환경 맞춤 체크리스트
- [ ] 경로의 `/Users/<계정>/claude-telegram/` 을 실제 계정으로
- [ ] 받는 창(텔레그램 Claude Code 채널)이 이미 돌고 있는가(이 스킬은 그 위에 얹는다)
- [ ] CLAUDE.md에 음성 규칙 추가 + 세션 재시작
- [ ] 모델 크기 선택(기본 small, 정확도 필요하면 medium)
