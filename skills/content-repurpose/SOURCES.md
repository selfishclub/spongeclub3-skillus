# 출처

> **규칙과 구조를 배웠고, 문장은 옮기지 않았다.** 원 저작자와 라이선스는 각 원본을 따른다.

스폰지클럽 3기 스킬러스 공유 저장소([selfishclub/spongeclub3-skillus](https://github.com/selfishclub/spongeclub3-skillus))의
스킬 **50개를 전부** 읽고 가져왔다. 조사 2026-09-08, 실전 테스트 반영 2026-09-10.

---

## 이 스킬의 뼈대를 준 것

| 스킬 | 가져온 것 | 반영한 곳 |
|---|---|---|
| `ecc/content-engine` | 글에서 원자 주장 3~7개를 뽑아 날카로움·새로움·근거로 세운다 | `atoms.md` · STEP 1 |
| `gooseworks…/content-repurposing` | 원자 여섯 종 · 날짜를 벌려 계단식으로 발행 | `atoms.md` · STEP 6 |
| `claude-shorts` | 채점 다섯 항목과 가중치 · 60점 컷 · 「홀로서기」 · 저자가 가리킨 문장 · 잘라낸 조각을 다시 조립 · 강한 것 먼저, 나머지는 2~3일 간격 | `scoring.md` · STEP 3·6 |
| `ecc/crosspost` | 가장 강한 채널 한 편을 먼저 확정하고 파생 · 품질 게이트 셋 · 채널의 스테레오타입이 아니라 제약에 맞춘다 | STEP 6·7 |
| `threads-contents2` | 되돌릴 수 없는 것은 쓰기 전에 정한다 · 범용 규칙과 계정 값을 파일로 가른다 | STEP 2 · `account.example.md` |
| `threads-contents` | 발행 후 비교할 변수를 셋으로 고정 · 첫 문장은 나를 모르는 사람 기준 | STEP 8 |
| `eli5` | 청중 보정은 명시하지 않으면 무너진다 · 처음 보는 사람과 아는 사람의 용어 | STEP 2 |
| `크리틱디렉터` | 점수 구간에 행동을 붙인다 · 채널마다 검수자를 바꾼다 · 고칠 곳은 3~5개, 승인한 것만 | STEP 7 |
| `customer-research` · `coupang-ad-analysis` | 표본이 모자라면 결론 내지 않는다 · 설정 바꾼 직후엔 판정하지 않는다 · 지난 권고부터 보고, 틀렸으면 거둔다 | STEP 9 |
| `gooseworks…/newsletter` · `copywriting-coreyhaines/emails` | 제목과 미리보기는 한 세트 · 한 통에 CTA 하나 · 추신 · 발신자와 답장률 · 90일 무반응 정리 · 스팸 신호 | `newsletter.md` |
| `grill-me` · `service-blueprint` · `skillers-share` | 찾을 수 있는 건 묻지 않는다 · 한 라운드에 몰아서, 추천안과 함께 · 마감 세 줄 | 묻는 법 · 산출물 |
| `caveman` | 줄일 때 지워도 되는 것과 못 지우는 것(부정어·숫자·조건) | STEP 4 |
| `spec-guard` · `marp-deck` | O/X 로 판정할 수 있는 기준 · 고치기는 세 번까지 | STEP 7 |

## 채널 규칙을 준 것

| 스킬 | 가져온 것 | 반영한 곳 |
|---|---|---|
| `hooks` (노슈니) | 훅 후보는 서로 다른 유형에서 뽑는다 | STEP 4 |
| `cardnews` (노슈니) | 캐러셀에 정리 장을 둔다 · 장수는 단정하지 않는다 | `carousel.md` |
| `blog-writing` (노슈니) | 네이버 SEO 실무 · 발행 결과를 봤다고 말하지 않는다 | `reach.md` · SKILL |
| `threads-writing` (노슈니) | 링크·CTA 는 기본적으로 안 붙인다 · 불안으로 닫지 않는다 · 첫 150자 | SKILL · `reach.md` |
| `topic-mining` (노슈니) · `last30days` | 주제 발굴은 이 스킬 앞 단계 · 건질 게 없으면 없다고 적는다 | STEP 0·9 |
| `copywriting-coreyhaines/analytics` · `attribution` | UTM 표준과 명명 규칙 · 작은 규모엔 자가보고 경로가 낫다 | `publish-check.md` |
| `landing-page-generator/campaign-analytics` · `marketing-ops` | 48시간 회고 형식 · 정해 둔 순서를 따른다 | `publish-check.md` |
| `spongeclub3-carousel` | 인스타 슬라이드는 캐러셀 스킬에 맡긴다 · 댓글 → DM 정책 | STEP 4-3 · `channels.md` |

## 이 스킬이 직접 확인한 것

공유 저장소 50개 가운데 **카카오톡을 다룬 스킬은 0개, 네이버 블로그는 1개**였다. 아래는 실제 화면에서 확인했다.

- **오픈 채팅방 공지 접힘** — 접힌 화면 두 장을 비교했다. 좁은 화면 23줄 ≈ 460자, 넓은 화면 14줄 ≈ 480자.
  줄 수는 달라도 글자 수가 같다 → **글자 수 기준, 경계 약 500자, 안전선 400자**
- **카카오톡 채널** — 소식은 사진과 링크 중 하나만 · 미리보기 카드는 첫 링크에만 · 채팅은 두 곳에서 꺼야 한다 ·
  웰컴메시지는 무료지만 기존 친구에게는 안 간다 · 사업자 정보 미확인 채널은 「전문의」 같은 자격 표기가 막힌다
- **링크 미리보기** — og:image 없이 한 번 뿌리면 「이미지 없음」이 캐시되고, 카카오는 갱신 도구가 없다
- **네이버 블로그** — 상단메뉴에 외부 링크 불가 → 위젯, 위젯은 PC 에만 보인다
- **실전 테스트** — 발행된 블로그 글 한 편으로 돌려 보고 규칙 열 개를 고쳤다
  (방 안내 공지는 교체하지 않는다 · 꼬리표는 그 값을 읽는 페이지에만 · 알림형 통과선 75 · 인스타 캡션에 출처·고지 줄을 달지 않는다 등)

## 안 가져온 것

| | 왜 |
|---|---|
| 각 스킬의 문장·표현 | 규칙만 배우고 다시 썼다 |
| 개인 말투 파일 | 그 계정의 것이다. 이 스킬은 「있으면 읽으라」고만 한다 |
| `크리틱디렉터` 의 「얼마나 매섭게 볼까요(1~4)」 | 질문이 하나 더 는다 |
| `ads-creative-development` 의 부품 매트릭스 | 광고 A/B 테스트용이다. 한 편을 나누는 일엔 과하다 |
| `auto-skill-scout` 의 스케줄 회고 | 스킬이 스케줄을 건드리는 건 범위 밖이다 |
| `cardnews` 의 HTML 제작 | 캐러셀 스킬이 할 일이다 |

---

## 원본과 라이선스

| 줄여 부른 이름 | 공유 저장소 폴더 | 원본 |
|---|---|---|
| `ecc/…` | `ecc-(everything-claude-code)/skills/…` | [affaan-m/ECC](https://github.com/affaan-m/ECC) · MIT |
| `gooseworks…/…` | `gooseworks-ai-competitor-ad-intelligence/skills/…` | [openclaudia/openclaudia-skills](https://github.com/openclaudia/openclaudia-skills) · MIT |
| `copywriting-coreyhaines/…` | `copywriting-coreyhaines/skills/…` | [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) · MIT |
| `landing-page-generator/…` | `landing-page-generator/marketing/…` | borghei/Claude-Skills · MIT |
| `hooks` · `cardnews` · `blog-writing` · `threads-writing` · `topic-mining` | 같은 이름 폴더 | 노슈니(오수인) · 스폰지클럽 3기 제공 |
| `spongeclub3-carousel` | — | 스폰지클럽 3기 제공 |
| 그 밖 | 같은 이름 폴더 | 각 폴더의 `SOURCE.md` |

## 웹 출처

- 네이버 C-Rank · D.I.A — [로카포스팅](https://locaposting.com/blog/naver-crank-dia-algorithm)
- 스레드 알고리즘 — [ThreadsAuto](https://www.threadsauto.kr/blog/threads-algorithm-2026-signals)
- 인스타 캐러셀 — [linkfarm](https://linkfarm.ai/blog/instagram-carousel-content-guide-2026)
- 인스타 인앱 SEO — [포크레터](https://forcreator.co.kr/blog/instagram-search-seo) · [SNS헬프](https://www.helpsns.com/blog/instagram-search-seo-guide/)
- GEO — [AB180](https://blog.ab180.co/posts/geo-generative-engine-optimization-vs-seo-difference) · [GeoRank](https://georank.co.kr/report/seo-vs-geo-generative-engine-optimization-ai-search)
- AEO — [WRITER](https://writer.com/blog/geo-aeo-optimization/) · [Jasper](https://www.jasper.ai/blog/geo-aeo) · [Profound](https://www.tryprofound.com/blog/aeo-vs-geo)

**플랫폼 규칙은 바뀐다.** 숫자가 안 맞으면 그 자리에서 다시 확인한다.
