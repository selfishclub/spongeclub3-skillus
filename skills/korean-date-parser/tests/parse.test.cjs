const test = require("node:test");
const assert = require("node:assert");
const P = require("../parse.js");
const T = "2026-07-11"; // 기준일(토)

const eq = (input, expected) => assert.deepStrictEqual(P.parse(input, T), expected);

test("N일 + 무표기 오후시", () => eq("17일 3시 치과", {title:"치과", date:"2026-07-17", time:"15:00", hasDate:true}));
test("내일 + HH:MM", () => eq("내일 13:30 스폰지", {title:"스폰지", date:"2026-07-12", time:"13:30", hasDate:true}));
test("M/N + 시간없음", () => eq("7/20 병원", {title:"병원", date:"2026-07-20", time:null, hasDate:true}));
test("모레 + 오전", () => eq("모레 오전 9시 미사", {title:"미사", date:"2026-07-13", time:"09:00", hasDate:true}));
test("지난 날짜는 다음달", () => eq("3일 저녁 6시 가족식사", {title:"가족식사", date:"2026-08-03", time:"18:00", hasDate:true}));
test("요일", () => eq("금요일 10시 회의", {title:"회의", date:"2026-07-17", time:"10:00", hasDate:true}));
test("다음주 요일", () => eq("다음주 화요일 점심", {title:"점심", date:"2026-07-21", time:null, hasDate:true}));
test("M월 N일 + N시반", () => eq("8월 15일 2시반 성당", {title:"성당", date:"2026-08-15", time:"14:30", hasDate:true}));
test("날짜 없으면 오늘·시간 null", () => eq("치과 예약", {title:"치과 예약", date:"2026-07-11", time:null, hasDate:false}));
test("시각 뒤 조사 '에'", () => eq("내일 10시에 서현역", {title:"서현역", date:"2026-07-12", time:"10:00", hasDate:true}));
test("N시 반 + 조사", () => eq("내일 10시 반에 회의", {title:"회의", date:"2026-07-12", time:"10:30", hasDate:true}));
test("N시 M분 + 조사", () => eq("모레 3시 15분에 미팅", {title:"미팅", date:"2026-07-13", time:"15:15", hasDate:true}));
test("N시 45분", () => eq("금요일 10시 45분 회의", {title:"회의", date:"2026-07-17", time:"10:45", hasDate:true}));
test("HH:MM + 조사", () => eq("내일 13:30에 스폰지", {title:"스폰지", date:"2026-07-12", time:"13:30", hasDate:true}));
// 음성 인식은 띄어쓰기를 생략하기도 함
test("붙여쓰기: 내일+시각+조사", () => eq("내일10시에 서현역", {title:"서현역", date:"2026-07-12", time:"10:00", hasDate:true}));
test("붙여쓰기: 모레+시각반", () => eq("모레3시반 병원", {title:"병원", date:"2026-07-13", time:"15:30", hasDate:true}));
test("붙여쓰기: M월N일", () => eq("7월20일 여행", {title:"여행", date:"2026-07-20", time:null, hasDate:true}));
test("붙여쓰기: 요일", () => eq("금요일10시 회의", {title:"회의", date:"2026-07-17", time:"10:00", hasDate:true}));
// 음성 인식이 분·시를 한글 숫자로 적는 경우
test("한글 분: 십오분", () => eq("내일 10시 십오분에 서현역", {title:"서현역", date:"2026-07-12", time:"10:15", hasDate:true}));
test("한글 분: 삼십분", () => eq("모레 3시 삼십분 회의", {title:"회의", date:"2026-07-13", time:"15:30", hasDate:true}));
test("한글 분: 사십오분", () => eq("금요일 10시 사십오분 미사", {title:"미사", date:"2026-07-17", time:"10:45", hasDate:true}));
test("한글 시: 두시 반", () => eq("내일 두시 반 병원", {title:"병원", date:"2026-07-12", time:"14:30", hasDate:true}));
test("한글 시: 열시", () => eq("내일 열시에 회의", {title:"회의", date:"2026-07-12", time:"10:00", hasDate:true}));
// 조사 확장: 음성 인식이 에→의로 적기도 하고, 날짜 뒤에도 조사가 붙음
test("분 뒤 '의'(음성 오기)", () => eq("내일 10시 15분의 이매역", {title:"이매역", date:"2026-07-12", time:"10:15", hasDate:true}));
test("날짜 뒤 조사: N일에", () => eq("20일에 정기검진", {title:"정기검진", date:"2026-07-20", time:null, hasDate:true}));
test("시각 뒤 부터", () => eq("내일 3시부터 회의", {title:"회의", date:"2026-07-12", time:"15:00", hasDate:true}));
test("요일 뒤 조사", () => eq("금요일에 소풍", {title:"소풍", date:"2026-07-17", time:null, hasDate:true}));
test("시각 뒤 쯤", () => eq("내일 10시쯤 카페", {title:"카페", date:"2026-07-12", time:"10:00", hasDate:true}));
test("M월N일 뒤 조사", () => eq("8월 15일에 성당", {title:"성당", date:"2026-08-15", time:null, hasDate:true}));
// 음성 인식이 "15 분"처럼 숫자와 분 사이를 띄는 경우 (실제 스크린샷 사례)
test("분 앞 공백", () => eq("내일 11시 15 분에 서현역", {title:"서현역", date:"2026-07-12", time:"11:15", hasDate:true}));
test("분 앞 공백 + 무조사", () => eq("모레 3시 30 분 회의", {title:"회의", date:"2026-07-13", time:"15:30", hasDate:true}));

/* 한글 숫자+단위 → 아라비아 숫자 (음성 인식 결과 정리) */
const { test: tn } = require("node:test");
const an = require("node:assert");
const CP = require("../parse.js");
tn("음성: '삼 번출구' → '3번 출구'", () => {
  an.strictEqual(CP.parse("내일 열시 반에 강남역 삼 번출구", "2026-07-20").title, "강남역 3번 출구");
});
tn("음성: '칠 번출구' → '7번 출구'", () => {
  an.strictEqual(CP.parse("칠 번출구 미팅", "2026-07-20").title, "7번 출구 미팅");
});
tn("음성: '십오 층' → '15층', '이 호선' → '2호선'", () => {
  an.strictEqual(CP.parse("십오 층 회의실", "2026-07-20").title, "15층 회의실");
  an.strictEqual(CP.parse("이 호선 타고 이동", "2026-07-20").title, "2호선 타고 이동");
});
tn("음성: 숫자 없는 제목은 그대로", () => {
  an.strictEqual(CP.parse("번개 모임", "2026-07-20").title, "번개 모임");
  an.strictEqual(CP.parse("동네 산책", "2026-07-20").title, "동네 산책");
});

/* "다음 주" 해석 */
const { test: tw } = require("node:test");
const aw = require("node:assert");
const CPW = require("../parse.js");
tw("'다음 주' 단독 = +7일", () => { // 2026-07-20 = 월요일
  const r = CPW.parse("다음 주 회의", "2026-07-20");
  aw.strictEqual(r.date, "2026-07-27"); aw.strictEqual(r.title, "회의"); aw.ok(r.hasDate);
});
tw("'다음주' 붙여쓰기 단독도 +7일", () => {
  aw.strictEqual(CPW.parse("다음주 병원", "2026-07-20").date, "2026-07-27");
});
tw("'다음 주 금요일' = 다음 주의 금요일", () => {
  const r = CPW.parse("다음 주 금요일 3시 발표", "2026-07-20");
  aw.strictEqual(r.date, "2026-07-31"); aw.strictEqual(r.time, "15:00"); aw.strictEqual(r.title, "발표");
});
tw("'다다음 주' = +14일", () => {
  aw.strictEqual(CPW.parse("다다음 주 검진", "2026-07-20").date, "2026-08-03");
});
