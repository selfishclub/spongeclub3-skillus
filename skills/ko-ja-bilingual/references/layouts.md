# Page skeleton, components, layouts

The design language here was reverse-engineered from a real LY deck (*2026 LINE Creators Market AWARD 事業部間コラボレーション提案*). Everything below matches `assets/deck-base.html` — if you write markup that isn't in this file, it will render unstyled.

---

## 1. Page skeleton

Every slide is the same two-layer structure: a soft gradient ground, and a white panel floating on it. Never put content directly in `.slide`.

```html
<section class="slide" data-layout="headline-body">
  <div class="panel">
    <div class="pill blue">EYEBROW</div>
    <h1>結論を述べるタイトル</h1>
    <p class="lead">1〜4行の説明。</p>
    <div class="body"> … </div>
    <div class="foot"><span>左</span><span>右</span></div>
    <div class="pageno"></div>
  </div>
</section>
```

`.pageno` is filled in by script — **leave it empty**. Typing `01 / 07` by hand is how page numbers end up wrong after a slide gets cut, which is exactly the kind of small error that costs credibility in a 本社 review.

`.foot` is optional; use it for the owner line, not for decoration.

### Stage size

Default is 16:9 (1920×1080) for projection. Add `class="a4"` to `<body>` for A4 landscape (1414×1000) — the denser, document-style format the reference deck uses, better when the deck will be read on screen or printed rather than presented. The type scale adjusts automatically.

---

## 2. Components

### Eyebrow pill — `.pill`
A small colour-tinted label above the headline. It orients the reader ("what kind of slide is this") in one glance, which matters more than it sounds in a 20-slide deck.

```html
<div class="pill green">RESULT</div>     <!-- green tint -->
<div class="pill blue">EVENT OVERVIEW</div>
<div class="pill amber">HIGHLIGHTS</div>  <!-- solid amber, dark text -->
<div class="pill pink">RISK</div>
<div class="pill">DEFAULT — violet</div>
<div class="pill plain">開催規模</div>     <!-- solid dark, sentence case -->
```

### Gradient headline — `.grad`
The signature move of the reference deck: line one plain black, line two running through the brand colours. Reserve it for the cover, section openers, and the closing ask — a gradient on every slide stops reading as emphasis.

```html
<h1>6月ポップアップ、<br><span class="grad cool">売上は計画比 118%</span> で着地</h1>
```
- `.grad` — green → blue → violet → pink (the full run, best on long phrases)
- `.grad cool` — green → blue → violet (calmer; use for results and numbers)
- `.grad warm` — amber → pink → violet (use for proposals and asks)

Apply it to a **phrase**, not the whole line. The contrast between plain and gradient text is what creates the emphasis; gradient-on-gradient has none.

Inline single colours: `.c-green .c-pink .c-amber .c-violet .c-blue`, plus `.pos` / `.neg` for deltas and `.hi` for a soft green highlighter behind text.

### Stat bar — `.statbar`
A dark band of 2–5 headline numbers. Strong on a cover slide, right under the lead.

```html
<div class="statbar" style="--n:4">
  <div class="stat"><div class="k">売上</div><div class="v c-green">45.3<small>百万円</small></div></div>
  <div class="stat"><div class="k">計画達成率</div><div class="v c-amber">118<small>%</small></div></div>
  <div class="stat"><div class="k">客単価</div><div class="v c-pink">3,940<small>円</small></div></div>
  <div class="stat"><div class="k">来場者数</div><div class="v">11,800<small>名</small></div></div>
</div>
```
Set `--n` to the number of columns. Units go in `<small>` — keep them to a true unit (`%`, `円`, `名`, `%p`). Pushing a phrase in there (`월 목표`) crowds the number; move the qualifier up into `.k` instead. Colour rotation green → amber → pink → white reads as variety, not as meaning — if one number is the point of the slide, colour only that one.

### Cards — `.grid` + `.card`
```html
<div class="grid" style="--cols:3">
  <div class="card">
    <div class="top"><span class="tag">01 在庫</span><span class="n">要承認</span></div>
    <h2>初動物量 1.5倍</h2>
    <p>文具の人気SKUに限定し、初期投入量を1.5倍へ。</p>
    <div class="inset"><div class="k c-green">想定効果</div><p>欠品由来の損失 約2.4百万円を回収</p></div>
  </div>
  …
</div>
```
A card can carry an image: `<img class="thumb" src="img/x.jpg" alt="">` as its first child (add `contain` when the whole image matters). This is how an illustration stays attached to the claim it supports instead of drifting onto a separate gallery slide.

Variants: `.card.dark` (dark navy, green title — good for concept slides), `.card.mark` (green border + glow, for the one option you are recommending). `.inset` is pinned to the card bottom so insets align across unequal-length cards.

`--cols:2` or `3`. Four columns only works with very short text.

Add `.fill` (`<div class="grid fill">`) when the cards **are** the slide's content, so the row stretches to fill the panel instead of floating in the middle with dead space above and below. Leave it off when the grid sits alongside a callout or table and should keep its natural height. Pair `.fill` with `.inset` on each card: stretching a card without giving its lower half something to hold just moves the dead space inside the card. In the reference deck every full-height card carries an inset — a 想定効果, a 副賞案, a next step — and that is what makes a tall card read as deliberate rather than unfinished.

### Callout — `.callout`
One soft green bar, centred, for the single sentence you want remembered. Once per slide at most.

### Bars — `.bars`
For distributions and plan-versus-actual on a slide, where a table would make the reader do the comparison themselves.
Pure CSS, no script. `--v` is the percentage (largest bar = 100%); the real figure goes in `.val`, so a reader who
needs the number never estimates it from a length. Series colours are `s1`–`s4`.

```html
<div class="legend"><span class="s1">여성</span><span class="s2">남성</span></div>
<div class="bars">
  <div class="row"><span class="lbl">20대</span>
    <div class="track"><span class="b s1" style="--v:100%"></span><span class="val">41.0%</span></div></div>
</div>
```

### Table, images, timeline
```html
<table><thead><tr><th>カテゴリ</th><th>計画</th><th>実績</th><th>達成率</th></tr></thead>
<tbody><tr><td>ぬいぐるみ</td><td>18.0</td><td>23.4</td><td class="pos">130%</td></tr>
       <tr><td>合計</td><td>38.4</td><td>45.3</td><td class="pos">118%</td></tr></tbody></table>
```
When a table has more than about 8 rows or 6 columns it will overflow the fixed stage. Add `dense` to the section (`<section class="slide dense" ...>`) to tighten row padding and drop to caption size — that buys roughly 12 extra rows. Splitting a financial table across two slides is usually worse than one dense slide, because the reader loses the totals row.

Numbers right-align automatically and the last `<tbody>` row is styled as a total. State the unit once in `.lead` or a caption, never per cell.

```html
<div class="figs" style="--cols:2">
  <figure class="fig"><img src="img/1.jpg" alt=""><figcaption>入口フォトゾーン</figcaption></figure>
</div>
```
Add `.contain` (`<div class="figs contain">`) when the images are **evidence rather than atmosphere** — product shots, precedent cases, screenshots, packaging. The default `cover` crops to fill the cell, which is right for mood photography and wrong for anything the audience is meant to examine: a cropped product shot quietly destroys the reason the slide exists. `contain` letterboxes each image whole on a soft background. Keep evidence grids to **3 per slide (one row)**: with `--cols:3` a single row gives each cell the full body height, while a 3×2 grid halves it and the images stop being examinable — which defeats the point of showing them. Six precedents belong on two slides, not one.

Keep images external in an `img/` folder beside the HTML. Inlining 100 photos as base64 produces a file too heavy to open; if it must travel as a single file, downscale to ~1600px first.

```html
<div class="steps">
  <div class="step"><div class="when">9月</div><p>コンセプト確定</p></div>
  <div class="step"><div class="when">10月</div><p>商品開発・発注</p></div>
</div>
```

---

## 3. Layouts

`data-layout` mostly documents intent; only `cover`, `section` and `closing` change the panel's appearance (the latter two invert it to dark).

| Layout | Earns its place when | Avoid when |
|---|---|---|
| `cover` | Opening. Headline + lead + stat bar. Once per deck. | — |
| `section` | Dark divider at a real gear change | Fewer than 3 slides follow |
| `headline-body` | The default: one claim, then evidence | More than 5 points — split |
| `two-col` | Genuine pairs: 計画/実績, 国内/日本, before/after | The halves aren't parallel |
| `cards` | 2–3 peer items, options, or actions | 4+ items — use a table |
| `big-number` | 2–3 metrics carrying the whole slide | Numbers need context to mean anything |
| `data-table` | Financial reporting, period comparisons | Under 3 rows — write a sentence |
| `image-grid` | Popup photos, product shots, venue | Images are filler |
| `timeline` | Schedules, phased rollouts, 3–5 stages | Steps aren't sequential |
| `quote` | A customer or executive line worth a slide | You're padding |
| `closing` | Dark. The ask, the owner, the date. Once. | — |

Do not invent a twelfth layout. When nothing fits, the content almost always needs splitting.

### Closing
End on the ask, never on 感謝します. A closing slide without an owner and a date is where decisions go to die.

```html
<section class="slide" data-layout="closing">
  <div class="panel">
    <div class="pill green">APPROVAL REQUEST</div>
    <h1>文具SKUの<span class="grad cool">初動物量 1.5倍案</span>、<br>8月31日までにご承認いただきたい</h1>
    <p class="lead">担当: IPX 事業企画 · 次回発注着手は9月上旬</p>
    <div class="pageno"></div>
  </div>
</section>
```
