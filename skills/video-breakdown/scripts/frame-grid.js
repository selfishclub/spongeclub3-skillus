// 영상 프레임 콘택트시트 + 컷 감지 — 브라우저 패널(javascript_tool)에서 실행
// 사용 순서:
//   1) resize_window 900x1600 (768 미만이면 모바일 UA로 바뀌어 m.youtube.com 자동재생이 안 됨)
//   2) 영상 URL navigate → 3초 대기
//   3) 이 파일 전체를 javascript_tool로 한 번 실행해 함수 등록 (페이지 이동 시 사라지므로 영상마다 다시 등록)
//   4) await __grid([t1..t9], 1.5) → computer screenshot 1장 = 프레임 9장
//   5) await __cuts(start, span, 1.5) → 컷 전환 시점 목록
//
// 왜 이렇게 만들었는지 (2026-09-17 실제로 실패했던 것들):
// - video 요소를 body로 옮기면 YouTube MSE 버퍼가 끊겨 readyState 0이 됨 → 요소는 건드리지 않고 캔버스에 복사만 함
// - 일시정지 후 currentTime 이동(seek)으로 뽑으면 seeked 이벤트는 와도 같은 프레임만 그려짐 → 재생하면서 시점 통과 시 캡처
// - 캔버스 하나에 여러 번 drawImage 하면 GPU 지연 렌더링 때문에 전 칸이 마지막 프레임으로 찍힘
//   → 프레임마다 별도 캔버스 + willReadFrequently + getImageData로 즉시 확정
// - 2.5배속 이상이면 디코딩이 못 따라가 같은 프레임 반복 → 1.5배속 고정
// - javascript_tool 45초 제한 → 호출 1회당 영상 약 55초(1.5배속 36초)까지만
// - requestVideoFrameCallback은 패널이 가려져 있으면 안 불림 → setInterval 폴링 사용

window.__grid = async function (times, rate) {
  if (document.visibilityState === 'hidden') return 'HIDDEN: 브라우저 패널이 안 보임. 사용자에게 패널을 열어두라고 요청 후 재호출';
  rate = rate || 1.5;
  const v = document.querySelector('video');
  v.muted = true;
  document.getElementById('__grid')?.remove();
  const grid = document.createElement('div');
  grid.id = '__grid';
  Object.assign(grid.style, {
    position: 'fixed', top: '0', left: '0', width: '900px', height: '1600px',
    zIndex: 2147483647, background: '#000', display: 'grid',
    gridTemplateColumns: 'repeat(3,300px)', gridAutoRows: '533px'
  });
  document.documentElement.appendChild(grid);
  const r = await captureOnce(v, grid, times, rate);
  if (r.stale) return 'STALE: 첫/끝 프레임 동일. 패널 가려짐 여부 확인 후 재호출. 그래도 같으면 정지 화면 영상 → ' + r.got.join(',');
  return r.got.join(',');
};

// 패널이 가려져 있으면(visibilityState hidden) 크롬이 영상 프레임 갱신을 멈춰서 전 칸이 같은 프레임으로 찍힘.
// 2026-09-17 해물탕 쇼츠에서 확인: 재시도·예열 모두 소용없었고 hidden 상태였음. 코드로 패널을 띄울 방법 없음
window.__visible = function () { return document.visibilityState; };

async function captureOnce(v, grid, times, rate) {
  // YouTube는 Trusted Types 정책이라 innerHTML 대입이 막힘
  grid.replaceChildren();
  v.currentTime = Math.max(0, times[0] - 0.2);
  v.playbackRate = rate;
  try { await v.play(); } catch (e) {}
  let idx = 0; const got = [];
  const thumbs = [];
  await new Promise(done => {
    const h = setInterval(() => {
      while (idx < times.length && v.currentTime >= times[idx]) {
        const c = document.createElement('canvas'); c.width = 300; c.height = 533;
        const g = c.getContext('2d', { willReadFrequently: true });
        g.drawImage(v, 0, 0, 300, 533);
        thumbs.push(g.getImageData(0, 0, 300, 533).data);
        g.fillStyle = '#f0f'; g.font = 'bold 22px sans-serif';
        g.fillText(v.currentTime.toFixed(1) + 's', 6, 26);
        grid.appendChild(c); got.push(v.currentTime.toFixed(1)); idx++;
      }
      if (idx >= times.length || v.ended) { clearInterval(h); v.pause(); done(); }
    }, 40);
    setTimeout(() => { clearInterval(h); v.pause(); done(); }, 40000);
  });
  // got이 비면 재생이 시작 안 된 것 → 호출한 쪽에서 시작 시점을 1~2초 바꿔 재호출
  // 첫 칸과 마지막 칸이 거의 같으면 멈춘 프레임으로 봄 (재시도 후에도 같으면 진짜 정지 화면일 수 있음)
  let stale = false;
  if (thumbs.length > 1) {
    const a = thumbs[0], b = thumbs[thumbs.length - 1];
    let s = 0; for (let i = 0; i < a.length; i += 40) s += Math.abs(a[i] - b[i]);
    stale = s / (a.length / 40) < 2;
  }
  return { got, stale };
}

// 컷 감지: 18x32로 줄인 프레임끼리 평균 픽셀 차이가 임계값을 넘으면 컷으로 봄
// 페이드·줌 전환은 놓칠 수 있으니 평균 컷 길이 추정용으로만 씀
window.__cuts = async function (start, span, rate) {
  if (document.visibilityState === 'hidden') return 'HIDDEN: 브라우저 패널이 안 보임. 사용자에게 패널을 열어두라고 요청 후 재호출';
  rate = rate || 1.5;
  const v = document.querySelector('video');
  v.muted = true;
  document.getElementById('__grid')?.remove();
  const c = document.createElement('canvas'); c.width = 18; c.height = 32;
  const g = c.getContext('2d', { willReadFrequently: true });
  v.currentTime = start; v.playbackRate = rate;
  try { await v.play(); } catch (e) {}
  let prev = null; const cuts = [];
  await new Promise(done => {
    const h = setInterval(() => {
      g.drawImage(v, 0, 0, 18, 32);
      const d = g.getImageData(0, 0, 18, 32).data;
      if (prev) {
        let s = 0;
        for (let i = 0; i < d.length; i += 4) s += Math.abs(d[i] - prev[i]) + Math.abs(d[i + 1] - prev[i + 1]) + Math.abs(d[i + 2] - prev[i + 2]);
        const m = s / (18 * 32 * 3);
        if (m > 35) cuts.push(v.currentTime.toFixed(1));
      }
      prev = d;
      if (v.currentTime >= start + span || v.ended) { clearInterval(h); v.pause(); done(); }
    }, 100);
    setTimeout(() => { clearInterval(h); v.pause(); done(); }, 40000);
  });
  return cuts.join(' ');
};

// 메타데이터: SPA 이동 후엔 ytInitialPlayerResponse가 이전 영상일 수 있어 videoId 일치 확인 필수
window.__meta = function (videoId) {
  const v = document.querySelector('video');
  const pr = window.ytInitialPlayerResponse;
  const same = !!(pr && pr.videoDetails && pr.videoDetails.videoId === videoId);
  return {
    same,
    title: document.title,
    duration: v && v.duration, width: v && v.videoWidth, height: v && v.videoHeight,
    author: same ? pr.videoDetails.author : null,
    description: same ? pr.videoDetails.shortDescription : null,
    captions: same && pr.captions ? pr.captions.playerCaptionsTracklistRenderer.captionTracks.map(c => c.languageCode + ':' + (c.kind || 'manual')) : [],
    pageText: document.body.innerText.slice(0, 600)
  };
};
'registered';
