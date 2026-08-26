# korean-date-parser

한국어 자연어를 **날짜·시간·제목**으로 분해하는 의존성 0 자바스크립트 파서.
음성 인식 결과의 오탈자(한글 숫자·붙여쓰기·조사)까지 잡는 게 핵심.

```js
CalParse.parse("내일 10시 반에 서현역", "2026-07-22")
// → { title:"서현역", date:"2026-07-23", time:"22:30", hasDate:true }
```

- **무의존성** · 브라우저(`window.CalParse`) / Node(`require`) 양쪽 동작
- 테스트 39개 포함: `node --test tests/parse.test.cjs`
- 실제 캘린더 앱(i Day)의 빠른입력·음성입력에서 다듬어짐

## 쓰는 법

1. `parse.js` 를 프로젝트에 복사
2. 브라우저: `<script src="parse.js"></script>` → `CalParse.parse(...)`
   Node: `const CalParse = require("./parse.js")`

## 처리 범위

상대 날짜(오늘/내일/모레·다음 주·다다음 주·(다음 주) X요일·M월 N일·N일·M/N),
시간(HH:MM·N시·N시 반·오전/오후, 무표기 1~7시=오후),
한글 숫자(열시 십오분→10:15), 한글 숫자+단위(삼 번출구→3번 출구),
붙여쓰기, 조사 흡수(에/에서/의/부터/까지…).

Claude Code 스킬로도 제공됩니다 — `SKILL.md` 참고.

MIT License.
