#!/usr/bin/env python3
"""Verify that every <img> in an HTML deck stays inside its box, its slide, and actually loads.

Usage:
    python3 check_images.py deck.html [--slide "section.slide"] [--chrome "/path/to/Chrome"]

Exit 0 = every image and every slide passes. Exit 1 = at least one finding (listed).

How it works: the deck is copied to a temp file with a measuring script appended, then rendered in
headless Chrome (--dump-dom after a virtual-time budget, so fonts and data-URI images have decoded).
Each slide is forced visible one at a time (decks hide inactive slides with display:none), and for
every <img> we measure the rendered rect against:
  1. its box   = nearest ancestor with overflow:hidden, or one carrying a class named in --box
  2. its slide = the --slide ancestor
plus: loaded (naturalWidth > 0), not collapsed (< 8px), not loading="lazy" (hidden slides never
lazy-load, so the image is missing from print/PDF), and the slide's own scroll overflow.
"""
import argparse, json, os, re, subprocess, sys, tempfile, time

DEFAULT_CHROME = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Google Chrome 2.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
]

MEASURE = r"""
<script>
(function(){
  const SLIDE=%(slide)s, BOX=%(box)s;
  function run(){
    const out={slides:[],lazy:0};
    const slides=[...document.querySelectorAll(SLIDE)];
    const targets = slides.length ? slides : [document.body];
    for (const [k,s] of targets.entries()){
      const prevDisp=s.style.display, prevCls=s.className;
      const wasHidden = getComputedStyle(s).display==='none';
      if (wasHidden){ s.style.display='block'; }
      const sr=s.getBoundingClientRect();
      const findings=[];
      // scroll overflow inside clipped containers (text or images pushed past the edge)
      for (const el of [s,...s.querySelectorAll('*')]){
        const cs=getComputedStyle(el);
        if ((cs.overflowY==='hidden'||cs.overflow==='hidden') && el.scrollHeight>el.clientHeight+2 && el.clientHeight>40)
          findings.push('clipped overflow '+(el.scrollHeight-el.clientHeight)+'px in <'+el.tagName.toLowerCase()+(el.className?'.'+String(el.className).trim().split(/\s+/).join('.'):'')+'>');
      }
      for (const im of s.querySelectorAll('img')){
        const r=im.getBoundingClientRect();
        const tag='<img'+(im.alt?' alt="'+im.alt.slice(0,40)+'"':'')+(im.className?' .'+String(im.className).trim().split(/\s+/).join('.'):'')+'>';
        if (im.getAttribute('loading')==='lazy'){ findings.push(tag+' has loading="lazy" (hidden slides never load it; missing from PDF)'); out.lazy++; }
        if (!im.complete || im.naturalWidth===0){ findings.push(tag+' not loaded'); continue; }
        if (r.width<8||r.height<8){ findings.push(tag+' collapsed to '+Math.round(r.width)+'x'+Math.round(r.height)); continue; }
        // box = nearest overflow:hidden ancestor or a named box class
        let box=im.parentElement;
        while (box && box!==s){
          const cs=getComputedStyle(box);
          if (cs.overflow==='hidden'||cs.overflowY==='hidden'||cs.overflowX==='hidden') break;
          if (BOX && box.matches(BOX)) break;
          box=box.parentElement;
        }
        if (!box||box===s) findings.push(tag+' has no clipping box (no overflow:hidden ancestor inside the slide)');
        const br=(box||s).getBoundingClientRect();
        const outBox = r.left<br.left-1||r.right>br.right+1||r.top<br.top-1||r.bottom>br.bottom+1;
        if (box && box!==s && outBox)
          findings.push(tag+' escapes its box: img '+Math.round(r.width)+'x'+Math.round(r.height)+' vs box '+Math.round(br.width)+'x'+Math.round(br.height)+
            ' (overflow '+Math.round(Math.max(0,r.bottom-br.bottom,br.top-r.top))+'px v / '+Math.round(Math.max(0,r.right-br.right,br.left-r.left))+'px h)');
        if (r.left<sr.left-1||r.right>sr.right+1||r.top<sr.top-1||r.bottom>sr.bottom+1)
          findings.push(tag+' escapes the slide');
      }
      out.slides.push({n:k+1,imgs:s.querySelectorAll('img').length,findings});
      if (wasHidden){ s.style.display=prevDisp; }
    }
    const pre=document.createElement('pre'); pre.id='__imgcheck__'; pre.textContent=JSON.stringify(out); document.body.appendChild(pre);
  }
  const go=()=>{ const ready=(document.fonts&&document.fonts.ready)||Promise.resolve(); ready.then(()=>setTimeout(run,300)); };
  if (document.readyState==='complete') go(); else addEventListener('load',go);
})();
</script>
"""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html")
    ap.add_argument("--slide", default="section.slide, section, .slide", help="CSS selector for one slide/page")
    ap.add_argument("--box", default=".vis, .fig, .thumb, figure", help="class selectors that count as an image box even without overflow:hidden")
    ap.add_argument("--chrome", default=None)
    ap.add_argument("--width", type=int, default=1920)
    ap.add_argument("--height", type=int, default=1080)
    a = ap.parse_args()

    chrome = a.chrome or next((c for c in DEFAULT_CHROME if os.path.exists(c)), None)
    if not chrome:
        sys.exit("no Chromium-based browser found; pass --chrome /path/to/binary")

    src = open(a.html, encoding="utf-8").read()
    inject = MEASURE % {"slide": json.dumps(a.slide), "box": json.dumps(a.box)}
    patched = src.replace("</body>", inject + "</body>") if "</body>" in src else src + inject
    tmpdir = tempfile.mkdtemp(prefix="imgcheck_")
    tmp = os.path.join(tmpdir, os.path.basename(a.html))
    open(tmp, "w", encoding="utf-8").write(patched)

    cmd = [chrome, "--headless", "--disable-gpu", "--no-sandbox", "--hide-scrollbars", "--no-first-run",
           "--disable-background-networking", "--disable-component-update", "--disable-sync",
           f"--window-size={a.width},{a.height}", "--virtual-time-budget=8000",
           "--user-data-dir=" + os.path.join(tmpdir, "profile"), "--dump-dom", "file://" + tmp]
    # Chrome may keep running after the dump (it spawns the Google Updater on macOS), so never wait
    # for exit: read stdout until the document is complete, then kill it.
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    dom, deadline = "", time.time() + 120
    try:
        while time.time() < deadline:
            line = proc.stdout.readline()
            if not line:
                if proc.poll() is not None: break
                continue
            dom += line
            if "</html>" in line: break
    finally:
        try: proc.kill()
        except Exception: pass
    m = re.search(r'<pre id="__imgcheck__">(.*?)</pre>', dom, re.S)
    if not m:
        sys.exit("measure script did not run (no __imgcheck__ marker). Is the file valid HTML with a </body>?")
    res = json.loads(m.group(1).replace("&quot;", '"').replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&"))

    bad = 0
    for s in res["slides"]:
        mark = "ok " if not s["findings"] else "FAIL"
        print(f"[{mark}] slide {s['n']:>2}  imgs={s['imgs']}")
        for f in s["findings"]:
            bad += 1
            print(f"        - {f}")
    total = sum(s["imgs"] for s in res["slides"])
    print(f"\n{len(res['slides'])} slides, {total} images, {bad} finding(s)")
    sys.exit(1 if bad else 0)

if __name__ == "__main__":
    main()
