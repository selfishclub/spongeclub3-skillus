/* 스토어 진단 — 증거 추출기 (6판)
 *
 * ── 5판에서 뭐가 달라졌나 ────────────────────────────────
 * **43 추가이미지를 크기가 아니라 이름표로 센다.** 담헌 실측에서 썸네일이 40×40 이라
 * 「55~120px」 그물을 통째로 빠져나가 **9장을 0장**으로 셌다. 캡처엔 줄이 또렷했다.
 * 네이버가 alt="추가이미지0"… 을 붙여 준다 — 그걸 먼저 보고, 없을 때만 크기로 어림한다.
 * 그리고 출력의 판 표기가 5판에서도 「4판」으로 남아 있던 것을 바로잡았다.
 *
 * ── 4판에서 뭐가 달라졌나 ────────────────────────────────
 * **쇼핑스토리를 홈 절에서 `fetch` 로 같이 받는다.** 화면 순회가 넷에서 **셋**으로 줄었다.
 * 4판은 「쇼핑스토리 탭은 로그인 벽이라 못 뽑는다」고 적었는데 **틀렸다.**
 * 「이동」이 막히는 것이지 스토어가 막은 게 아니다 — 목록 페이지와 똑같은 벽이고
 * `fetch` 하면 200 이다. 루리에 글이 4개 있었다.
 * 그리고 42 할인율을 카드 상자까지 올라가서 센다 (링크 안쪽만 보면 0 이 나온다).
 *
 * ── 아래는 4판 설명 ─────────────────────────────────────
 *
 * 스토어 진단 — 증거 추출기 (4판)
 *
 * 판정 기준표(01_기획/리포트_판정기준표.md) **6판 · 88줄**을 겨냥해 증거를 뽑는다.
 *
 * ── 3판에서 뭐가 달라졌나 ────────────────────────────────
 * 기준표가 6판이 되며 다섯 가지가 어긋났다.
 *
 *  1. **켬과 보임을 둘 다 세야 한다.** 3판은 19·29·37 셋만 둘 다 적었다.
 *     루리 홈에서 켠 위젯 9개 중 화면에 그려진 건 4개였다. 23·24·25·29·31 이
 *     설정만 보고 매겨지고 있었다. → **홈에서도 화면을 훑어 그려진 구역을 센다**
 *     세는 기준선은 **메인배너(promotionBannerWidget)** 다. 그 아래만 센다
 *
 *  2. **공지 구역과 상세설명을 갈라야 한다.** 3판은 div#DEFAULT 안에서 둘을
 *     섞어 셌다. 46(상세설명 5,000px)과 85(공지가 이미지냐 텍스트냐)가 갈렸다
 *
 *  3. **쇼핑스토리 화면이 재료에 들어왔다.** 81·82 가 글 제목과 썸네일을 본다.
 *     **탭 이름은 스토어마다 다르다.** 「쇼핑스토리」라는 글자로 찾으면 놓친다 —
 *     홈에서 상단 메뉴를 통째로 뽑아 두고, 검수가 어느 탭인지 고른다
 *
 *  4. **새 줄 여덟(81~88)** 이 붙었다. 앞 번호는 밀지 않았다
 *
 *  5. **용어를 통일했다** — 대표이미지(1장) · 추가이미지(9장) · 영상(1개) = 미디어 11개.
 *     정가 → **정상가**, 판매가 → **할인가**
 *
 * ── 쓰는 법 (5판 기준) ──────────────────────────────────
 * 스토어 하나에 **세 번** 돌린다. **화면은 셋만 연다.**
 *   1) 스토어 홈으로 이동        → 이 파일을 browser_evaluate 에
 *   2) 상품 상세로 이동          → 다시
 *   3) **다른 상품** 상세로 이동 → 또 한 번
 *
 * **쇼핑스토리는 열지 않는다.** 홈 절이 `fetch` 로 같이 받는다.
 * (4판은 여기에 「쇼핑스토리 탭으로 이동」 네 번째가 있었는데, 이동은 로그인으로
 *  튕기고 `fetch` 는 200 이라 필요 없어졌다.)
 *
 * 홈에서 돌리면 결과의 `증거.0` 에 **다음에 열 상품 두 개**와 **상단 메뉴 전부**가 들어 있다.
 *
 * **상세를 두 개 여는 건 6번 때문이 아니다.** 6판에서 6번 조건이 「설정만 돼 있으면」
 * 으로 뒤집혀 비교가 필요 없어졌다. 그래도 두 개를 여는 건 47·86·88 처럼
 * **상품마다 다른 줄**이 여럿이라서다. 하나만 보면 그 스토어를 봤다고 할 수 없다.
 *
 * 일반 스마트스토어의 상세는 **m.smartstore.naver.com** 주소로 이동해야 열린다.
 * 데스크톱 주소로 넘어가며 화면이 다 그려진다.
 *
 * ── 이 파일이 지키는 것 ─────────────────────────────────
 * 1. 판정하지 않는다. 증거만 뽑는다. ⭕❌ 는 검수가 기준표를 보고 매긴다
 * 2. 증거에 줄 번호를 붙인다
 * 3. **「켰나」와 「보이나」를 구분해서 둘 다 적는다.**
 *    **「왜 안 보이나」는 여기서 단정하지 않는다.** 그건 판정이다
 * 4. 원격 코드를 실행하지 않는다. :undefined → :null 치환 후 JSON.parse 만
 * 5. **가를 규칙이 불안하면 덩어리째 남긴다.** 47 옵션 이름이 그렇다 —
 *    라벨과 값의 순서가 상품마다 달라 코드로 못 가른다. 검수가 읽는다
 * 6. **못 뽑으면 못뽑음에 적는다.** 추정해서 채우지 않는다.
 *    끝내 안 뽑히는 줄은 기준표에서 ➖ 로 내리고 「잊지 않았나요」로 보낸다
 *
 * ── 속도 ────────────────────────────────────────────────
 * **네이버는 몰아서 두드리면 429 를 준다.** 요청 사이 1.5초, 429 면 그 자리에서 멈춘다.
 * fetch 는 홈에서 목록 한 번뿐이다. 상세·쇼핑스토리는 화면을 읽는다.
 *
 * ⚠ 이 파일을 sed·python 으로 부분 치환하지 말 것. \s 이스케이프가 어긋나
 *   조용히 실패한다. 고칠 땐 통째로 다시 쓴다.
 */

async () => {
  // ══ 공통 ════════════════════════════════════════════
  const ev = {};
  const put = (n, v) => { if (v !== null && v !== undefined && v !== '') ev[n] = v; };
  const 못뽑음 = [];
  const 쉬기 = ms => new Promise(r => setTimeout(r, ms));
  const 글 = e => ((e && e.innerText) || '').trim();
  const 한줄 = s => (s || '').replace(/\s+/g, ' ').trim();
  const 위 = e => Math.round(e.getBoundingClientRect().top + window.scrollY);
  const 보임 = e => !!(e && e.offsetHeight > 0 && e.offsetWidth > 0);
  const 버튼포함 = re => [...document.querySelectorAll('button, a')].find(e => re.test(글(e)));

  const 팝업닫기 = () => {
    [...document.querySelectorAll('[role=dialog] button, [class*=Dialog] button, [class*=dialog] button')]
      .filter(e => /닫기|close/i.test(글(e) + (e.getAttribute('aria-label') || '')))
      .forEach(b => { try { b.click(); } catch (x) {} });
  };
  // 빈 dialog 껍데기가 문서 앞쪽에 여러 개 있다. querySelector 로 첫 개를 집으면
  // 글이 없는 걸 잡는다. **보이면서 글이 제일 많은 것**을 고른다.
  const 대화글 = () => {
    const ds = [...document.querySelectorAll('[role=dialog], [class*=Dialog], [class*=dialog]')]
      .filter(d => d.offsetHeight > 100 && ((d.innerText || '').trim().length > 30));
    if (!ds.length) return null;
    const d = ds.reduce((a, b) => (((b.innerText || '').length > (a.innerText || '').length) ? b : a));
    return (d.innerText || '').replace(/\n{2,}/g, '\n');
  };
  const 훑어내리기 = async () => {
    for (let y = 0; y < document.documentElement.scrollHeight; y += 1000) {
      window.scrollTo(0, y); await 쉬기(140);
    }
    window.scrollTo(0, 0); await 쉬기(500);
  };
  // 설정 원본에서 키를 이름으로 뒤진다. 자리를 모르는 설정을 찾을 때 쓴다.
  // 84(알림받기 노출 설정)가 그 자리다 — 어느 키에 들어 있는지 확인 안 됐다.
  const 키찾기 = (obj, re, 깊이) => {
    const 나온것 = []; let 본노드 = 0;
    const 걷기 = (o, 길, d) => {
      if (!o || typeof o !== 'object' || d > (깊이 || 4) || 본노드 > 4000) return;
      for (const k of Object.keys(o)) {
        본노드++; if (본노드 > 4000) return;
        const v = o[k]; const p = 길 ? 길 + '.' + k : k;
        if (re.test(k) && (typeof v === 'boolean' || typeof v === 'string' || typeof v === 'number')) {
          나온것.push(p + ' = ' + v);
        }
        if (v && typeof v === 'object' && !Array.isArray(v)) 걷기(v, p, d + 1);
      }
    };
    try { 걷기(obj, '', 0); } catch (x) {}
    return 나온것.slice(0, 30);
  };

  const 갈래 = /brand\.naver\.com/.test(location.hostname) ? '브랜드스토어'
            : /smartstore\.naver\.com/.test(location.hostname) ? '일반' : '알수없음';
  const base = location.origin + '/' + (location.pathname.split('/')[1] || '');
  const 상세인가 = /\/products\/\d+/.test(location.pathname);
  const ST = window.__PRELOADED_STATE__ || null;
  const 홈인가 = !상세인가 && !!(ST && ST.homeSetting);
  const 스토리인가 = !상세인가 && !홈인가;

  // 기준표 6판 기준
  const 캡처로판정 = [13, 17, 19, 30, 33, 34, 53, 54, 81];
  const 채점안함 = [11, 18, 21, 36, 37, 38, 39, 41, 45, 48, 49, 52, 57, 58, 59, 60, 61, 65, 66];
  const 원리적불가 = [7, 8, 10, 12, 70, 74, 77, 78, 87];
  const 전체줄수 = 88;

  // ══════════════════════════════════════════════════════
  // 상세 화면 — 눌러서 열고 훑어서 읽는다
  // ══════════════════════════════════════════════════════
  if (상세인가) {
    const 상품번호 = (location.pathname.match(/products\/(\d+)/) || [])[1];

    put(5, document.title);
    put(6, {
      값: (document.querySelector('meta[name=description]') || {}).content,
      비고: '6판에서 조건이 뒤집혔다. 설정만 돼 있으면 ⭕ 다. 상품 간 비교는 이제 필요 없다'
    });

    // ── 4 카테고리 경로 ────────────────────────────────
    // 화면이 이미 부른 요청의 주소에서 읽는다. 새로 두드리지 않는다.
    try {
      const 주소 = performance.getEntriesByType('resource').map(r => r.name)
        .find(u => /category-navigations/.test(u));
      const m = 주소 && 주소.match(/wholeCategoryName=([^&]+)/);
      put(4, {
        경로: m ? decodeURIComponent(m[1]).replace(/>/g, ' > ') : null,
        출처: 주소 ? '화면이 부른 category-navigations 요청' : null,
        비고: '어느 카테고리에 넣었는지는 채점하지 않는다. 끝까지 지정됐는지만 본다'
      });
      if (!주소) 못뽑음.push('4 카테고리 경로 — category-navigations 요청을 못 찾았다');
    } catch (x) { 못뽑음.push('4 카테고리 경로 — ' + String(x).slice(0, 50)); }

    // ── 43 · 44 · 88 미디어 — 펼치기 전에 잡는다 ────────
    // 갤러리는 상세설명을 펼치면 화면이 다시 그려져 자리가 바뀐다.
    const 리뷰탭0 = [...document.querySelectorAll('*')].find(e => /^리뷰\s*\d+$/.test(글(e)));
    const 리뷰탭위 = 리뷰탭0 ? 위(리뷰탭0) : 1e9;
    const 갤러리안 = e => 위(e) < Math.min(1600, 리뷰탭위);
    const 대표후보 = [...document.querySelectorAll('img')]
      .filter(i => 갤러리안(i) && i.naturalWidth >= 300 && i.offsetWidth >= 200);
    // ★ 5판 실측(담헌) — 크기로 어림하면 못 센다. 썸네일이 **40×40** 이라
    // 「55~120px」 그물을 통째로 빠져나가 **9장을 0장**으로 셌다. 캡처엔 줄이 또렷했다.
    // 네이버가 `alt="추가이미지0"…` 을 붙여 준다. **이름표를 먼저 본다.**
    // 이름표가 없는 스토어를 만나면 그때 크기로 어림한다 — 그물은 30px 까지 넓혔다.
    const 이름표추가 = [...document.querySelectorAll('img[alt^="추가이미지"]')].filter(보임);
    const 어림추가 = [...document.querySelectorAll('img')]
      .filter(i => 갤러리안(i) && i.offsetWidth >= 30 && i.offsetWidth <= 120);
    const 추가후보 = 이름표추가.length ? 이름표추가 : 어림추가;
    const 영상 = [...document.querySelectorAll('video')].filter(v => 위(v) < 리뷰탭위);
    put(43, {
      대표이미지: 대표후보.length ? 1 : 0,
      대표이미지크기: 대표후보[0] ? { 원본: 대표후보[0].naturalWidth + '×' + 대표후보[0].naturalHeight,
                                    화면: 대표후보[0].offsetWidth + '×' + 대표후보[0].offsetHeight } : null,
      추가이미지후보: 추가후보.length,
      추가이미지alt: 추가후보.map(i => 한줄(i.alt).slice(0, 20)),
      센방법: 이름표추가.length ? 'alt="추가이미지N" 이름표' : '크기 어림 (30~120px) — 이름표를 못 찾았다',
      크기로어림한수_참고: 어림추가.length,
      영상: 영상.length,
      미디어합계후보: (대표후보.length ? 1 : 0) + 추가후보.length + 영상.length,
      비고: '최대 11개(대표1+추가9+영상1)가 기준이다. ★ 크기 어림으로 셌으면 다른 상품 카드가 섞일 수 있다 — 검수가 alt 를 보고 거른다'
    });
    put(44, {
      영상수: 영상.length,
      비율: 영상.map(v => (v.videoWidth && v.videoHeight) ? v.videoWidth + '×' + v.videoHeight : null),
      비고: '1:1 정방형이어야 대표이미지 구역에서 정상 노출된다. 리뷰 영역 아래의 video 는 뺐다'
    });
    // 88 — 갤러리를 끝까지 넘기면 리뷰 칸이 나온다
    // ★ 4판 실측 — 「리뷰이벤트」 배너를 갤러리 리뷰 칸으로 잘못 집었다. 그건 다른 것이다
    const 리뷰칸후보 = [...document.querySelectorAll('a, button, div')]
      .filter(e => 갤러리안(e) && /^(리뷰|포토리뷰|리뷰\s*\d)/.test(글(e)) && 글(e).length < 20)
      .filter(e => !/리뷰이벤트|리뷰\s*이벤트/.test(글(e)));
    put(88, {
      갤러리끝리뷰칸: 리뷰칸후보.length > 0,
      후보: 리뷰칸후보.slice(0, 4).map(e => 한줄(글(e)).slice(0, 20)),
      비고: '대표이미지 갤러리 끝의 리뷰 칸이다. 리뷰 탭(본문 아래)과 다르다 — 위치로 갈랐다'
    });
    // 86 — 대표이미지 · 상품명 · 첫 옵션명이 같은 상품을 가리키나
    const 상품명 = 한줄((document.querySelector('h3') || document.querySelector('h2') || {}).innerText || document.title);
    put(86, {
      상품명: 상품명.slice(0, 80),
      대표이미지alt: 대표후보[0] ? 한줄(대표후보[0].alt).slice(0, 80) : null,
      첫옵션명: null,
      비고: '첫 옵션명은 47 구매영역 덩어리에서 검수가 읽는다. 셋이 어긋나면 어뷰징으로 상품이 삭제될 수 있다 — 위험도 최상'
    });

    // ── 팝업을 닫고 상세정보를 펼친다 ──────────────────
    팝업닫기();
    await 쉬기(500);
    const 펼침 = 버튼포함(/상세정보 펼쳐보기/);
    if (펼침) { 펼침.scrollIntoView({ block: 'center' }); await 쉬기(400); 펼침.click(); await 쉬기(2500); }
    else 못뽑음.push('「상세정보 펼쳐보기」 버튼이 없다 — 이미 펼쳐져 있거나 자리가 다르다');

    // 지연 로딩을 깨운다. 안 하면 이미지 장수와 세로합을 덜 센다 (9장 → 12장)
    await 훑어내리기();

    // ── 46 상세설명 · 85 공지 구역 ─────────────────────
    // **`.se-main-container` 만 보면 안 된다.** 스마트에디터로 안 올린 셀러가 있다.
    // 루리코리아 젓가락 상품이 그랬다 — SE 컨테이너엔 공지 한 장뿐이고
    // 상세설명 15,457px 짜리는 `div#DEFAULT` 안에 그냥 img 로 박혀 있었다.
    //
    // **4판은 둘을 가른다.** 상품등록에서 넣으면 공지사항 → 상세설명 순으로 그려진다.
    // 그래서 #DEFAULT 안의 최상위 덩어리를 **문서 순서대로** 늘어놓고
    // 각각의 높이·이미지수·글자수를 적는다. **경계는 검수가 정한다.**
    const se = [...document.querySelectorAll('.se-main-container')];
    const 영역 = document.getElementById('DEFAULT')
              || (se.length ? se.reduce((a, b) => (b.offsetHeight > a.offsetHeight ? b : a)) : null);
    if (영역) {
      // ★ 4판 실측 — `#DEFAULT` 의 자식이 하나뿐인 스토어가 있다. 그러면 못 가른다.
      // 루리가 그랬다: 자식 1개 26,628px 인데 `.se-main-container` 는 둘이었다 —
      // **1,024px 1장(공지)** 과 **24,886px 12장(상세설명)**. 이미 갈라져 있었다.
      // 그래서 SE 컨테이너가 둘 이상이면 그걸 덩어리로 쓴다.
      // SE 컨테이너가 하나뿐인데 그 밖에 이미지가 더 있으면, 그 하나가 공지고
      // 나머지 날 이미지가 상세설명이다. 스마트에디터로 안 올린 셀러가 그렇다 —
      // 루리 젓가락 상품이 그랬다: SE 1,024px 1장 + 날 이미지 여러 장.
      const 밖이미지 = [...영역.querySelectorAll('img')]
        .filter(i => i.offsetHeight > 100 && !se.some(c => c.contains(i)));
      const 덩어리원본 = se.length >= 2 ? se
        : (se.length === 1 && 밖이미지.length ? [se[0], { 밖: 밖이미지 }]
        : [...영역.children].filter(보임));
      const 덩어리 = 덩어리원본.map((c, idx) => {
        const 날것 = !!c.밖;
        const im = 날것 ? c.밖 : [...c.querySelectorAll('img')].filter(i => i.offsetHeight > 100);
        return {
          순서: idx + 1,
          어디: 날것 ? 'SE 밖의 날 이미지' : '.se-main-container',
          높이: 날것 ? im.reduce((a, i) => a + i.offsetHeight, 0) : c.offsetHeight,
          이미지수: im.length,
          세로합: im.reduce((a, i) => a + i.offsetHeight, 0),
          글자수: 날것 ? 0 : 한줄(c.innerText).length,
          첫글: 날것 ? '' : 한줄(c.innerText).slice(0, 60)
        };
      });
      // 공지는 **위쪽의 작은 덩어리**다. 덩어리가 하나뿐이면 못 가른 것이니 공지후보를 비운다.
      // 46 이 이 값을 써야 해서 85 보다 먼저 잡는다.
      const 세로합계 = 덩어리.reduce((a, x) => a + x.세로합, 0);
      const 공지후보 = 덩어리.length >= 2
        ? 덩어리.filter(d => d.순서 <= 2 && d.세로합 < 세로합계 * 0.3)
        : [];
      const 상세설명세로합 = 덩어리
        .filter(d => !공지후보.some(n => n.순서 === d.순서))
        .reduce((a, x) => a + x.세로합, 0);

      const imgs = [...영역.querySelectorAll('img')].filter(i => i.offsetHeight > 100);
      put(46, {
        전체이미지수: imgs.length,
        전체세로합: imgs.reduce((a, i) => a + i.offsetHeight, 0),
        전체글자수: 한줄(영역.innerText).length,
        덩어리: 덩어리,
        출처: document.getElementById('DEFAULT') ? 'div#DEFAULT (상세설명 탭 전체)' : 'se-main-container',
        덩어리출처: se.length >= 2 ? '.se-main-container ' + se.length + '개'
                  : (se.length === 1 && 밖이미지.length ? 'SE 1개 + 밖의 날 이미지 ' + 밖이미지.length + '장'
                  : '#DEFAULT 의 자식'),
        상세설명세로합: 상세설명세로합,
        공지몫: 세로합계 - 상세설명세로합,
        se컨테이너: se.map(c => ({ 높이: c.offsetHeight, 이미지: c.querySelectorAll('img').length })),
        기준: '상세설명만의 세로합이 5,000px 이상이어야 ⭕ (6판에서 3,000 → 5,000 으로 올랐다)',
        비고: '★ 상세설명세로합이 5,000px 과 견줄 값이다. 공지 몫은 이미 뺐다 — 덩어리가 하나뿐이면 못 가른 것이라 전체가 그대로 들어간다'
      });
      // 85 — 공지 구역이 이미지냐 텍스트냐
      put(85, {
        공지후보: 공지후보,
        텍스트만인덩어리: 덩어리.filter(d => d.이미지수 === 0 && d.글자수 > 30).length,
        기준: '공지 구역은 이미지로 등록돼야 ⭕. 네이버 AI 쇼핑에이전트가 이미지를 읽게 되며 GEO 가 중요해졌다',
        비고: '특별한 중요 공지가 아닌데 텍스트로 들어가 있으면 감점이다. 어디까지가 공지인지는 검수가 정한다'
      });
      const 첫 = imgs.slice().sort((a, b) => 위(a) - 위(b))[0];
      put(45, {
        첫이미지: 첫 ? { 원본: 첫.naturalWidth + '×' + 첫.naturalHeight, 화면높이: 첫.offsetHeight } : null,
        비고: '채점 보류 줄. 캡처만 남긴다 — 이 이미지가 보이는 상태에서 뷰포트 캡처를 찍을 것'
      });
    } else 못뽑음.push('46·85 상세설명 — div#DEFAULT 도 se-main-container 도 못 찾았다');

    // ── 3 태그 ─────────────────────────────────────────
    const 태그 = [...document.querySelectorAll('a, span')].map(e => 글(e))
      .filter(t => /^#[^\s#]{1,20}$/.test(t));
    const 태그목록 = [...new Set(태그)].slice(0, 20);
    put(3, {
      개수: 태그목록.length, 태그: 태그목록,
      기준: '최대 10개. 등록만 돼 있으면 ⭕ 지만 최대한 채우는 것을 권장한다 — 리포트에 숫자를 적는다'
    });

    // ── 47 옵션 · 50 · 51 상품정보 표 ──────────────────
    const 본문 = document.body.innerText;
    const 줄들 = 본문.split('\n').map(s => s.trim());

    const i배송 = 본문.indexOf('배송비');
    const i구매 = 본문.indexOf('구매하기');
    put(47, {
      구매영역: (i배송 >= 0 && i구매 > i배송) ? 한줄(본문.slice(i배송, i구매)).slice(0, 500) : null,
      기준: '6판 조건은 「규칙이 일관되나」다. 「옐로 5개」와 「5개 블루」처럼 순서가 뒤섞이면 ❌',
      비고: '옵션 라벨과 값의 순서가 상품마다 달라 코드로 못 가른다. 덩어리째 남긴다 — 검수가 읽는다. 86 의 첫 옵션명도 여기서 읽는다'
    });

    const s표 = 줄들.indexOf('상품번호');
    const 표 = s표 >= 0 ? 줄들.slice(s표, s표 + 60) : 줄들;
    const 라벨값 = 라벨 => {
      const i = 표.indexOf(라벨);
      return i >= 0 ? (표.slice(i + 1).find(s => s && s !== '복사') || null) : null;
    };
    put(50, {
      제조사: 라벨값('제조사'), 브랜드: 라벨값('브랜드'),
      비고: '상품정보 표의 값이다. 고시 표에는 「상품상세참조」로 돼 있을 수 있다 — 자리가 둘이다'
    });
    put(51, 라벨값('원산지'));

    // ── 53 사이즈 정보 — 「둘」 줄이다. 존재는 구조로, 질은 캡처로 ──
    const 사이즈표 = [...document.querySelectorAll('table')]
      .filter(보임)
      .filter(t => /(사이즈|치수|SIZE|총장|가슴|어깨|허리)/i.test(글(t)));
    put(53, {
      사이즈표: 사이즈표.length,
      머리글: 사이즈표.slice(0, 2).map(t => 한줄(글(t)).slice(0, 120)),
      사이즈단어: (본문.match(/사이즈|치수/g) || []).length,
      비고: '패션이 아니면 ⊘ 다. 표가 이미지 안에 구워져 있으면 여기 안 잡힌다 — 캡처로 한 번 더 본다'
    });

    // ── 52 · 62 눌러야 열리는 팝업 둘 ──────────────────
    const 고시 = 버튼포함(/상품정보제공고시/);
    if (고시) {
      고시.click(); await 쉬기(1400);
      const t = 대화글();
      if (t) {
        put(52, {
          참조회수: (t.match(/상품상세\s*참조|상세페이지\s*참조/g) || []).length,
          본문: 한줄(t).slice(0, 1500),
          비고: '채점 안 하는 줄이다. 네이버가 틀과 표준 문구를 내려준다. 리포트에 사실로 적을 값만 남긴다'
        });
        // 63 A/S 는 고시 표 안에 있다. 반품 팝업이 아니다
        const as = t.match(/A\/S 책임자와 전화번호\n([^\n]*)/);
        put(63, { 고시AS: as ? 한줄(as[1]) : null, 비고: '「상세정보 확인」이면 자리는 있는데 안 채운 것이다' });
      } else 못뽑음.push('52 고시 — 버튼은 눌렀는데 팝업 글을 못 읽었다');
      팝업닫기(); await 쉬기(700);
    } else 못뽑음.push('52 고시 — 「상품정보제공고시 보기」 버튼이 없다');

    const 반품 = 버튼포함(/반품\/교환안내/);
    if (반품) {
      반품.click(); await 쉬기(1500);
      const t = 대화글();
      if (t) {
        const 잡기 = re => { const m = t.match(re); return m ? 한줄(m[0]) : null; };
        put(62, {
          반품배송비: 잡기(/반품배송비[^\n]*/),
          교환배송비: 잡기(/교환배송비[^\n]*/),
          지정택배사: 잡기(/판매자 지정 택배사[^\n]*/),
          보내실곳: 잡기(/보내실 곳[^\n]*/),
          비고: '불가 사유 7가지는 네이버 공통 문구다. 배송비·택배사·반송지가 셀러가 넣은 값이다'
        });
      } else 못뽑음.push('62 반품·교환 — 버튼은 눌렀는데 팝업 글을 못 읽었다');
      팝업닫기(); await 쉬기(700);
    } else 못뽑음.push('62 반품·교환 — 「반품/교환안내」 버튼이 없다');

    // ── 54 상단 띠배너 · 55 · 64 · 68 · 71 · 76 ─────────
    const 별점 = 본문.match(/\d\.\d{1,2}\s*\(최근 6개월[^)]*\)/);
    put(55, {
      요약: 별점 ? 한줄(별점[0]).replace(/도움말/g, '').replace(/\s+/g, ' ').trim() : null,
      리뷰수: (본문.match(/리뷰\s*(\d[\d,]*)/) || [])[1] || null
    });
    put(64, {
      쿠폰단어: (본문.match(/쿠폰/g) || []).length,
      쿠폰받기버튼: !!버튼포함(/쿠폰\s*받기|쿠폰\s*다운/),
      알림받기쿠폰: /알림받기.*쿠폰|쿠폰.*알림받기/.test(한줄(본문)),
      기준: '☆ 하면 좋은 것. 상품·시기 따라 안 걸 수도 있다. 다만 낮은 퍼센트의 알림받기 쿠폰은 권장'
    });
    put(68, { 톡톡문의버튼: !!버튼포함(/톡톡문의/), 비고: '스토어를 열면 자동으로 붙는지 확인이 안 됐다. 붙는다면 채점 제외 후보' });
    put(71, {
      리뷰포인트단어: (본문.match(/포인트/g) || []).length,
      텍스트리뷰: /텍스트\s*리뷰/.test(본문), 포토리뷰: /포토|동영상\s*리뷰/.test(본문)
    });
    put(76, {
      자동응답: /자동응답|챗봇/.test(본문),
      QnA답변완료: (본문.match(/답변완료/g) || []).length,
      QnA미답변: (본문.match(/미답변|답변대기/g) || []).length,
      비고: '세부설정은 톡톡 파트너센터에 있어 밖에서 못 본다 → 「잊지 않았나요」'
    });

    // ── 29 숏클립 ──────────────────────────────────────
    put(29, {
      숏클립단어: (본문.match(/숏클립/g) || []).length,
      비고: '「관련 숏클립」 제목이 떴다가 사라지면 등록된 클립이 0개다. 훑어 내린 뒤의 값이 진짜다'
    });

    // ── 72 리뷰 답글 — 맨 마지막에 한다 ─────────────────
    // 리뷰 창을 닫으면 화면이 다시 그려져 앞서 잡아둔 것이 날아간다.
    const 리뷰 = 버튼포함(/^리뷰 전체보기$/);
    if (리뷰) {
      리뷰.scrollIntoView({ block: 'center' }); await 쉬기(400);
      리뷰.click(); await 쉬기(2500);
      for (let n = 0; n < 6; n++) { window.scrollBy(0, 1200); await 쉬기(300); }
      await 쉬기(800);
      const T = document.body.innerText;
      put(72, {
        답글단어: (T.match(/답글/g) || []).length,
        본리뷰수: (T.match(/[a-zA-Z0-9]+\*+\d{2}\.\d{2}\.\d{2}\./g) || []).length,
        비고: '답글이 0 이면 노출된 리뷰에 판매자 답글이 없다는 뜻. 몇 건을 보고 한 말인지 같이 남긴다'
      });
    } else 못뽑음.push('72 리뷰 답글 — 「리뷰 전체보기」 버튼이 없다');

    return {
      메타: { 화면: '상세', url: location.href, 상품번호, 갈래, 스토어: base, 판: '6판', 못뽑음 },
      증거: ev,
      비고: '홈·쇼핑스토리에서 뽑는 줄은 여기 없다. 홈에서 한 번, 쇼핑스토리 탭에서 한 번 더 돌릴 것',
      캡처로판정해야하는줄: 캡처로판정
    };
  }

  // ══════════════════════════════════════════════════════
  // 쇼핑스토리 화면 — 81 · 82 (4판에서 새로 생김)
  // ══════════════════════════════════════════════════════
  // **탭 이름이 스토어마다 다르다.** 그래서 「쇼핑스토리」라는 글자를 안 찾는다.
  // 홈이 아니고 상세도 아닌 화면이면 여기로 온다 — 검수가 맞는 탭을 열어준 것으로 본다.
  if (스토리인가) {
    await 훑어내리기();

    // 글 카드를 찾는다. 카드 = 링크 안에 이미지가 있고 글이 붙은 것.
    const 카드 = [...document.querySelectorAll('a')]
      .filter(a => 보임(a) && a.querySelector('img') && 글(a).length > 2 && a.offsetHeight > 80)
      .map(a => {
        const im = a.querySelector('img');
        return {
          제목: 한줄(글(a)).slice(0, 80),
          썸네일: im ? { 원본: im.naturalWidth + '×' + im.naturalHeight,
                        화면: im.offsetWidth + '×' + im.offsetHeight,
                        비율: (im.naturalWidth && im.naturalHeight)
                              ? (im.naturalWidth / im.naturalHeight).toFixed(2) : null,
                        alt: 한줄(im.alt).slice(0, 40) } : null,
          주소: a.href
        };
      });
    // 같은 글이 두 번 잡히는 걸 막는다
    const 본주소 = {}; const 글목록 = [];
    for (const c of 카드) { if (!본주소[c.주소]) { 본주소[c.주소] = 1; 글목록.push(c); } }

    if (글목록.length) {
      put(82, {
        글수: 글목록.length,
        제목: 글목록.map(c => c.제목),
        기준: '제목에 규칙이 있고 단순하지 않아야 ⭕. 규칙 없이 지어졌거나 너무 단순하면 ❌',
        비고: '규칙이 있는지는 코드로 못 정한다. 제목을 통째로 남긴다 — 검수가 읽는다'
      });
      put(81, {
        썸네일: 글목록.map(c => ({ 제목: c.제목.slice(0, 30), 썸네일: c.썸네일 })),
        기준: '글마다 썸네일이 따로 제작돼 있어야 ⭕. 글자나 이미지가 잘려 있으면 ❌',
        비고: '★ 잘렸는지는 캡처를 봐야 안다. 원본과 화면 크기의 비율이 어긋나면 잘린 것이다 — 캡처를 같이 찍을 것'
      });
      put(83, {
        글제목: 글목록.map(c => c.제목),
        비고: '민감 카테고리(건강기능식품·의료기기 등)를 판다면 인증을 뒷받침하는 글이 있는지 검수가 본다. 민감 카테고리가 아니면 ⊘'
      });
    } else 못뽑음.push('81·82 쇼핑스토리 — 글 카드를 못 찾았다. 탭이 맞는지, 등록된 글이 있는지 확인할 것');

    return {
      메타: { 화면: '쇼핑스토리(추정)', url: location.href, 갈래, 스토어: base, 판: '6판', 못뽑음 },
      증거: ev,
      비고: '이 화면이 정말 쇼핑스토리 탭인지는 코드가 단정하지 않는다. 홈이 아니고 상세도 아니라서 여기로 왔다',
      캡처로판정해야하는줄: [81]
    };
  }

  // ══════════════════════════════════════════════════════
  // 홈 화면 — 설정 원본 + 화면에 그려진 것
  // ══════════════════════════════════════════════════════
  const parseState = html => {
    const i = html.indexOf('__PRELOADED_STATE__');
    if (i < 0) return null;
    const s = html.indexOf('{', i);
    let d = 0, end = -1, inStr = false, esc = false;
    for (let p = s; p < html.length; p++) {
      const c = html[p];
      if (inStr) { if (esc) esc = false; else if (c === '\\') esc = true; else if (c === '"') inStr = false; continue; }
      if (c === '"') inStr = true; else if (c === '{') d++; else if (c === '}') { d--; if (d === 0) { end = p + 1; break; } }
    }
    if (end < 0) return null;
    try { return JSON.parse(html.slice(s, end).replace(/:\s*undefined/g, ':null')); } catch (e) { return null; }
  };
  let 멈춤 = false;
  let 요청수 = 0;
  const pull = async url => {
    if (멈춤) { 못뽑음.push(url + ' — 앞에서 429 를 만나 중단했다'); return null; }
    if (요청수 > 0) await 쉬기(1500);
    요청수++;
    try {
      const r = await fetch(url, { credentials: 'include' });
      if (r.status === 429) {
        멈춤 = true;
        못뽑음.push(url + ' — HTTP 429 (속도 제한). 여기서 멈춘다. 시간을 두고 다시 할 것');
        return null;
      }
      if (/nid\.naver\.com/.test(r.url)) { 못뽑음.push(url + ' — 로그인 벽'); return null; }
      if (!r.ok) { 못뽑음.push(url + ' — HTTP ' + r.status); return null; }
      const st = parseState(await r.text());
      if (!st) 못뽑음.push(url + ' — HTTP 200 인데 __PRELOADED_STATE__ 를 못 찾았다');
      return st;
    } catch (e) { 못뽑음.push(url + ' — ' + String(e).slice(0, 60)); return null; }
  };

  const HOME = ST;
  if (!HOME) return { 오류: '홈의 __PRELOADED_STATE__ 를 못 찾았다. 스토어 홈에서 실행해야 한다.' };

  // ── 화면에 그려진 구역을 센다 ★ 4판 ────────────────
  // 설정이 켜져 있어도 담은 상품이 없으면 구역 자체가 안 그려진다.
  // 루리는 켠 9개 중 4개만 그려졌다. **켬과 보임을 둘 다 적는다.**
  // **「왜 안 보이나」는 여기서 단정하지 않는다.** 그건 판정이다.
  await 훑어내리기();

  const 배너요소 = [...document.querySelectorAll('img, div')]
    .filter(e => 보임(e) && e.offsetHeight > 180 && 위(e) < 1400 && e.offsetWidth > 600);
  const 기준선 = 배너요소.length ? 위(배너요소[0]) : 0;

  // 후보를 모은다 — 상품이나 이미지가 든, 기준선 아래의 큰 덩어리
  const 후보 = [...document.querySelectorAll('#content > *, #content div, section')]
    .filter(보임)
    .filter(e => e.offsetHeight > 150 && e.offsetWidth > 500)
    .map(e => ({
      el: e, 위: 위(e), 높이: e.offsetHeight,
      상품수: e.querySelectorAll('a[href*="/products/"]').length,
      이미지수: [...e.querySelectorAll('img')].filter(i => i.offsetHeight > 60).length
    }))
    .filter(c => c.위 >= 기준선 && (c.상품수 > 0 || c.이미지수 > 0));

  // ★ 래퍼를 버린다 — 4판 실측에서 잡은 병.
  // 같은 구역이 바깥 div 와 안쪽 div 로 두 번 세어져 4개가 8개로 나왔다.
  // C 안에 D 가 있고 D 가 C 의 내용을 절반 이상 담고 있으면 C 는 껍데기다.
  const 알맹이 = 후보.filter(c => !후보.some(d =>
    d !== c && c.el.contains(d.el) &&
    (c.상품수 > 0 ? d.상품수 * 2 >= c.상품수 : d.이미지수 * 2 >= c.이미지수)));

  // 구역 제목은 **첫 상품 카드보다 위에** 있는 글이다.
  // `a[href*=products]` 안인지만 보면 안 된다 — 카드 제목이 링크 밖에 있는 스토어가 있다.
  // 루리가 그랬다: 제목을 찾으라 했더니 첫 상품 이름을 집어 왔다.
  // 그리고 **구역에서 250px 넘게 떨어진 글은 남의 제목**이다. 안 그러면 제목 없는 구역이
  // 위 구역의 제목을 훔쳐 온다.
  const 구역제목 = (el, 위치) => {
    let n = el;
    for (let i = 0; i < 5 && n; i++) {
      const 첫상품 = n.querySelector('a[href*="/products/"]');
      const 한계 = 첫상품 ? 위(첫상품) : 1e9;
      const h = [...n.querySelectorAll('h2, h3, strong')]
        .find(x => 보임(x) && 위(x) < 한계 && 위(x) >= 위치 - 250 && 글(x).length > 0 && 글(x).length <= 40);
      if (h) return 한줄(글(h));
      n = n.parentElement;
    }
    return '';
  };
  const 그려진구역 = 알맹이
    .map(c => ({ 제목: 구역제목(c.el, c.위) || '(제목 없음)', 위: c.위, 높이: c.높이, 상품수: c.상품수, 이미지수: c.이미지수 }))
    .sort((a, b) => a.위 - b.위);

  // ══ 홈 위젯 — ② 첫인상 ══════════════════════════════
  const W = (HOME.homeSetting && HOME.homeSetting.displayConfig && HOME.homeSetting.displayConfig.widgets) || {};
  const 켬 = k => (W[k] ? W[k].visible === true : null);
  const 순서 = k => (W[k] && typeof W[k].order === 'number') ? W[k].order : null;
  const 메인배너순서 = 순서('promotionBannerWidget');
  const 위젯목록 = Object.keys(W)
    .map(k => ({ 위젯: k, order: 순서(k), 켬: W[k] && W[k].visible === true,
                 제목: (W[k] && W[k].title) ? W[k].title : (W[k] && W[k].title === '' ? '(제목 비어 있음)' : null) }))
    .sort((a, b) => (a.order === null ? 99 : a.order) - (b.order === null ? 99 : b.order));
  const 기준선아래켠것 = 위젯목록.filter(w => w.켬 && 메인배너순서 !== null && w.order > 메인배너순서);

  const 배너 = (W.promotionBannerWidget && W.promotionBannerWidget.items) || [];
  put(13, {
    위젯켬: 켬('promotionBannerWidget'),
    배너수: 배너.length, 켜진것: 배너.filter(b => b && b.visible !== false).length,
    문구: 배너.map(b => (b.title || '') + (b.description ? ' / ' + b.description : '')).filter(x => x.trim()),
    비고: '★ 6판에서 「사람」 줄이 됐다. 자동으로 안 매긴다 — 정숙님이 직접 본다'
  });
  put(14, {
    링크걸린배너: 배너.filter(b => b.linkUrl).length, 전체: 배너.length,
    도착지: 배너.filter(b => b.linkUrl).map(b => b.linkUrl).slice(0, 5),
    기준: '링크가 걸렸는지에 더해 어디로 가는지까지 본다. 쇼핑스토리로 보내는 것이 권장 — 일반 상품도 ⭕'
  });
  put(19, {
    켬: 켬('benefitBannerWidget'),
    보임: 그려진구역.some(s => /쿠폰|혜택|적립/.test(s.제목)),
    기준: '☆ 하면 좋은 것. 권장은 알림받기 쿠폰을 걸어 첫 방문 고객을 잡는 것',
    비고: '켰는데 안 보이면 발행한 쿠폰이 없는 것이다. 처방은 「켜세요」가 아니라 「채우세요」'
  });
  put(23, {
    켬: 켬('bestProductWidget'), 제목: (W.bestProductWidget || {}).title,
    보임: 그려진구역.filter(s => /베스트|BEST/i.test(s.제목)).map(s => ({ 제목: s.제목, 상품수: s.상품수 })),
    기준: '☆ 하면 좋은 것 · 권장: 등록'
  });
  put(25, {
    켬: 켬('newProductWidget'),
    보임: 그려진구역.filter(s => /신상품|NEW/i.test(s.제목)).map(s => ({ 제목: s.제목, 상품수: s.상품수 })),
    기준: '☆ 하면 좋은 것 · 권장: 등록'
  });
  put(26, { 켬: 켬('bestReviewWidget'), 기준: '☆ 하면 좋은 것 · 권장: 등록' });
  put(27, { 켬: 켬('exhibitionBannerWidget') });
  put(28, { 켬: 켬('shoppingStoryWidget'), 비고: '메뉴에 있어도 홈 위젯이 꺼져 있으면 홈엔 안 뜬다. 글의 질은 81·82 에서 본다' });
  put(24, {
    자유상품위젯: Object.keys(W).filter(k => /customProductWidget/.test(k))
      .map(k => ({ 위젯: k, order: 순서(k), 켬: W[k].visible,
                   제목: W[k].title === '' ? '(제목 비어 있음)' : W[k].title })),
    화면에그려진구역: 그려진구역.map(s => ({ 제목: s.제목, 상품수: s.상품수 })),
    기준: '☆ 하면 좋은 것 · 권장: 등록. 제목에 사는 이유가 담겨야 ⭕',
    비고: '★ 제목이 비었는데 화면에도 없으면 담은 상품이 없는 것이다. 「제목만 넣으면 된다」는 틀린 처방 — 상품부터 담아야 한다'
  });
  put(31, {
    기준선: { 위젯: 'promotionBannerWidget', order: 메인배너순서, 화면Y: 기준선 },
    켠것_기준선아래: 기준선아래켠것.length,
    켠것목록: 기준선아래켠것,
    화면에그려진구역수: 그려진구역.length,
    화면에그려진구역: 그려진구역,
    전체위젯: 위젯목록,
    기준: '메인배너 아래로 화면에 그려진 구역이 3개 이상이면 ⭕',
    비고: '★ 켬과 보임을 둘 다 적는다. 왜 안 보이는지는 여기서 단정하지 않는다 — 그건 판정이다'
  });

  const CS = HOME.commonSetting || {};
  put(30, { colorType: CS.colorType, colorCode: CS.colorCode });

  const CM = HOME.categoryMenu || {};
  const 하위 = ((CM.storeCategoryTree || {}).subCategories) || [];
  put(20, 하위.map(c => c.name));
  put(22, {
    최상위수: 하위.length,
    하위가진것: 하위.filter(c => (c.subCategories || []).length).map(c => c.name + '(' + c.subCategories.length + ')'),
    표시방식: CM.categoryDisplayType
  });
  put(15, (HOME.channel || {}).channelName || document.title);
  put(16, (document.querySelector('meta[name=description]') || {}).content);
  put(17, { 비고: '캡처로 판정' });

  const SNS = [...document.querySelectorAll('a[href]')].map(a => a.href)
    .filter(h => /instagram|youtube|facebook|tiktok|x\.com|twitter|blog\.naver\.com\/(?!MyBlog)/.test(h));
  put(32, {
    스토어에걸린링크: [...new Set(SNS)].slice(0, 6),
    스토어명: (HOME.channel || {}).channelName || null,
    기준: '★ 6판에서 ⊘ 를 없앴다. SNS 를 안 할 리 없으니 링크가 없으면 ❌ 다',
    비고: '★ 수집 단계에서 스토어명으로 인스타·블로그를 실제로 찾아본 결과를 여기 붙일 것. 코드가 못 한다'
  });

  // 84 — 알림받기 노출 설정 (스토어전시 컴포넌트). 자리를 몰라 이름으로 뒤진다
  // ★ 4판 실측 — 넓게 뒤졌더니 라운지·멤버십 키만 걸렸다.
  // naverMembership.isSubscribed · loungeNotifyReceiveAgreeYn · loungeMember.agree* 따위로
  // **스토어전시의 알림받기 노출 설정과는 무관하다.** 위젯 목록에도 그런 위젯이 없다.
  const 알림위젯 = Object.keys(W).filter(k => /(notif|alarm|알림)/i.test(k));
  const 알림키 = 키찾기(HOME, /(notifyExpos|alarmExpos|notifyButton|notifyVisible|알림받기)/i, 5);
  put(84, {
    알림관련위젯: 알림위젯,
    좁게찾은키: 알림키,
    넓게찾은키_참고: 키찾기(HOME, /(notif|alarm)/i, 4),
    sellerInfo위젯: 켬('sellerInfoWidget'),
    기준: '스토어전시에서 알림받기 버튼 컴포넌트를 켰는지. 18번(모든 스토어 기본 버튼)과 다르다',
    비고: '★ 4판 실측 결과 이 설정은 홈 state 에 없다. 라운지·멤버십 키만 걸린다 — ➖ 로 내리고 「잊지 않았나요」로 보낸다'
  });
  if (!알림위젯.length && !알림키.length) {
    못뽑음.push('84 알림받기 노출 설정 — 위젯에도 state 에도 없다. ★ ➖ 확정 후보');
  }

  // ══ 목록 설정 — ③ 고르기 ════════════════════════════
  const PLS = HOME.productListSetting || {};
  const U = PLS.productUnitAddInfo || {};
  put(35, {
    imageShapeType: PLS.imageShapeType,
    기준: '★ 6판에서 조건이 바뀌었다. 1:1 정방형, 되도록 1000×1000px. 취향이 아니라 규칙이다',
    비고: 'SQUARE 가 아니면 ❌. 실제 픽셀은 목록 화면 이미지에서 확인할 것'
  });
  // ★ 4판 실측 — 설정에 discountRateVisible 이라는 키가 아예 없다.
  // productUnitAddInfo 의 키는 reviewRating · reviewCount · colorChip · detailForPc ·
  // cart · bestOrNewTag · productAttributeTag 일곱뿐이다.
  // 그래서 할인율은 설정이 아니라 **화면의 카드**에서 센다.
  // ★ 4판 두 번째 실측 — 상품 링크(`a`) 안쪽 글만 보면 0개가 나온다.
  // 할인율은 링크 **밖**, 카드 영역에 있다. 캡처엔 「40% 29,250원」이 또렷했다.
  // 그래서 링크에서 위로 올라가 **값이 든 카드 상자**를 찾아 그 글을 본다.
  const 카드상자 = a => {
    let n = a;
    for (let i = 0; i < 4 && n && n.parentElement; i++) {
      n = n.parentElement;
      if (/원/.test(글(n))) return n;
    }
    return a;
  };
  const 링크들 = [...document.querySelectorAll('a[href*="/products/"]')].filter(보임);
  const 볼것 = 링크들.slice(0, 40).map(카드상자);
  const 카드퍼센트 = 볼것.filter(c => /\d{1,2}\s*%/.test(글(c))).length;
  const 카드별점 = 볼것.filter(c => /\d\.\d{1,2}/.test(글(c))).length;
  const 카드리뷰수 = 볼것.filter(c => /리뷰\s*\d/.test(글(c))).length;
  const 카드수 = 링크들.length;
  put(42, {
    reviewRatingVisible: U.reviewRatingVisible,
    reviewCountVisible: U.reviewCountVisible,
    할인율노출설정: U.discountRateVisible !== undefined ? U.discountRateVisible : '설정에 그런 키가 없다',
    할인율보이는카드: 카드퍼센트, 별점보이는카드: 카드별점, 리뷰수보이는카드: 카드리뷰수,
    본카드수: Math.min(카드수, 40),
    설정키전체: Object.keys(U),
    기준: '★ 6판에서 할인율 노출이 조건에 더해졌다. 별점·리뷰수·할인율 셋',
    비고: '★ 할인율은 설정에 자리가 없어 화면 카드에서 % 표기를 센다. 링크 안쪽만 보면 0 이 나온다 — 카드 상자까지 올라가서 본다'
  });

  // ══ 상세 설정 — 셀러가 켜고 끈 것 ═══════════════════
  const PDS = ((HOME.productDetailSetting || {}).displayConfig) || {};
  const TNB = PDS.topNoticeBannerManagement || {};
  put(54, {
    useTopNoticeBanner: TNB.useTopNoticeBanner,
    문구: TNB.benefitTypeText || TNB.benefitDescription || null,
    기준: '☆ 하면 좋은 것 · 권장: 행사 있을 때. 네이버 공통 띠는 제외 — 판매자가 건 것만'
  });
  put(56, {
    자사추천: {
      함께구매: PDS.useTogetherProducts, 스토어인기: PDS.useSellerBestProducts,
      배송비절약: PDS.useBundleDeliveryProducts, 다른구성: PDS.useOtherCompositionProducts,
      관심상품: PDS.useInterestProducts, AiTEMS: PDS.useAitems
    },
    기준: '필수 세팅 권장. AiTEMS 는 자사 추천이라 여기 넣었다 — 57 은 6판에서 채점에서 빠졌다'
  });
  put(29, {
    켬: PDS.useShortClip, validMenu: (CM.validMenu || {}).isLiveValid,
    기준: '☆ 하면 좋은 것 · 권장: 등록',
    비고: '컴포넌트를 켰어도 등록된 클립이 없을 수 있다. 상세 화면에서 다시 볼 것'
  });
  // ★ 4판 실측 — PDS 에 정기구독 키가 없었다. 검색필터 쪽에 흔적이 있다
  put(67, {
    상세설정에서: 키찾기(PDS, /(subscri|정기)/i, 3),
    검색필터에서: 키찾기(HOME.searchFilter || {}, /(SUBSCRIPTION|정기)/i, 4),
    기준: '★ 6판에서 예약구매는 빠지고 정기구독만 남았다. 해당 상품이 아니면 ⊘',
    비고: '둘 다 비면 상세 화면에서 봐야 한다. 옵션 2개 이상 + 정기구독이면 나중에 그룹상품으로 못 바꾼다'
  });

  // ══ 목록 화면 — 상품 실물 ═══════════════════════════
  const 목록state = await pull(base + '/category/ALL?cp=1');
  const CP = (목록state && 목록state.categoryProducts) || {};
  const 상품 = CP.simpleProducts || [];
  if (상품.length) {
    const 이름 = 상품.slice(0, 10).map(p => p.name);
    put(1, 이름);
    put(2, { 상품명: 이름, 기준: '★ 6판에서 문장을 고쳤다. 아래 금지어가 상품명에 하나도 없어야 ⭕' });
    put(79, { 상품명: 이름, 기준: '★ 6판에서 조건이 뒤집혔다. 같은 뜻의 말이 여러 번 나오는 것은 정상이다 — 광고·검색 노출용 키워드다' });
    put(80, { 상품명: 이름, 기준: '색상·용량·수량 같은 주요 속성. 그룹상품이면 네이버 기본 옵션명 형식을 따르면 ⭕' });
    put(40, {
      가격: 상품.slice(0, 12).map(p => ({
        정상가: p.salePrice, 할인가: (p.benefitsView || {}).discountedSalePrice || null
      })),
      기준: '☆ 하면 좋은 것 · 권장: 적절한 할인율 표기. 네이버는 의도적 과다할인을 금지한다',
      비고: '★ 용어 통일 — 취소선 그은 것이 정상가, 크게 노출되는 것이 할인가'
    });
    put(42, Object.assign(ev[42] || {}, {
      리뷰있는상품: 상품.filter(p => ((p.reviewAmount || {}).totalReviewCount || 0) > 0).length,
      전체: 상품.length
    }));
    put(9, {
      상품: 상품.slice(0, 12).map(p => ({ 이름: (p.name || '').slice(0, 30), 옵션있음: p.optionUsable })),
      기준: '☆ 하면 좋은 것 · 권장: 조건부 — 옵션이 많아 드롭다운이 불편하거나 키워드별 광고를 돌릴 때만 유리'
    });
    put(31, Object.assign(ev[31] || {}, { 스토어상품수: CP.totalCount || 상품.length }));
  } else 못뽑음.push('목록 상품 배열 — categoryProducts.simpleProducts 가 비었다');

  // ══ 그 밖 — ⑥ 다시 오기 ════════════════════════════
  // ══ 쇼핑스토리 — 81 · 82 · 83 ★ 5판 ════════════════
  // **화면을 열지 않는다.** 「이동」하면 로그인으로 튕기지만 그건 우리 도구 문제다.
  // 목록 페이지와 똑같은 벽이고, `fetch` 하면 200 이며 state 에 글이 다 들어 있다.
  // 4판은 이걸 「로그인 벽이라 못 뽑는다」고 잘못 적었다 — 실제로는 글 4개가 있었다.
  const 스토리state = await pull(base + '/shoppingstory/list?cp=1');
  const SS = (스토리state && 스토리state.shoppingStory) || null;
  const 스토리목록 = (SS && SS.list && Array.isArray(SS.list.contents)) ? SS.list.contents : null;
  if (스토리목록) {
    const 글들 = 스토리목록.map(p => ({
      제목: 한줄(p.postTitle || ''),
      등록일: (p.regDate || '').slice(0, 10),
      조회: p.readCount,
      전시: p.postDisplayStatusType,
      이미지: (p.editorImageInfos || []).map(im => ({
        이름: im.imageName, 가로: im.width, 세로: im.height,
        비율: (im.width && im.height) ? (im.width / im.height).toFixed(2) : null,
        대표: im.representative
      }))
    }));
    put(82, {
      글수: (SS.list.totalElements !== undefined ? SS.list.totalElements : 글들.length),
      제목: 글들.map(g => g.제목),
      등록일: 글들.map(g => g.등록일),
      기준: '제목에 규칙이 있고 단순하지 않아야 ⭕',
      비고: '규칙이 있는지는 코드로 못 정한다. 제목을 통째로 남긴다 — 검수가 읽는다'
    });
    put(81, {
      대표지정한글: 글들.filter(g => g.이미지.some(i => i.대표)).length,
      전체글: 글들.length,
      이미지: 글들.map(g => ({ 제목: g.제목.slice(0, 24), 이미지: g.이미지 })),
      기준: '글마다 썸네일이 따로 제작돼 있어야 ⭕',
      비고: '★ 대표(representative)가 하나도 없고 본문용 세로 긴 이미지뿐이면 목록 카드에서 잘린다. 비율이 1 에서 멀수록 그렇다'
    });
    put(83, {
      글제목: 글들.map(g => g.제목),
      비고: '민감 카테고리를 판다면 인증을 뒷받침하는 글이 있는지 검수가 본다. 민감 카테고리가 아니면 ⊘'
    });
    put(28, Object.assign(ev[28] || {}, {
      실제글수: 글들.length,
      비고: '홈 위젯을 꺼도 쇼핑스토리 탭에는 글이 있을 수 있다. 28 은 홈 위젯, 81·82 는 글의 질이다'
    }));
  } else 못뽑음.push('81·82 쇼핑스토리 — shoppingStory.list.contents 를 못 찾았다. fetch 는 됐는지 확인할 것');

  put(73, { reviewEvent: HOME.reviewEvent ? Object.keys(HOME.reviewEvent) : null, validMenu리뷰: (CM.validMenu || {}).isReviewEventValid });
  // ★ 4판 실측 — 키찾기로 notice.detail 만 뒤져 빈 값이 나왔다. list 를 직접 읽는다
  const N = HOME.notice || {};
  const 공지배열 = Array.isArray(N.list) ? N.list
                 : (N.list && Array.isArray(N.list.contents)) ? N.list.contents
                 : (N.list && Array.isArray(N.list.items)) ? N.list.items : null;
  put(75, {
    공지수: 공지배열 ? 공지배열.length : null,
    공지: 공지배열 ? 공지배열.slice(0, 12).map(n => ({
      제목: 한줄(n.title || n.postTitle || '').slice(0, 50),
      날짜: n.regDate || n.registerDate || n.startDate || null,
      전시: n.exposureYn !== undefined ? n.exposureYn : (n.exposed !== undefined ? n.exposed : null)
    })) : null,
    notice키: Object.keys(N),
    list생김새: N.list && !Array.isArray(N.list) ? Object.keys(N.list) : null,
    기준: '★ 6판 조건이 「걸려 있다」 → 「관리되고 있나」로 바뀌었다. 개수가 적고 기간 지난 것은 전시중지돼야 ⭕',
    비고: '개수와 날짜를 봐야 한다. 배열을 못 찾으면 공지 탭을 따로 열어야 한다'
  });
  if (!공지배열) 못뽑음.push('75 공지 — notice.list 에서 배열을 못 찾았다. list생김새를 보고 다음 판에서 길을 고칠 것');
  put(69, {
    benefit: HOME.benefit ? Object.keys(HOME.benefit) : null,
    benefitBanner켬: 켬('benefitBannerWidget'),
    비고: '19(쿠폰 띠)·84(노출 설정)와 한 묶음이다. 셋이 있어야 알림받기 수가 쌓인다'
  });

  // ── 다음에 열 화면 ─────────────────────────────────
  // ★ 4판 실측 — nav·Menu 셀렉터로는 하나도 안 잡혔다. 스토어 안 링크를 통째로 훑는다.
  // 상단 메뉴는 스토어 주소로 시작하면서 상품·카테고리가 아닌 짧은 링크다.
  const 메뉴 = [...document.querySelectorAll('a[href]')]
    .filter(보임)
    .filter(a => a.href.indexOf(base) === 0 && 위(a) < 700)
    .map(a => ({ 이름: 한줄(글(a)).slice(0, 20), 주소: a.href, 위: 위(a) }))
    .filter(m => m.이름 && m.이름.length <= 12 && !/\/products\//.test(m.주소)
                 && m.주소.replace(base, '').length > 1);
  const 본메뉴 = {}; const 메뉴목록 = [];
  for (const m of 메뉴) { if (!본메뉴[m.주소]) { 본메뉴[m.주소] = 1; 메뉴목록.push(m); } }
  put(0, {
    상세로열것: 상품.slice(0, 2).map(p => ({ 번호: p.productNo, 이름: (p.name || '').slice(0, 40) })),
    상단메뉴: 메뉴목록.slice(0, 20),
    비고: '★ 쇼핑스토리 탭은 여기서 고른다. **탭 이름이 스토어마다 다르다** — 「쇼핑스토리」라는 글자로 찾지 말 것. ' +
          '카테고리·리뷰·문의가 아닌 것이 후보다. 그 주소로 이동해 이 파일을 한 번 더 돌린다'
  });

  const 전체 = Array.from({ length: 전체줄수 }, (_, i) => i + 1);
  const 상세에서뽑는줄 = [3, 4, 5, 6, 29, 43, 44, 45, 46, 47, 50, 51, 52, 55, 62, 63, 64, 68, 71, 72, 76, 85, 86, 88];
  const 스토리에서뽑는줄 = [];   // ★ 5판 — 81·82·83 을 홈 절에서 fetch 로 같이 받는다
  return {
    메타: {
      화면: '홈', url: location.href, 갈래, 스토어: base, 판: '6판',
      state읽음: { 홈: !!HOME, 목록: !!목록state },
      못뽑음
    },
    증거: ev,
    안뽑힌줄: 전체.filter(n => !(n in ev) && 캡처로판정.indexOf(n) < 0
                    && 채점안함.indexOf(n) < 0 && 원리적불가.indexOf(n) < 0
                    && 상세에서뽑는줄.indexOf(n) < 0 && 스토리에서뽑는줄.indexOf(n) < 0),
    상세에서뽑는줄,
    스토리에서뽑는줄,
    캡처로판정해야하는줄: 캡처로판정,
    비고: '기준표 6판 88줄 기준. 채점 안 함 19 · 원리적 불가 9'
  };
}
