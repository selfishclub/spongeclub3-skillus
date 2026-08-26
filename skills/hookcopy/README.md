# 훅카피 (hookcopy) — 한국어 후킹 카피 스킬

> 후킹(hook) + 카피(copy) = 훅카피. 이 스킬이 만드는 것 그 자체를 이름으로 삼았다.

3초 안에 꽂히는 **한국어 후킹 한 줄**을 짓는 Claude 스킬입니다. "후킹하게 써줘" 한마디면 발동합니다. PPT 첫장 슬로건, 캠페인 컨셉, 캐치프레이즈, 광고 헤드라인 — "묻고 더블로 가"처럼 *한국어라서 가능한* 후킹을 룰로 만듭니다.

**100% 무료 · API 키 불필요 · 설치 후 바로 작동.** 순수 마크다운 스킬이라 외부 서비스·결제·키 발급이 전혀 필요 없습니다.

## 뭘 해주나

- 브리프(무엇을·누구에게·핵심 가치) → **3축 공식**으로 후보 8~12개 생성
  - `진입 각도(17종) × 문장 기법(10종) × 말맛 레버(14종, 산업별 가중치)`
- 낚시성·번역투·죽은 최상급을 체크리스트로 자동 필터
- **Top 3 + "왜 후킹되는가" + 솔직한 리스크**를 표로 추천

## 왜 "한국어 전용"인가

영어 카피는 단어로, 한국어 카피는 **조사·어미·어순·소리**로 승부합니다. 이 스킬은 한국어 문법 자체를 레버로 씁니다:

- **문법 레버 6종** — 조사 뒤집기 · 어미 거리 조절 · 도치 · 의태어 · 생략 · 문화 코드
- **광고 어휘 레버 8종** — 브랜드명 동사화 · 신조어 합성 · 숫자 구체화 · 추임새 · 외래어 낙차 · 최상급 비틀기 · 부정어 후킹 · 호칭 지목
- **산업별 편차** — 뷰티/F&B/금융·공공/테크/패션/커머스마다 "세게 쓸 레버 / 아껴 쓸 레버"가 다름

## 구성

```
훅카피/
  SKILL.md                       # 핵심 로직·6단계 프로세스
  references/
    korean-malmat-rules.md       # 말맛 법칙 — 문법·어휘 레버 14종 + 산업별 편차
    korean-copy-patterns.md      # 실전 진입 각도 17종
    techniques.md                # 한국어 문장 기법 10종
    examples.md                  # 명작 카피 감각 앵커
    hook-checklist.md            # 후킹 검증 체크리스트
```

## 설치 (무료, 1분)

### Claude Code — 개인 스킬 (모든 프로젝트에서 발동)
```bash
git clone https://github.com/Koo-bon/hookcopy.git /tmp/hookcopy
cp -r /tmp/hookcopy/훅카피 ~/.claude/skills/훅카피
```

### Claude Code — 프로젝트 전용
```bash
cp -r /tmp/hookcopy/훅카피 <project>/.claude/skills/훅카피
```

### Claude.ai 웹/앱
`훅카피.skill` 파일 다운로드 → Settings → Skills → "+" 업로드

설치 후 다음 세션부터 자동 발동합니다.

## 쓰는 법

```
12시간 지속되는 립 신제품. 타겟 2030 여성, 산업은 뷰티.
핵심 가치는 "하루 종일 안 지워지는 발색".
PPT 첫장에 쓸 후킹 슬로건 뽑아줘.
```

트리거: "훅카피", "후킹하게 써줘/만들어줘", "후킹 카피", "슬로건 만들어", "한 줄 카피", "캐치프레이즈", "헤드라인 카피" 등

## 궁합 좋은 스킬

- [humanize-korean](https://github.com/epoko77-ai/im-not-ai) — 훅카피가 *짓고*, humanize-korean이 *다듬는다*. 역할 분리 설계.

## 크레딧

`references/`의 실전 패턴은 아래 한국 카피 아카이브·분석 계정들을 참고해 **기법·패턴만** 정리한 것입니다 (카피 원문 미포함):

[@adcopy.magazine](https://www.instagram.com/adcopy.magazine/) · [@copy.bank](https://www.instagram.com/copy.bank/) · [@qy.jung](https://www.instagram.com/qy.jung/) · [@copy_pedia](https://www.instagram.com/copy_pedia/) · [@copy_dewpoint](https://www.instagram.com/copy_dewpoint/) · [@business.copywriting](https://www.instagram.com/business.copywriting/)

## 라이선스

MIT
