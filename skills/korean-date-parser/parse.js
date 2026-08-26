/* 빠른입력 파서 — "17일 3시 치과" → {title,date,time}. 브라우저: window.CalParse / node: module.exports */
(function (root, factory) {
  if (typeof module !== "undefined" && module.exports) module.exports = factory();
  else root.CalParse = factory();
})(this, function () {
  const DOW = { "일": 0, "월": 1, "화": 2, "수": 3, "목": 4, "금": 5, "토": 6 };
  const pad = n => String(n).padStart(2, "0");
  const ymd = d => d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate());

  const ONES = { "일": 1, "이": 2, "삼": 3, "사": 4, "오": 5, "육": 6, "칠": 7, "팔": 8, "구": 9 };
  const HOUR_KO = { "열두": 12, "열한": 11, "열": 10, "아홉": 9, "여덟": 8, "일곱": 7, "여섯": 6, "다섯": 5, "네": 4, "세": 3, "두": 2, "한": 1 };

  /* 한글 숫자(1~99)+단위 → 아라비아 숫자 — 음성 인식이 "삼 번출구"처럼 적는 것 교정 */
  function hnum(s) {
    const m = s.match(/^([일이삼사오육칠팔구])?(십)?([일이삼사오육칠팔구])?$/);
    if (!m || (!m[1] && !m[2] && !m[3])) return null;
    return m[2] ? (m[1] ? ONES[m[1]] : 1) * 10 + (m[3] ? ONES[m[3]] : 0) : ONES[m[1] || m[3]];
  }
  function fixNums(s) {
    // 숫자와 단위 사이에 공백이 있을 때만(음성 인식 패턴) — "이동" 같은 일반 단어 오변환 방지
    return s.replace(/(^|\s)([일이삼사오육칠팔구십]{1,3})\s+(번지|호선|번|호|층|동|명|개|회|주년)(?=(.)?)/g, (all, pre, num, unit, next) => {
      const n = hnum(num);
      if (n == null) return all;
      return pre + n + unit + (next && /[가-힣A-Za-z0-9]/.test(next) ? " " : ""); // "삼 번출구"→"3번 출구"
    });
  }

  function parse(text, todayYmd) {
    let t = " " + String(text).trim() + " ";
    // 음성 인식이 한글 숫자로 적는 시·분을 숫자로 변환 ("열시 십오분" → "10시 15분")
    t = t.replace(/(열두|열한|열|아홉|여덟|일곱|여섯|다섯|네|세|두|한)\s?시/g, (_, w) => HOUR_KO[w] + "시");
    t = t.replace(/([일이삼사오육칠팔구]?)십([일이삼사오육칠팔구]?)\s?분/g,
      (_, a, b) => ((a ? ONES[a] : 1) * 10 + (b ? ONES[b] : 0)) + "분");
    // 음성 인식 등 띄어쓰기 없는 입력 정규화: 날짜·시간 토큰 앞뒤에 공백 삽입
    t = t.replace(/다다음\s?주/g, "다다음주").replace(/(^|[^다])다음\s?주/g, "$1다음주").replace(/담주/g, "다음주"); // "다음 주" 표기 통일
    t = t.replace(/(오늘|내일|모레|오전|오후|저녁|밤|다다음주|다음주)/g, " $1 ");
    t = t.replace(/((?:다다음주|다음주)\s*)?([일월화수목금토])요일(?:에서|에는|에도|엔|에|의|부터|까지|쯤|경)?/g, " $1$2요일 ");
    t = t.replace(/(\d{1,2}\s?:\s?\d{2}|\d{1,2}시\s?\d{1,2}\s?분|\d{1,2}시\s?반|\d{1,2}월\s?\d{1,2}일|\d{1,2}\/\d{1,2}|\d{1,2}시|\d{1,2}일)\s?(에서|에는|에도|엔|에|의|부터|까지|쯤|경)?/g, " $1$2 ");
    const today = new Date(todayYmd + "T00:00:00");
    let date = null, m;

    if (/\s오늘\s/.test(t)) { date = new Date(today); t = t.replace(/\s오늘\s/, " "); }
    else if (/\s내일\s/.test(t)) { date = new Date(today); date.setDate(date.getDate() + 1); t = t.replace(/\s내일\s/, " "); }
    else if (/\s모레\s/.test(t)) { date = new Date(today); date.setDate(date.getDate() + 2); t = t.replace(/\s모레\s/, " "); }

    if (!date && (m = t.match(/\s(\d{1,2})[\/월]\s?(\d{1,2})일?(?:에서|에는|에도|엔|에|의|부터|까지|쯤|경)?\s/))) {   // M월 N일 / M/N
      date = new Date(today.getFullYear(), +m[1] - 1, +m[2]);
      if (ymd(date) < todayYmd) date.setFullYear(date.getFullYear() + 1);
      t = t.replace(m[0], " ");
    }
    if (!date && (m = t.match(/\s(\d{1,2})일(?:에서|에는|에도|엔|에|의|부터|까지|쯤|경)?\s/))) {                      // N일
      date = new Date(today.getFullYear(), today.getMonth(), +m[1]);
      if (ymd(date) < todayYmd) date.setMonth(date.getMonth() + 1);
      t = t.replace(m[0], " ");
    }
    if (!date && (m = t.match(/\s((다다음주|다음주)\s*)?([일월화수목금토])요일?\s/))) { // [다(다)음주] X요일
      date = new Date(today);
      let diff = (DOW[m[3]] - date.getDay() + 7) % 7;
      if (diff === 0) diff = 7;
      date.setDate(date.getDate() + diff + (m[2] === "다다음주" ? 14 : m[2] ? 7 : 0));
      t = t.replace(m[0], " ");
    }
    if (!date && (m = t.match(/\s(다다음주|다음주)\s/))) { // 요일 없이 "다음 주"만 = +7일(다다음 주 = +14일)
      date = new Date(today);
      date.setDate(date.getDate() + (m[1] === "다다음주" ? 14 : 7));
      t = t.replace(m[0], " ");
    }

    let ampm = null, time = null;
    if (/\s오전\s?/.test(t)) { ampm = "am"; t = t.replace(/\s오전\s?/, " "); }
    if (/\s(오후|저녁|밤)\s?/.test(t)) { ampm = "pm"; t = t.replace(/\s(오후|저녁|밤)\s?/, " "); }
    // 시간 표현 뒤 조사(에/에서/부터)는 흡수해서 제목에 안 남긴다
    if ((m = t.match(/\s(\d{1,2}):(\d{2})(?:에서|에는|에도|엔|에|의|부터|까지|쯤|경)?\s/))) { time = [+m[1], +m[2]]; t = t.replace(m[0], " "); }
    else if ((m = t.match(/\s(\d{1,2})시\s?(반|(\d{1,2})\s?분)?(?:에서|에는|에도|엔|에|의|부터|까지|쯤|경)?\s/))) {
      time = [+m[1], m[2] === "반" ? 30 : (m[3] ? +m[3] : 0)];
      t = t.replace(m[0], " ");
    }
    if (time) {
      let h = time[0];
      if (ampm === "pm" && h < 12) h += 12;
      else if (ampm === "am") { if (h === 12) h = 0; }
      else if (h >= 1 && h <= 7) h += 12;   // 무표기 1~7시 = 오후
      time = pad(h) + ":" + pad(time[1]);
    }
    return { title: fixNums(t.trim().replace(/\s+/g, " ")), date: ymd(date || today), time: time || null, hasDate: !!date };
  }
  return { parse };
});
