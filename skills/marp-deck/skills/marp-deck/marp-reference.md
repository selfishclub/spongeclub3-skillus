# Marp Markdown Reference

Comprehensive reference for Marp presentation syntax. Loaded by the `marp-deck` skill when needed.

## Frontmatter

Every Marp deck starts with YAML frontmatter:

```yaml
---
marp: true
theme: default
paginate: true
style: |
  /* Custom CSS goes here */
---
```

### Global Directives (frontmatter)

| Directive | Description |
|-----------|-------------|
| `marp: true` | **Required.** Enables Marp processing |
| `theme: default` | Built-in themes: `default`, `gaia`, `uncover` |
| `paginate: true` | Show slide numbers |
| `header: "text"` | Header on every slide |
| `footer: "text"` | Footer on every slide |
| `style: \|` | Custom CSS block (multi-line) |
| `math: mathjax` | Enable math rendering |

## Slide Separator

Use `---` on its own line to separate slides:

```markdown
# Slide 1

Content here

---

# Slide 2

More content
```

## Local Directives

Per-slide directives override globals. Place in HTML comments:

```markdown
<!-- _class: dark -->
<!-- _paginate: false -->
<!-- _header: "" -->
<!-- _backgroundColor: #1a1f36 -->
<!-- _color: #ffffff -->
```

Underscore prefix (`_`) = applies to current slide only.
Without underscore = applies to current slide and all subsequent slides.

## CSS Classes

Define classes in the `style` frontmatter, apply with `_class`:

```yaml
style: |
  section.dark {
    background: #1a1f36;
    color: #cdd6e4;
  }
  section.dark h1, section.dark h2 {
    color: #ffffff;
  }
  section.dark strong {
    color: #00c9a7;
  }
  section.dark a {
    color: #00c9a7;
  }

  section.accent {
    background: #1a1f36;
    color: #cdd6e4;
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
```

Apply to a slide:
```markdown
<!-- _class: dark -->
# Dark Slide Title
```

## Scoped Styles

Override styles for a single slide using `<style scoped>`:

```markdown
<style scoped>
table { font-size: 20px; }
th { background: #1a1f36; color: #fff; }
</style>

| Column 1 | Column 2 |
|----------|----------|
| data     | data     |
```

## Background Images

### Full background
```markdown
![bg](image.png)           <!-- stretch to fill -->
![bg contain](image.png)   <!-- fit within slide, maintain ratio -->
![bg cover](image.png)     <!-- fill slide, may crop -->
![bg 80%](image.png)       <!-- scale to 80% -->
```

### Split layouts (most useful for presentations)
```markdown
![bg right](image.png)            <!-- 50/50 split, image on right -->
![bg right:40%](image.png)        <!-- 60/40 split -->
![bg right:75% contain](image.png) <!-- 25/75 split, image contained -->
![bg left:40%](image.png)         <!-- image on left, 40% width -->
```

### Multiple backgrounds
```markdown
![bg](image1.png)
![bg](image2.png)
<!-- Creates a side-by-side background -->
```

### Background color
```markdown
![bg](#1a1f36)
```

## Inline Images

```markdown
![w:300](image.png)        <!-- width 300px -->
![h:200](image.png)        <!-- height 200px -->
![w:300 h:200](image.png)  <!-- both dimensions -->
```

**Note:** Inline images at slide resolution (1280x720) can render small. For large images, prefer background image directives.

## Text Formatting

Standard markdown plus:

```markdown
**bold**
*italic*
***bold italic***
~~strikethrough~~
`inline code`
[link text](url)
> blockquote
```

## Tables

Standard markdown tables. Control sizing with scoped styles:

```markdown
<style scoped>table { font-size: 22px; }</style>

| Feature | Benefit |
|---------|---------|
| Fast    | Saves time |
```

## Code Blocks

````markdown
```javascript
function hello() {
  console.log('world');
}
```
````

Control code font size:
```markdown
<style scoped>pre { font-size: 18px; }</style>
```

## Speaker Notes

Place in HTML comments:

```markdown
<!--
SPEAKER NOTES:
"This is what I'll say during this slide."
-->
```

Speaker notes are visible in presenter mode (`--preview` flag) but not in exported images/PDFs.

## HTML in Slides

Marp supports HTML, but **markdown inside HTML tags is not processed**. This means:

```markdown
<!-- BAD: markdown inside HTML won't render -->
<div style="display: grid;">
  **This bold won't work**
</div>

<!-- GOOD: use Marp's native layout features instead -->
![bg right:50%](image.png)
**This bold works** because it's in markdown context
```

For two-column layouts, prefer `![bg right:XX%]` or `![bg left:XX%]` over HTML grids.

## Slide Sizing

Default: 16:9 (1280x720). Can be changed:

```yaml
---
size: 4:3
---
```

Or custom:
```yaml
---
size: 1920x1080
---
```

## Theming Recipe: Dark/Light Sandwich

A professional pattern for executive presentations:

1. **Slide 1** (dark): Title slide with branding
2. **Slides 2-N-1** (light): Content slides — tables, images, text
3. **Transition slide** (dark/accent): Dramatic pause or pivot point
4. **More content** (light): Supporting material
5. **Final slide** (dark): Call to action, links, closing

CSS classes needed:

```css
/* Light slides: default Marp theme handles these */

/* Dark slides */
section.dark {
  background: #1a1f36;
  color: #cdd6e4;
}
section.dark h1, section.dark h2, section.dark h3 {
  color: #ffffff;
}
section.dark strong {
  color: #00c9a7;  /* teal accent */
}
section.dark a {
  color: #00c9a7;
}
section.dark::after {  /* page number */
  color: #4a5270;
}

/* Centered accent slides (for dramatic transitions) */
section.accent {
  background: #1a1f36;
  color: #cdd6e4;
  text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
section.accent h2 {
  color: #ffffff;
  font-size: 40px;
}
section.accent h3 {
  color: #00c9a7;
  font-size: 32px;
}
```

## CLI Commands

```bash
# Export as individual PNG images (for visual QA)
npx @marp-team/marp-cli deck.md --images png --allow-local-files -o slides/slide.png

# Export as single PDF
npx @marp-team/marp-cli deck.md --allow-local-files -o deck.pdf

# Export as PowerPoint
npx @marp-team/marp-cli deck.md --allow-local-files -o deck.pptx

# Export as HTML (self-contained)
npx @marp-team/marp-cli deck.md --allow-local-files -o deck.html

# Live preview with hot reload
npx @marp-team/marp-cli deck.md --preview

# Watch mode (auto-export on save)
npx @marp-team/marp-cli deck.md --images png -w
```

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Markdown not rendering inside HTML tags | Use Marp's native features (`![bg right]`) instead of HTML grids |
| Retina screenshots appear tiny | Crop to relevant area, or use `![bg right:75% contain]` for max size |
| Text overflows slide bottom | Reduce content or split into two slides — Marp doesn't scroll |
| Links invisible on dark backgrounds | Add explicit `a` color rule in dark class CSS |
| Table too small to read | Use `<style scoped>table { font-size: 22px; }</style>` |
| Code block text tiny | Use `<style scoped>pre { font-size: 18px; }</style>` |
| Page numbers hard to see on dark | Style `section.dark::after { color: #4a5270; }` |
