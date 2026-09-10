# 직접 만든 사이트에 붙이기

랜딩과 폼을 직접 만들었다면 여기까지 할 수 있다. **반나절이면 끝나고, 한 번 붙이면 계속 돈다.**

예시는 Next.js + Supabase 기준이지만, **판단은 스택과 무관하다.** 왜 그렇게 하는지만 가져가면 어디서든 같다.

## 만들 것 넷

```
① 링크 표          어떤 링크를 어디에 내보냈나 + 클릭 수
② 짧은 링크 경로    /l/<열쇠>  →  UTM 붙여 랜딩으로
③ 유입 저장        폼 제출에 utm_* 와 링크 열쇠를 같이 담는다
④ 관리 화면        링크별 클릭 → 신청 → 전환율
```

## ① 링크 표

```sql
create table if not exists links (
  slug          text primary key,          -- 짧은 주소의 열쇠
  created_at    timestamptz not null default now(),
  label         text not null,             -- 「어디에 내보냈나」 한글 그대로
  target        text not null default '/', -- 사이트 안 경로만
  utm_source    text not null,
  utm_medium    text not null,
  utm_campaign  text,
  utm_content   text,
  note          text,
  clicks        int  not null default 0,
  last_click_at timestamptz
);
```

**`label` 이 utm 값보다 중요하다.** utm 은 기계가 세는 이름이고 label 은 내가 찾는 이름이다.

신청 표에는 다섯 칸을 더한다.

```sql
alter table responses add column if not exists utm_source   text;
alter table responses add column if not exists utm_medium   text;
alter table responses add column if not exists utm_campaign text;
alter table responses add column if not exists utm_content  text;
alter table responses add column if not exists link_slug    text;
```

**`link_slug` 를 빠뜨리지 않는다.** utm 값이 같아도 내보낸 자리가 다르면 다른 링크다. 이 칸이 있어야 「이 링크 클릭 12 → 신청 3」이 이어진다.

> 이미 쓰던 출처 칸(`source` 같은 것)이 있으면 **지우지 말고 둔다.** 그 값으로 들어온 사람이 이미 명단에 있고, 컬럼을 갈아치우면 그 사람들의 출처가 통째로 사라진다. 화면에서 `utm_source ?? source` 로 읽으면 된다.

## ② 짧은 링크 경로 — 오는 쪽이 둘이라 답도 둘

`/l/<slug>` 하나에 두 가지 답이 있다.

```
사람  →  UTM 붙여 랜딩으로 넘긴다. 그리고 센다
기계  →  미리보기 카드 재료(og 태그)를 여기서 바로 준다. 안 센다
```

**기계에게 넘기면 안 되는 이유** — 카카오는 넘김을 따라가지 않는다. 랜딩에 og 를 아무리 잘 붙여둬도 재료가 있는 곳까지 안 가서 카드가 안 뜬다.

**기계를 막아도 안 되는 이유** — 막으면 카드를 못 만들어서 링크가 맨몸으로 나간다. 보내주되 안 세면 된다.

```ts
const bot = isBot(req.headers.get('user-agent'))
// ... 링크를 찾아 목적지 to 를 만든 뒤
if (bot) return ogPage(origin, to)     // 재료만 주고 끝
countClick(slug)                        // 사람만 센다
return Response.redirect(to, 307)
```

**307 로 보낸다.** 영구(301)로 보내면 브라우저가 기억해서, 나중에 목적지를 고쳐도 이미 누른 사람에게는 옛 주소가 계속 나간다.

**없는 열쇠는 404 대신 랜딩으로 보낸다.** 404 를 띄우면 오래된 링크를 누른 사람이 「이 사이트 죽었네」로 읽고 돌아간다.

## ③ 클릭 세기 — 떼어놓는 것과 버리는 것은 다르다

세는 일이 느려도 링크는 빨라야 하니 응답 뒤로 뺀다. **그런데 빼는 방법을 틀리면 통째로 버려진다.**

```ts
// ❌ 이렇게 두면 응답 후 서버가 얼어붙어 아예 안 돈다
void db.rpc('bump_link', { slug })

// ✅ 응답 뒤에 반드시 실행되는 장치를 쓴다
after(async () => { await db.rpc('bump_link', { slug }) })
```

Next.js 는 `after()`, 다른 환경이면 큐·워커·백그라운드 작업이 그 자리다. **「나중에 한다」와 「안 한다」를 프레임워크가 구분해 주는지 확인하고 쓴다.**

세는 것도 한 문장으로 한다. 읽고 +1 해서 다시 쓰면 동시에 두 명이 누를 때 하나가 사라진다.

```sql
update links set clicks = clicks + 1, last_click_at = now() where slug = $1;
```

## ④ 봇 판별

**넉넉하게 거른다.** 사람을 기계로 잘못 보면 클릭 하나를 잃지만, **기계를 사람으로 세면 숫자 전체를 못 믿게 된다.**

```ts
// 정규식은 한 줄이어야 한다. 줄을 나누면 그대로 복사했을 때 문법 오류가 난다.
// 보기 좋게 나누려면 조각을 이어 붙인다.
const BOT = new RegExp([
  'kakao', 'facebookexternalhit', 'twitterbot', 'slackbot', 'linkedinbot',
  'telegrambot', 'whatsapp', 'discordbot', 'embedly', 'applebot',
  'googlebot', 'bingbot', 'yeti', 'daum',
  'bot\\b', 'crawler', 'spider', 'preview', 'scrap',
  'curl', 'wget', 'python-requests', 'node-fetch', 'headless',
].join('|'), 'i')

function isBot(ua) {
  if (!ua || ua.trim().length < 10) return true   // 브라우저는 늘 보낸다
  return BOT.test(ua)
}
```

**UA 가 아예 없는 요청도 사람이 아니다.**

## ⑤ 랜딩 → 폼 사이에서 출처를 놓치지 않기

첫 화면과 폼이 다른 페이지면, 넘어갈 때 값을 들고 가야 한다.

```tsx
// 랜딩: 받은 utm 을 그대로 다음 주소에 실어 보낸다
const href = `/form${utmQuery(readUtm(searchParams), linkSlug)}`
```

폼 쪽에서는 주소창에서 읽어 제출에 싣는다. **저장은 서버에서 한 번 더 다듬는다** — 주소창 값은 누구나 아무거나 넣을 수 있으니 길이를 자르고, 저장은 하되 **그 값을 믿고 무언가를 열어주지는 않는다.**

## ⑥ 미리보기 카드

1:1 발송이 주력이면 여기에 30분을 쓸 값어치가 있다. **받는 사람이 가장 먼저 보는 화면이 랜딩이 아니라 이 카드다.**

- `og:title` · `og:description` · `og:image` — **설명 메타만 있으면 안 된다.** 카톡은 `og:` 를 먼저 읽는다
- 그림 주소를 **절대경로**로 만든다. 상대경로면 카톡이 그 주소를 못 연다
- **그림 주소에 내용이 바뀌면 달라지는 값을 붙인다** (`?v=<해시>`). 카카오는 주소로 그림을 기억해서, 주소가 같으면 그림을 고쳐도 옛것을 계속 쓴다

그림을 코드로 그린다면(`ImageResponse` 등) **한글 글꼴을 직접 넘겨야 한다.** 안 넘기면 전부 네모로 나온다 — **카드가 안 뜨는 것보다 나쁘다.** 깨진 채로 남의 대화창에 남고, 보낸 사람은 자기 화면이 아니라 못 본다.

원본 글꼴은 한글이라 수 MB 다. 카드에 쓰는 글자는 보통 40자 안쪽이니, **그 글자만 잘라내면 수십 KB** 가 된다. 대신 **잘라낸 글꼴에는 잘라낸 글자밖에 없으므로**, 문구를 바꾸면 테스트가 먼저 깨지게 묶어둔다.

## ⑦ 누적 카운터 — 지워도 안 줄어드는 숫자

```sql
create table if not exists tallies (key text primary key, n bigint not null default 0);

create or replace function tally_bump() returns trigger language plpgsql as $$
begin
  if coalesce(new.utm_source, '') = 'test' then return new; end if;   -- 시험은 안 센다
  insert into tallies (key, n) values ('responses_total', 1)
    on conflict (key) do update set n = tallies.n + 1;
  return new;
end $$;

create trigger responses_tally after insert on responses
for each row execute function tally_bump();
```

**코드가 아니라 DB 트리거로 단다.** 코드에 달면 나중에 다른 경로로 저장할 때 세기를 빠뜨리는데, **빠뜨린 것은 「숫자가 안 는다」는 신호를 안 낸다.**

**시험을 빼는 조건을 같이 넣는다.** 안 넣으면 이번 주 내내 눌러본 것이 다 누적에 얹히고, 부푼 숫자는 어디에도 못 쓴다.

## ⑧ 관리 화면에 띄울 것

목록보다 **위에** 둔다. 아래에 있으면 안 본다.

```
지금 명단 6명    누적 11건(지운 것 5건 포함)    클릭 24    그중 신청 3    전환율 13%
```

링크 표에는 한 줄에 **클릭 → 신청 → 전환율**을 같이 놓는다. 셋이 한 줄에 있어야 「클릭 0」과 「클릭은 있는데 신청 0」이 눈으로 갈린다. 그게 SKILL.md 4단계의 표다.

## 내보내기 전 확인 목록

**전부 배포된 서버에서 한다.** 내 컴퓨터에서 되는 건 아직 아무것도 확인한 게 아니다.

- [ ] 짧은 링크를 열면 주소창에 `utm_source` 가 보인다
- [ ] 첫 화면 → 폼으로 넘어간 뒤에도 **주소창에 그대로 남아 있다** ← 여기서 제일 많이 깨진다
- [ ] 끝까지 제출하면 명단 유입 칸에 그 채널이 뜬다
- [ ] 링크 표의 클릭이 1 오르고, 신청도 1 오른다
- [ ] 봇 UA 로 열면 **클릭이 안 오른다**
- [ ] 「나와의 채팅」에 보내면 **미리보기 카드가 뜬다**
- [ ] 확인이 끝나면 시험 데이터를 지운다 — **지우기 전에 내려받아 둔다**

> 🔴 **시험할 때는 그 사이트 탭을 전부 닫고 시작한다.** 링크는 새 탭에서 열렸는데 폼은 옛 탭에서 제출하면, 코드가 다 멀쩡해도 유입이 「직접 방문」으로 뜬다. **시험 환경에서 제일 안 보이는 변수가 시험하는 사람 자신이다.**
