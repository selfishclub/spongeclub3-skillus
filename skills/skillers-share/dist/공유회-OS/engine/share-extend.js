(function () {
  var SLIDE_SEL = '.slide';
  var state = { segments: [], notes: {}, t0: null, timerOn: false, notesOn: false };

  function el(id, tag) {
    var n = document.getElementById(id);
    if (!n) { n = document.createElement(tag); n.id = id; document.body.appendChild(n); }
    return n;
  }

  // webdeck 은 페이지형 덱이라 현재 슬라이드에 .active 가 붙는다(`.slide.active .rv` 로 reveal).
  // 스크롤 위치로 찾으면 스크롤이 없는 덱에서 항상 0을 돌려준다.
  function currentIndex() {
    var slides = document.querySelectorAll(SLIDE_SEL);
    for (var i = 0; i < slides.length; i++) {
      if (slides[i].classList.contains('active')) return i;
    }
    // .active 를 쓰지 않는 스크롤형 덱 폴백
    for (var j = 0; j < slides.length; j++) {
      var r = slides[j].getBoundingClientRect();
      if (r.top <= window.innerHeight * 0.5 && r.bottom > window.innerHeight * 0.5) return j;
    }
    return 0;
  }

  function segmentAt(min) {
    var name = '', next = null;
    for (var i = 0; i < state.segments.length; i++) {
      if (state.segments[i][0] <= min) { name = state.segments[i][1]; next = state.segments[i + 1]; }
    }
    return { name: name, next: next };
  }

  function tick() {
    var box = el('sd-timer', 'div');
    if (!state.timerOn) { box.classList.remove('on'); return; }
    box.classList.add('on');
    var sec = state.t0 ? Math.floor((Date.now() - state.t0) / 1000) : 0;
    var min = Math.floor(sec / 60);
    var s = String(sec % 60).padStart(2, '0');
    var seg = segmentAt(min);
    var left = seg.next ? (seg.next[0] - min) + '분 남음' : '';
    box.innerHTML = min + ':' + s + '  <span class="seg">' + seg.name + (left ? ' · ' + left : '') + '</span>';
    box.classList.toggle('over', min >= 60);
  }

  function renderNotes() {
    var box = el('sd-notes', 'div');
    document.body.classList.toggle('sd-notes-on', state.notesOn);
    if (!state.notesOn) { box.classList.remove('on'); return; }
    box.classList.add('on');
    var i = currentIndex();
    var text = state.notes[String(i + 1)] || '(이 슬라이드의 노트가 없습니다)';
    box.innerHTML = '';
    var h = document.createElement('h4');
    h.textContent = 'SLIDE ' + (i + 1) + ' — 발표자 노트  ·  S 닫기';
    var p = document.createElement('pre');
    p.textContent = text;
    box.appendChild(h); box.appendChild(p);
  }

  document.addEventListener('keydown', function (e) {
    if (e.target && /^(INPUT|TEXTAREA)$/.test(e.target.tagName)) return;
    var k = e.key.toLowerCase();
    if (k === 's') { state.notesOn = !state.notesOn; renderNotes(); }
    if (k === 't') {
      state.timerOn = !state.timerOn;
      if (state.timerOn && !state.t0) state.t0 = Date.now();
      tick();
    }
    if (k === 'r' && e.shiftKey) { state.t0 = Date.now(); tick(); }
  });

  window.addEventListener('scroll', function () { if (state.notesOn) renderNotes(); }, { passive: true });

  fetch('notes.json')
    .then(function (r) { return r.ok ? r.json() : null; })
    .then(function (d) {
      if (!d) return;
      state.segments = d.segments || [];
      state.notes = d.notes || {};
    })
    .catch(function () {});

  // 페이지형 덱은 스크롤 이벤트가 없으므로 노트도 주기적으로 현재 슬라이드를 다시 읽는다.
  setInterval(function () { tick(); if (state.notesOn) renderNotes(); }, 1000);
})();
