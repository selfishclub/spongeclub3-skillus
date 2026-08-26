# YouTube Digest

YouTube 영상을 분석하여 요약, 인사이트, 한글 번역을 생성하고 퀴즈로 학습 이해도를 테스트하는 플러그인.

## Features

- **Transcript 추출**: yt-dlp로 자막 추출 (한/영 수동/자동)
- **고유명사 교정**: 웹 검색으로 자동 자막 오인식 보정
- **문서 생성**: 요약 + 인사이트 + 전체 번역
- **학습 퀴즈**: 3단계 × 3문제 = 9문제 이해도 테스트
- **Deep Research**: 웹 심층 조사 옵션

## Prerequisites

- `yt-dlp` 설치 필요

```bash
brew install yt-dlp
```

## Usage

```
유튜브 정리해줘 https://www.youtube.com/watch?v=xxxxx
```

또는:
- "영상 요약해줘"
- "transcript 번역해줘"
- "YouTube digest"

## Output

`research/readings/youtube/{YYYY-MM-DD}-{title}.md` 형식으로 저장:
- 요약 및 주요 포인트
- 인사이트 및 적용점
- 전체 스크립트 (한글 번역)
- 퀴즈 결과 및 오답 노트
