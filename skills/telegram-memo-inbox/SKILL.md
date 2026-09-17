---
name: telegram-memo-inbox
description: "이동 중에 던진 한 줄 메모를 텔레그램 봇이 받아 분류해서 노션 DB·저장소에 자동으로 쌓는 인박스를 만드는 스킬. 봇 만들기(BotFather) → 웹훅 서버 코드 생성 → Vercel 배포 → 환경변수·웹훅 등록 → 실제 저장 확인까지 한 단계씩 같이 하고, 매 단계 됐는지 직접 검증한다. 글감·감사일기·할 일·지출·아이디어처럼 '나중에 꺼내 쓸 재료'를 모으는 용도. 사용자가 '텔레그램으로 메모 보내면 자동 저장', '글감 모으는 봇', '메모 인박스', '카톡처럼 던지면 노션에 쌓이게', '운전하다 떠오른 거 저장', '봇이 알아서 분류해줬으면', '아이디어 쌓는 곳 만들어줘', '노션에 자동으로 넣어줘', '웹훅 붙여줘', '봇이 답장을 안 해', '저장은 되는데 노션에 안 들어가' 같은 말을 하거나, 이미 만든 봇의 저장 흐름을 고치려 하면 반드시 이 스킬을 사용한다. 봇이 Claude 세션을 거쳐 대화하게 만드는 일(클로드코드 텔레그램 연동)에는 쓰지 않는다 — 이 스킬의 봇은 Claude 없이 혼자 돌아간다."
---

# 텔레그램 메모 인박스

**"좋은 생각은 책상 앞에서 안 떠오른다"** 를 푸는 스킬이다.

운전 중, 강의 끝나고 나오는 길, 자기 직전 — 떠오른 한 줄을 어딘가 적어두려다 결국 못 적는다.
적었어도 카톡 나에게 보내기, 메모앱, 노트 여기저기 흩어져서 나중에 못 찾는다.

이 스킬은 **텔레그램 대화창 하나를 인박스로 만든다.** 던지면 끝. 봇이 받아서 분류하고, 노션 대장에 줄을 하나 추가한다.
나중에 그 대장이 통째로 글 재료가 된다.

**핵심 설계 — 이 봇은 Claude를 거치지 않는다.** 웹훅이 직접 받아서 직접 저장한다.
그래야 새벽 3시에 던져도, PC가 꺼져 있어도, 세션이 끊겨 있어도 저장된다. (Claude 세션을 거치는 봇은 세션이 살아 있을 때만 동작한다 — 인박스로는 실격이다.)

## 언제 쓰나

- 콘텐츠·칼럼·뉴스레터 글감을 계속 모아야 하는 사람
- 감사일기·회고처럼 매일 한 줄 쌓아 나중에 묶을 계획이 있는 사람
- 외부 일정이 많아 책상 앞에 있는 시간이 적은 사람 (강사·영업·현장직)
- 이미 노션을 쓰는데 "노션 앱 여는 것" 자체가 귀찮아서 기록이 끊기는 사람

**안 쓰는 경우** — 팀 공용 업무 요청 접수(그건 폼·이슈트래커), 봇과 대화하며 일을 시키는 용도(그건 클로드코드 텔레그램 연동 스킬).

---

## 0단계 — 먼저 정할 것 세 가지

코드부터 짜지 않는다. 이 세 가지를 물어보고 확정한 뒤 시작한다.

**① 뭘 모을 건가 (인박스의 정체)**
하나로 정한다. 욕심내서 "전부 다"로 만들면 분류가 무너지고 안 쓰게 된다.
> 예: 글감 / 감사일기 / 아이디어 / 지출 / 읽을거리 / 고객 문의 메모

**② 어디에 쌓을 건가 (목적지)**
- **노션 DB** — 가장 추천. 나중에 보기·필터·정렬이 되고, 모바일에서도 읽힌다.
- **JSON 저장소** (Vercel Blob 등) — 웹 화면에서 직접 읽어 쓸 계획이 있으면.
- **둘 다** — 저장소가 원본, 노션이 미러. 사용자의 실전 구성이 이것이다.

**③ 분류 기준 (있으면 좋고, 없어도 된다)**
- 접두어 방식: `글감:` `일기:` `할일:` → 접두어로 대장을 나눈다
- 이모지 방식: 첫 글자 이모지를 속성으로 기록 (😊기쁨 🔥열정 🤔생각 …)
- 무분류: **아무 텍스트나 던지면 다 저장.** 진입 마찰이 0이라 가장 오래 간다.

> **권장 — 무분류를 기본으로 하고, 접두어는 "있으면 인식, 없어도 됨"으로 짠다.**
> `text.replace(/^(글감|일기|회고)\s*[:：]?\s*/, "")` 한 줄이면 둘 다 만족한다.
> 사용자가 매번 접두어를 붙여야 하면 그 봇은 두 달 안에 죽는다.

---

## 1단계 — 봇 만들기

텔레그램에서 **@BotFather** 를 찾아 대화를 시작하고, 아래를 순서대로 안내한다.
**각 단계마다 "됐어요?"를 확인하고 넘어간다. 한 번에 다 쏟아내지 않는다.**

1. `/newbot` 입력
2. 봇 이름(표시용, 한글 가능) → 예: `글감 인박스`
3. 봇 아이디(영문, `_bot`으로 끝나야 함) → 예: `mygulgam_inbox_bot`
4. **토큰이 나온다.** `1234567890:AA...` 형태.

> ⚠️ **토큰은 비밀번호다.** 채팅창·저장소·발표자료에 그대로 두지 않는다.
> 환경변수로만 넣고, 대화 중 받았으면 설정 끝난 뒤 "위 메시지에서 토큰 지워주세요"라고 안내한다.
> 노출됐으면 BotFather `/revoke` 로 즉시 재발급.

5. 만든 봇 대화방에 들어가 **아무 말이나 한 번 보낸다** (이걸 해야 chat_id가 생긴다)
6. chat_id 확인:
```bash
curl -s "https://api.telegram.org/bot<토큰>/getUpdates"
```
응답의 `message.chat.id` 숫자가 내 chat_id다. 이것도 환경변수로 넣는다.

> 💡 **웹훅을 등록한 뒤에는 `getUpdates`가 동작하지 않는다.** 순서를 지킨다 — chat_id 먼저, 웹훅 나중.

---

## 2단계 — 웹훅 서버 만들기

Vercel 서버리스 함수 2개 파일이면 끝난다. (Next.js·정적 사이트 어디에 붙여도 된다.)

### `api/telegram.js` — 받는 곳

```js
// 텔레그램 → 인박스 직통. Claude 세션 없이 웹훅이 직접 저장한다.
import { saveEntry } from "../lib/inbox-core.js";

const MOODS = ["😊", "🥰", "😌", "✨", "😆", "🔥", "🤔", "🥲", "😤", "😴"];

async function send(chatId, text, replyTo) {
  const tok = process.env.BOT_TOKEN;
  if (!tok) return;
  try {
    await fetch(`https://api.telegram.org/bot${tok}/sendMessage`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ chat_id: chatId, text, ...(replyTo ? { reply_to_message_id: replyTo } : {}) }),
    });
  } catch {}
}

export default async function handler(req, res) {
  // ★ 항상 200으로 끝낸다 — 에러를 돌려주면 텔레그램이 같은 메시지를 계속 재전송한다.
  if (req.method !== "POST") return res.status(200).send("inbox webhook");

  // ★ 관문 1: 웹훅 시크릿 헤더
  const secret = req.headers["x-telegram-bot-api-secret-token"] || "";
  if (secret !== process.env.TG_WEBHOOK_SECRET) return res.status(401).json({ error: "unauthorized" });

  const msg = req.body && req.body.message;
  const chatId = msg && msg.chat && String(msg.chat.id);
  // ★ 관문 2: 내 chat_id만 처리 (봇 아이디는 공개라 아무나 말을 걸 수 있다)
  if (!msg || chatId !== process.env.MY_CHAT_ID) return res.status(200).json({ ok: true });

  let text = (msg.text || "").trim();
  if (!text) {
    await send(chatId, "글(텍스트)만 저장할 수 있어요 ✍️", msg.message_id);
    return res.status(200).json({ ok: true });
  }
  if (text === "/start") {
    await send(chatId,
      "📥 인박스예요!\n\n아무 말이나 보내면 그대로 저장됩니다.\n" +
      "첫 글자에 이모지를 붙이면 분류로 함께 기록돼요.\n\n" +
      "연결 확인은 \"핑\"이라고 보내보세요!");
    return res.status(200).json({ ok: true });
  }
  // ★ 연결 확인용 핑-퐁 — 있으면 나중에 "이거 살아있나?" 를 5초 만에 확인한다
  if (text === "핑" || text.toLowerCase() === "ping") {
    await send(chatId, "퐁! 인박스 직통 연결 정상이에요 📥", msg.message_id);
    return res.status(200).json({ ok: true });
  }

  // 접두어는 있어도 없어도 되게
  text = text.replace(/^(글감|메모|일기|회고)\s*[:：]?\s*/, "");
  let mood = "";
  for (const m of MOODS) {
    if (text.startsWith(m)) { mood = m; text = text.slice(m.length).trim(); break; }
  }
  if (!text) {
    await send(chatId, "내용이 비어 있어요 ✍️ 한 줄이라도 적어주세요!", msg.message_id);
    return res.status(200).json({ ok: true });
  }
  if (text.length > 5000) {
    await send(chatId, "5000자 이하로 나눠서 보내주세요 🙏", msg.message_id);
    return res.status(200).json({ ok: true });
  }

  try {
    const r = await saveEntry(text, mood, "telegram");
    // ★ 저장 번호를 돌려준다 — "쌓이고 있다"는 감각이 이 봇을 계속 쓰게 만든다
    await send(chatId, `📥 ${r.count}번째 기록 저장! ${mood || "✨"}${r.notion ? "\n노션에도 적어뒀어요 ✓" : ""}`, msg.message_id);
  } catch {
    await send(chatId, "⚠️ 저장에 실패했어요. 잠시 후 다시 보내주시면 꼭 저장할게요.", msg.message_id);
  }
  return res.status(200).json({ ok: true });
}
```

### `lib/inbox-core.js` — 쌓는 곳

```js
// 원본(저장소) + 미러(노션). 웹 화면과 봇 웹훅이 이 파일을 공유한다.
import { list, put } from "@vercel/blob";

export const INBOX_PATH = "inbox/entries.json";

export async function loadEntries() {
  const { blobs } = await list({ prefix: INBOX_PATH, limit: 1 });
  if (!blobs.length) return [];
  const res = await fetch(blobs[0].url + "?t=" + Date.now(), { cache: "no-store" });
  if (!res.ok) return [];
  try {
    const data = await res.json();
    return Array.isArray(data) ? data : [];
  } catch { return []; }
}

export async function mirrorToNotion(entry) {
  const token = process.env.NOTION_TOKEN;
  const db = process.env.NOTION_DB;
  if (!token || !db) return false;
  const preview = entry.text.slice(0, 24) + (entry.text.length > 24 ? "…" : "");
  // ★ select 값은 한글 라벨로. 영문("web"/"telegram")을 그대로 두면
  //   브라우저 번역기가 web→편물, telegram→전보 로 오역해서 보여준다.
  const srcLabel = entry.source === "telegram" ? "✈️ 텔레그램" : "🖥️ 웹";
  const props = {
    "제목": { title: [{ text: { content: preview } }] },
    "날짜": { date: { start: entry.date } },
    "출처": { select: { name: srcLabel } },
  };
  if (entry.mood) props["분류"] = { select: { name: entry.mood } };
  const res = await fetch("https://api.notion.com/v1/pages", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Notion-Version": "2022-06-28",
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      parent: { database_id: db },
      properties: props,
      children: [{
        object: "block", type: "paragraph",
        paragraph: { rich_text: [{ type: "text", text: { content: entry.text } }] },
      }],
    }),
  });
  return res.ok;
}

export async function saveEntry(text, mood = "", source = "web") {
  const entries = await loadEntries();
  const kst = new Date(Date.now() + 9 * 3600 * 1000); // ★ 서버는 UTC다. 한국 날짜로 보정.
  const entry = {
    id: Date.now().toString(36) + Math.random().toString(36).slice(2, 6),
    date: kst.toISOString().slice(0, 10),
    time: kst.toISOString().slice(11, 16),
    source, mood, text,
  };
  entries.push(entry);
  await put(INBOX_PATH, JSON.stringify(entries, null, 1), {
    access: "public",
    contentType: "application/json",
    addRandomSuffix: false,   // ★ 없으면 저장할 때마다 파일이 새로 생겨 누적이 깨진다
    allowOverwrite: true,
    cacheControlMaxAge: 0,    // ★ 없으면 방금 저장한 게 안 보인다
  });
  // ★ 미러 실패가 원본 저장을 막지 않는다. 노션이 죽어도 글은 남아야 한다.
  let notion = false;
  try { notion = await mirrorToNotion(entry); } catch {}
  return { count: entries.length, entry, notion };
}
```

### 노션 DB를 목적지로 쓸 때 (권장)

1. 노션에서 **새 페이지 → 데이터베이스(표)** 생성. 속성을 코드와 맞춘다:
   `제목`(제목) · `날짜`(날짜) · `출처`(선택) · `분류`(선택)
2. notion.so/my-integrations 에서 **새 integration 생성 → 토큰 복사**
3. **만든 DB 페이지에서 `⋯` → 연결 → 방금 만든 integration 추가** ← 이걸 빼먹으면 계속 404가 난다
4. DB URL에서 database_id 추출: `notion.so/<워크스페이스>/<32자리>?v=...` 의 32자리

---

## 3단계 — 배포와 연결

```bash
npx vercel --prod --yes
```

환경변수 4개를 Vercel 프로젝트 설정에 넣는다 (넣은 뒤 **재배포해야 적용된다**):

| 이름 | 값 |
|---|---|
| `BOT_TOKEN` | BotFather 토큰 |
| `MY_CHAT_ID` | 내 chat_id |
| `TG_WEBHOOK_SECRET` | 아무 긴 문자열 (직접 정함) |
| `NOTION_TOKEN` / `NOTION_DB` | 노션 쓸 때만 |

웹훅 등록 — **이 한 줄이 봇과 서버를 연결한다:**

```bash
curl -s "https://api.telegram.org/bot<토큰>/setWebhook?url=https://<내프로젝트>.vercel.app/api/telegram&secret_token=<TG_WEBHOOK_SECRET>"
```

`{"ok":true,"result":true}` 가 나와야 한다.

---

## 4단계 — 검증 (여기를 건너뛰지 않는다)

**말로 "됐습니다" 하지 않는다. 아래를 실제로 확인하고 결과를 보여준다.**

1. 텔레그램에서 봇에게 **`핑`** → `퐁!` 이 오면 웹훅 연결 정상
2. 아무 한 줄 보내기 → `📥 1번째 기록 저장!` 회신 확인
3. 노션 DB 열어서 줄이 실제로 생겼는지 확인 (회신에 `노션에도 적어뒀어요 ✓` 가 붙었는지)
4. 안 되면:
```bash
curl -s "https://api.telegram.org/bot<토큰>/getWebhookInfo"
```
`last_error_message` 를 읽는다. 답이 거기 있다.

| 증상 | 원인 |
|---|---|
| 아무 반응 없음 | 웹훅 미등록 / URL 오타 / 배포 안 됨 |
| 같은 메시지 무한 반복 | 200이 아닌 응답을 돌려주고 있음 |
| `unauthorized` | `secret_token` 과 env 값 불일치 |
| 저장은 되는데 노션만 빔 | DB에 integration 연결을 안 함(3-3단계) / 속성 이름 불일치 |
| 날짜가 하루 어긋남 | KST 보정 누락 |

---

## 5단계 — 운영 (인박스는 비워야 인박스다)

쌓기만 하면 6개월 뒤 "뭔가 많이 쌓였는데 못 쓰겠다"가 된다. **회수 주기를 같이 정한다.**

- **주간 회수** — "이번 주 들어온 거 보여줘" → 목록을 훑고 쓸 것만 다음 단계로 넘긴다
- **묶어 쓰기** — "지난 달 것 모아서 날짜순 정리본 만들어줘" → 칼럼·에세이·회고 초안의 재료
- **분류 추가** — 접두어를 새로 인식시키고 싶으면 `text.replace(...)` 한 줄만 고치고 재배포

> **읽기 API도 같이 만들어 두면 좋다** — `GET /api/inbox?key=...` 로 전체를 받아
> Claude가 바로 정리·요약·초안 작성에 쓸 수 있다. 인박스의 진짜 값어치는 **꺼내 쓸 때** 나온다.

---

## 반드시 지킬 것 (실전에서 데인 것들)

1. **웹훅은 항상 200을 반환한다.** 에러를 돌려주면 텔레그램이 같은 메시지를 계속 재전송한다.
2. **관문 두 개를 다 건다.** `secret_token` 헤더 + `chat_id` 화이트리스트. 봇 아이디는 공개라 누구나 말을 걸 수 있다.
3. **웹훅을 쓰는 봇에 `getUpdates`를 호출하지 않는다.** 둘은 동시에 못 쓴다.
4. **미러 실패가 원본 저장을 막지 않게 한다.** 노션이 죽어도 글은 남아야 한다.
5. **노션 select 라벨은 한글로.** 영문이면 브라우저 번역기가 오역해서 보여준다.
6. **서버 시간은 UTC다.** KST 보정 없이 날짜를 찍으면 밤에 쓴 글이 전날로 들어간다.
7. **토큰·chat_id는 절대 코드나 저장소에 넣지 않는다.** 전부 환경변수. 노출됐으면 `/revoke`.
8. **Windows에서 한글을 curl로 보내지 않는다.** `curl -d '한글'` 은 깨진다.
   UTF-8 파일로 만들어 `--data-binary @file` 하거나 python(`json.dumps(..., ensure_ascii=False).encode('utf-8')`)으로 보낸다.
9. **저장소 목록 조회(`list()`)를 남발하지 않는다.** Vercel Blob의 "고급 작업"은 무료 플랜 월 2,000회이고,
   넘기면 **계정의 저장소 전체가 차단된다.** 존재 확인만 필요하면 `head()`를 쓴다.
10. **회신 문구에 번호를 넣는다.** `3번째 기록 저장!` — 쌓이는 감각이 이 봇의 수명을 결정한다.

---

## 이 스킬을 쓰는 순서 요약

0. 뭘·어디에·어떻게 분류할지 세 가지 확정 (코드보다 먼저)
1. BotFather로 봇 생성 → 토큰·chat_id 확보 (웹훅 등록 **전에** chat_id)
2. `api/telegram.js` + `lib/inbox-core.js` 생성, 목적지에 맞게 수정
3. Vercel 배포 → 환경변수 4개 → 재배포 → `setWebhook`
4. **핑-퐁 → 실제 저장 → 노션 확인** 3종 검증 통과할 때까지 끝내지 않는다
5. 회수 주기와 읽기 방법을 정해준 뒤 마무리
