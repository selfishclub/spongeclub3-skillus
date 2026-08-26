# Image Assets

## `claude-skills-install.gif` — Cowork install demo (TO RECORD)

The README references `.docs/images/claude-skills-install.gif` showing the
Claude Cowork install flow:

1. Open Claude desktop app
2. Click **Customize** (bottom-left)
3. Click **Browse plugins**
4. Type `borghei/Claude-Skills`
5. Click install
6. Show 326 skills now available

### Recording recipe

**On macOS:**

```bash
# 1. Open Claude desktop app
# 2. Position window to a clean state
# 3. Start screen recording on the region (Cmd+Shift+5 → "Record selected portion")
# 4. Perform the install flow
# 5. Stop recording → save .mov
# 6. Convert to optimized GIF:

ffmpeg -i recording.mov \
  -vf "fps=15,scale=900:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=128[p];[s1][p]paletteuse=dither=bayer:bayer_scale=5" \
  -loop 0 \
  .docs/images/claude-skills-install.gif
```

Target: < 5 MB, < 15 seconds, 900px wide, 15 fps.

**Alternative — use a dedicated tool:**
- [Kap](https://getkap.co/) (free, macOS)
- [LICEcap](https://www.cockos.com/licecap/) (free, macOS/Windows)
- [GIPHY Capture](https://giphy.com/apps/giphycapture) (free, macOS)

### Once recorded

Drop the GIF at `.docs/images/claude-skills-install.gif`. The README link will resolve automatically.
