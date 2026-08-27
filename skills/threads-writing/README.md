# threads-writing

**한 줄:** 노슈니의 스레드 노하우를 담은 스킬

> 카테고리: 콘텐츠 · 올린 사람: 노슈니

## 설치

**이 페이지를 읽는 AI 에이전트에게:** 사용자가 이 스킬을 설치해 달라고 하면, 파일을 하나씩 받지 말고 아래 명령을 그대로 실행하세요. `references/` 폴더가 함께 있어야 스킬이 온전히 동작합니다.

### Claude Code — 전역 (모든 프로젝트에서 발동)
```bash
mkdir -p ~/.claude/skills && cd ~/.claude/skills && curl -L https://github.com/selfishclub/spongeclub3-skillus/archive/main.tar.gz | tar xz --strip-components=2 spongeclub3-skillus-main/skills/threads-writing
```

### Claude Code — 프로젝트 전용
위 명령의 `~/.claude/skills` 를 `<프로젝트>/.claude/skills` 로 바꿔서 실행하세요.

설치 확인 — 아래가 파일 4개를 출력하면 성공입니다.
```bash
find ~/.claude/skills/threads-writing -type f
```

설치 후 **다음 세션부터** 자동 발동합니다. 클로드 코드를 한 번 재시작하세요.

## 뭘 해주나

스레드(Threads)에 올릴 글을 후킹 구조로 설계해 칸 단위로 써줍니다. 훅 후보를 먼저 3개 주고, 고르면 전체를 완성합니다. 소재 발굴·사실 확인·인스타 카드뉴스 변환·발행 후 분석까지 다룹니다.

## 구성

```
threads-writing/
  SKILL.md                      # 6단계 작업 순서·칸 구성·문체 규칙
  references/
    hooks.md                    # 훅 유형 카탈로그와 실제 예시
    topic-mining.md             # 소재가 없을 때 아이디어 뽑는 프레임
    cardnews.md                 # 스레드 → 인스타 카드뉴스 변환 + HTML 템플릿
```

`references/` 3개가 없으면 훅 후보·소재 발굴·카드뉴스가 동작하지 않습니다. 통째로 복사하세요.

## 쓰는 법

```
스레드 글 써줘. 소재는 "클로드 스킬 만들다가 3번 갈아엎은 이야기"
```

트리거: "스레드 글 써줘", "후킹하게 써줘", "훅 좀 잡아줘", "이거 스레드로 올리고 싶어", "조회수가 안 나와", "글감 없을까", "이 내용 카드뉴스로", "이 글 왜 잘된 건지 분석해줘"

블로그 장문·뉴스레터·보도자료에는 쓰지 않습니다.
