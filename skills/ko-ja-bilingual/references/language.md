# Korean / Japanese

The deck's `<html lang>` attribute drives typography — set it to `ko` or `ja` and the token overrides in the template handle the rest. What follows is what the CSS cannot do for you.

## Typography

| | ko | ja |
|---|---|---|
| Body font | Noto Sans KR | Noto Sans JP |
| Line height | 1.6 | 1.75 — kana/kanji mixed text needs more air |
| Letter spacing | −0.01em | +0.01em |
| Line breaking | Break at 어절 boundaries | Never split a 熟語 across lines |

Use `<br>` deliberately in headlines in both languages. Auto-wrapping a two-line action title usually breaks it in the wrong place, and a headline is the one place that's worth controlling by hand.

## Numbers and units

| | ko | ja |
|---|---|---|
| Currency | 원 / 엔 (¥) | 円 |
| Large units | 억 원, 만 명 | 億円, 百万円, 万人 |
| Percent point | %p | ポイント / pt |
| Date | 2026.08.24 | 2026年8月24日 or 26/8/24 |
| Fiscal | 2026년 2분기 | 2026年度 第2四半期 / FY26 Q2 |

Japanese financial reporting leans on **百万円** where Korean would say 억 원 — converting the number but keeping the Korean unit is the classic tell of a machine-translated deck. Always state the unit once, in the table caption or axis label, rather than repeating it in every cell.

## Tone

Korean report decks read as **명사형 종결** — "객단가 +23%, 세트 구성이 견인". Not 문장형, not 존댓말. Japanese decks are the same shape but more likely to use だ・である体 in body text and to soften recommendations: 「〜が望ましい」「〜を検討したい」rather than a flat imperative.

One thing that does not translate: a Korean action title can be blunt about a miss ("문구 역성장, 재고 배분 실패"). The Japanese equivalent lands harsher than intended in a 本社 setting — state the same fact but attribute it to the cause rather than the failure（「文具は在庫配分が想定とずれ、前年割れ」）. This is not softening the message; it is keeping the reader focused on the fix instead of on who is at fault.

## When the user wants both

Write the outline once, then produce two files. Translate the **claims**, not the sentences — an action title that was punchy in Korean and became a 40-character Japanese clause has lost the thing that made it work. Rewrite it in Japanese to be punchy in Japanese.

Filenames: `2026Q2_review_ko.html`, `2026Q2_review_ja.html`.
