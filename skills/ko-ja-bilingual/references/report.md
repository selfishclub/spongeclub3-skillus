# Report documents

The second output format. Where the deck is a fixed 1920×1080 page you advance in front of people, a report is a scrolling document someone opens on their own and reads at their own pace. Almost every rule flips between the two, so decide which one you're making before writing anything.

The design system comes from a document this team already uses — a bilingual Instagram diagnostic report — with the accent swapped to LINE green. Template: `assets/report-base.html`.

## Which format

| | Deck (`deck-base.html`) | Report (`report-base.html`) |
|---|---|---|
| Read where | Projected, you narrate it | A link, read alone |
| Density | One claim per slide | Full paragraphs, long tables |
| Language | **Two files**, no toggle | **One file with a toggle** |
| Nuance | Cut it — you say it out loud | Keep it — nobody's there to explain |
| Palette | Slate + gradient headlines | Warm paper + one flat accent |

The language rule reverses because the failure mode reverses. On a projector a toggle is only a way to show the wrong language to a room. In a document the reader picks their own, and shipping two files means half your readers get the wrong link.

Pick report when: the material needs caveats to be understood, there are more numbers than a slide can hold, the audience reads asynchronously, or someone will come back to it weeks later as a reference. Pick deck when there's a meeting.

## Bilingual mechanics

Every piece of text is a paired span inside its parent:

```html
<p class="lede"><span class="x-ja">日本語の本文。</span><span class="x-ko">한국어 본문.</span></p>
```

`data-lang` on `<html>` hides one side. Two rules keep this from rotting:

1. **Never leave a span unpaired.** A `.x-ja` with no `.x-ko` sibling vanishes entirely when the reader switches — silent content loss, the worst kind of bug because nothing looks broken. Before delivering, count them:
   ```js
   [...document.querySelectorAll('.x-ja')].filter(e=>!e.parentElement.querySelector('.x-ko')).length  // must be 0
   ```
2. **Write each language, don't translate one into the other.** A Japanese sentence that was punchy in Korean and arrived as a 40-character clause has lost what made it work. See `language.md` for units, dates, and the tone difference on bad news.

Numbers, table values, and code stay outside the spans — they're the same in both languages, and duplicating them means fixing every correction twice.

## Components

All defined in `report-base.html`. Nothing else is styled.

- **`.masthead`** — `.eyebrow` (mono, English kicker) → `h1` → `.lede` (3–5 lines) → `.meta` (mono byline). The lede should let someone stop reading there and still know what you found.
- **`.keyfig`** — 3–4 headline numbers in mono. `.n.down` colours a number as bad news. Past four, each one weakens the others.
- **`section`** + **`.sec-head`** — a numbered `.sec-no` badge and an `h2`. Section headings are conclusions, not labels: 「未達は文具のみ、しかも需要側の問題ではない」, not 「カテゴリ別実績」.
- **`.tw` > `table`** — wrap every table in `.tw` so it scrolls horizontally instead of breaking the layout. `.num` for figures (mono, tabular, right-aligned), `tr.hi` to spotlight one row, `.t-good` / `.t-crit` on values.
- **`.thesis`** — the accent-tinted box holding the one sentence you want remembered. Once or twice per document; a third makes all three ordinary.
- **`.callout`** — three flavours carrying three different jobs: default (critical) for a risk or compliance problem, `.warn` for *this number does not mean what it looks like*, `.good` for an asset already working that shouldn't be discarded. The `.warn` variant earns its place more often than people expect — most misreadings come from a real number read the wrong way.
- **`ul.ticks`** — short evidence lists.
- **`footer`** — Methodology & Limits. **Not optional.** State what you measured, and state what you couldn't get. A report that lists its own blind spots is trusted; one that reads as complete gets audited by the first person who spots a gap.

Prose lives in `<p class="prose">`; `<em>` is a highlight, not italics.


### Charts — `.chart`
Two primitives, both self-contained. They exist because a popup or quarterly report usually needs exactly two things: a plan-versus-actual comparison, and a curve over days.

**Bars** are pure CSS — no script, nothing to break. Put the percentage in `--v` (scaled so the largest bar is 100%) and the real number in `.val`; the bar shows proportion, the text carries the value, and a reader who needs the actual figure never has to estimate it from a length.

```html
<figure class="chart">
  <figcaption><span class="x-ja">単位・出所</span><span class="x-ko">단위·출처</span></figcaption>
  <div class="legend"><span class="s1">計画</span><span class="s2">実績</span></div>
  <div class="bars">
    <div class="row"><span class="lbl">1st</span>
      <div class="group">
        <div class="track"><span class="b s1" style="--v:52%"></span><span class="val">3,480</span></div>
        <div class="track"><span class="b s2" style="--v:100%"></span><span class="val">6,880</span></div>
      </div></div>
  </div>
</figure>
```

**Line** takes raw numbers and draws itself — you never hand-compute coordinates:

```html
<div class="linechart" data-values="18,31,44,39,28,22,25,19"
     data-labels="D1,D2,D3,D4,D5,D6,D7,D8" data-label="daily curve"></div>
```
The peak point is filled automatically, which is usually the thing being discussed in a daily curve.

Series colours are `--s1`…`--s4`, defined in all three theme blocks. Use `s1` for the series the slide is about and `s2` for its comparison; reaching for `s3`/`s4` usually means the chart is carrying more than one idea.

Keep the y-axis honest: bars start at zero because `--v` is a proportion of the maximum. If you ever need a truncated axis, say so in the `figcaption` — a bar chart that silently starts at 80% overstates every difference on it.

Numbers stay outside the `.x-ja`/`.x-ko` spans; only labels and captions get translated.

## Tokens

Warm neutrals, one accent. `--brand` / `--accent` are LINE green (`#06C755`, `#0A7A3A`); `--paper` `--surface` `--sunken` `--rule` carry the paper feel; `--critical` `--ochre` `--good` are the semantic trio, each with a soft `-2` background.

Colours are defined three times — bare `:root`, then `@media (prefers-color-scheme:dark)` guarded with `:root:not([data-theme="light"])`, then `:root[data-theme="dark"]`. Keep all three in sync when changing a token, or the document will look right in one theme and broken in the other.

## Before delivering

1. Orphan span count is 0 (the one-liner above).
2. Both languages read as originals — check the h1 and the thesis especially.
3. Every table sits inside `.tw`.
4. The footer states real limits, not boilerplate.
5. If the numbers are placeholders or test data, say so **in the document**, not just in chat — a sample that circulates without that line becomes a real report by accident.
