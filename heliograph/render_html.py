"""Static dark dashboard. One self-contained file, no external assets.

The "Signal" direction: the verdict is the page. A status-colored glow and
an oversized count lead; findings sit in plain ledger rows (hairline rules,
a small colored dot + plain-weight label - never a tinted callout box);
the metrics are large bare tiles with accent sparklines; tables carry the
full detail. SOL price rides in the hero as a ticker - the one number a
regular user came for, above the fold. Craft rules: hierarchy from
weight+size+leading, negative tracking on display sizes, tabular figures
only in columns, in-view reveals as interruptible transitions on a strong
ease-out (55ms stagger), reduced-motion and reduced-transparency fallbacks,
hover effects only on hover-capable pointers. Radius rule: surfaces 14px,
interactive chips full-pill.
"""

import html
import json
import math
from datetime import datetime, timezone

from .report import usd

# dark tokens from the reference palette
CSS = """
:root {
  --page: #0d0d0d; --surface: #1a1a19; --ink: #ffffff; --ink-2: #c3c2b7;
  --muted: #898781; --grid: #2c2c2a; --baseline: #383835;
  --border: rgba(255,255,255,0.08); --edge: rgba(255,255,255,0.14);
  --accent: #3987e5;
  --good: #0ca30c; --warning: #fab219; --serious: #ec835a; --critical: #d03b3b;
  --ease: cubic-bezier(0.23, 1, 0.32, 1);
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body { background: var(--page); color: var(--ink-2);
  font: 15px/1.55 system-ui, -apple-system, "Segoe UI", sans-serif;
  -webkit-font-smoothing: antialiased; }
.wrap { max-width: 1100px; margin: 0 auto; padding: 0 28px 72px; }

.bar { display: flex; justify-content: space-between; align-items: baseline;
  flex-wrap: wrap; gap: 10px; padding: 22px 0; }
.brand { color: var(--ink); font-size: 17px; font-weight: 700; letter-spacing: -.01em;
  display: inline-flex; align-items: center; gap: 9px; }
.brand svg { color: var(--accent); }
.meta { color: var(--muted); font-size: 13px; }

.hero { position: relative; padding: 64px 0 26px; }
.glow { position: absolute; top: -60px; left: -120px; width: 520px; height: 520px;
  border-radius: 50%; pointer-events: none; filter: blur(2px);
  background: radial-gradient(circle, var(--glowc) 0%, transparent 62%); }
.hero-in { animation: focusin 320ms var(--ease) backwards; }
.hero .row { display: flex; align-items: baseline; gap: 22px; flex-wrap: wrap; position: relative; }
.hero .n { font-size: clamp(110px, 17vw, 170px); font-weight: 700;
  letter-spacing: -.05em; line-height: .9; }
.ticker { position: absolute; right: 0; top: 140px; text-align: right; }
.ticker .l { color: var(--muted); font-size: 13px; }
.ticker .p { color: var(--ink); font-size: 46px; font-weight: 700;
  letter-spacing: -.03em; line-height: 1.15; }
.ticker .win { color: var(--muted); font-size: 13px; font-weight: 400; margin-left: 6px; }
.badge { font-size: 12px; font-weight: 700; letter-spacing: .14em; }
.badge::before { content: ""; display: inline-block; width: 8px; height: 8px;
  border-radius: 50%; margin-right: 7px; background: currentColor; }
.verdict { position: relative; font-size: 19px; max-width: 36em; margin-top: 20px; }
.verdict b { color: var(--ink); font-weight: 600; }

.finding { border-top: 1px solid var(--grid); padding: 18px 0; }
.finding:last-of-type { border-bottom: 1px solid var(--grid); }
.sev { font-size: 11px; font-weight: 650; letter-spacing: .1em; color: var(--muted); }
.sev::before { content: ""; display: inline-block; width: 7px; height: 7px;
  border-radius: 50%; margin-right: 7px; background: var(--sc, var(--warning)); }
.headline { color: var(--ink); font-weight: 550; font-size: 17px; margin-top: 6px; }
.detail { color: var(--muted); font-size: 13px; margin-top: 6px;
  font-variant-numeric: tabular-nums; }

h2 { display: flex; align-items: center; flex-wrap: wrap; gap: 10px; color: var(--ink-2);
  font-size: 12px; font-weight: 650; letter-spacing: .1em; text-transform: uppercase;
  margin: 56px 0 22px; }
h2::before { content: ""; width: 18px; height: 2px; background: var(--accent); }
.secnote { color: var(--muted); font-size: 13px; margin: -12px 0 18px; }

.tiles { display: grid; gap: 30px 34px;
  grid-template-columns: repeat(auto-fill, minmax(min(100%, 280px), 1fr)); }
.tile .l { color: var(--muted); font-size: 13px; }
.tile .v { color: var(--ink); font-size: 42px; font-weight: 700; letter-spacing: -.03em;
  line-height: 1.1; margin: 4px 0 8px; }
.delta { font-size: 14px; margin-left: 9px; font-weight: 600; }
.d-good { color: var(--good); } .d-bad { color: var(--critical); }
.spark { display: block; width: 100%; }

.card { background: linear-gradient(180deg, rgba(255,255,255,.035), rgba(255,255,255,.015));
  border: 1px solid var(--border); border-top-color: var(--edge); border-radius: 14px;
  overflow-x: auto; }
.switch { display: flex; gap: 6px; margin-left: auto; }
.sw { border: 1px solid var(--border); background: none; color: var(--muted);
  font: inherit; font-size: 12px; letter-spacing: .02em; padding: 5px 13px;
  border-radius: 999px; cursor: pointer;
  transition: color 140ms var(--ease), border-color 140ms var(--ease), transform 140ms var(--ease); }
.sw:active { transform: scale(.97); }
.sw[aria-pressed="true"] { color: var(--ink); border-color: var(--edge);
  background: rgba(255,255,255,.05); }
.chartcard { padding: 20px 12px 10px; }
.cpane { transition: opacity 200ms var(--ease), transform 200ms var(--ease); }
@starting-style { .cpane { opacity: 0; transform: translateY(6px); } }
.bigchart { display: block; width: 100%; height: auto;
  min-width: 840px; }  /* on narrow screens the card scrolls; ticks stay legible */
.bigchart .tick { fill: var(--muted); font-size: 12px; font-variant-numeric: tabular-nums; }
.bigchart .endlabel { fill: var(--ink); font-size: 13px; font-weight: 600;
  font-variant-numeric: tabular-nums; }
.nochart { color: var(--muted); font-size: 13px; padding: 26px 18px; }
.duo { display: grid; gap: 14px;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 320px), 1fr)); }
table { width: 100%; border-collapse: collapse; }
th, td { text-align: left; padding: 11px 18px; font-size: 14px; }
th { color: var(--muted); font-size: 11.5px; font-weight: 650; letter-spacing: .08em;
  text-transform: uppercase; }
td { color: var(--ink-2); border-top: 1px solid var(--grid); font-variant-numeric: tabular-nums; }
td:first-child { font-variant-numeric: normal; }
.num, th.num { text-align: right; }
.mono { font-family: ui-monospace, "SF Mono", monospace; font-size: 12.5px; }

footer { margin-top: 56px; color: var(--muted); font-size: 13px;
  border-top: 1px solid var(--grid); padding-top: 18px;
  display: flex; gap: 18px; flex-wrap: wrap; }
footer a { color: var(--ink-2); text-decoration: none; transition: color 140ms var(--ease); }
footer .thesis { flex: 1 1 100%; }

#tip { position: fixed; pointer-events: none; z-index: 9; display: none; opacity: 0;
  background: color-mix(in srgb, var(--page) 88%, transparent);
  backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);
  border: 1px solid var(--edge); border-radius: 7px; padding: 5px 9px;
  font-size: 12px; color: var(--ink); font-variant-numeric: tabular-nums;
  transition: opacity 100ms var(--ease); }

@media (hover: hover) and (pointer: fine) {
  footer a:hover { color: var(--accent); }
  .sw:hover { color: var(--ink-2); border-color: var(--edge); }
}
@media (pointer: coarse) {
  .sw { padding: 9px 15px; }
}

/* in-view reveal: a head script stamps .pre on <html> before paint (so no-JS
   stays visible), the IntersectionObserver in the footer script adds .in with
   a staggered delay. Transitions, not keyframes: interruptible by design. */
.rise { transition: opacity 480ms var(--ease), transform 480ms var(--ease); }
.pre .rise { opacity: 0; transform: translateY(10px); }
.pre .rise.in { opacity: 1; transform: none; }

@keyframes focusin { from { opacity: 0; filter: blur(6px); transform: scale(.985); } }
@keyframes fade { from { opacity: 0; } }
@media (prefers-reduced-motion: reduce) {
  .hero-in { animation: fade 180ms ease backwards; }
  .pre .rise { transform: none; transition: opacity 200ms ease; }
  .cpane { transition: opacity 160ms ease; }
  @starting-style { .cpane { transform: none; } }
}
@media (prefers-reduced-transparency: reduce) {
  #tip { backdrop-filter: none; -webkit-backdrop-filter: none; background: var(--page); }
}
@media print {
  .pre .rise { opacity: 1; transform: none; }
}

@media (max-width: 640px) {
  .wrap { padding: 0 20px 56px; }
  .hero { padding: 40px 0 20px; }
  .ticker { position: static; text-align: left; margin-top: 22px; }
  .ticker .p { font-size: 38px; }
  h2 { margin: 44px 0 18px; }
  th, td { padding: 10px 12px; }
  .tiles { gap: 26px; }
}
"""

JS = """
const tip = document.getElementById('tip');
const fmtTime = t => new Date(t * 1000).toISOString().slice(5, 16).replace('T', ' ') + ' UTC';
function fmtVal(v, kind) {
  if (kind === 'usd') {
    for (const [d, s] of [[1e12,'T'],[1e9,'B'],[1e6,'M'],[1e3,'K']])
      if (Math.abs(v) >= d) return '$' + (v / d).toLocaleString('en-US', {maximumFractionDigits: 2}) + s;
    return '$' + Math.round(v).toLocaleString('en-US');
  }
  return v.toLocaleString('en-US', {maximumFractionDigits: 1});
}
function hideCrosshairs() {
  document.querySelectorAll('.bigchart .ch, .bigchart .chd')
    .forEach(el => el.setAttribute('visibility', 'hidden'));
}
function showTip(e, text) {
  tip.textContent = text;
  tip.style.left = (e.clientX + 12) + 'px';
  tip.style.top = (e.clientY - 30) + 'px';
  tip.style.display = 'block';
  requestAnimationFrame(() => tip.style.opacity = '1');
}
document.addEventListener('mousemove', e => {
  const big = e.target.closest ? e.target.closest('.bigchart') : null;
  if (big && big.dataset.pts) {
    const pts = JSON.parse(big.dataset.pts);  // [t, v, x, y] in viewBox units
    const r = big.getBoundingClientRect();
    const mx = (e.clientX - r.left) / (r.width / big.viewBox.baseVal.width);
    let best = pts[0];
    for (const p of pts) if (Math.abs(p[2] - mx) < Math.abs(best[2] - mx)) best = p;
    const ch = big.querySelector('.ch'), chd = big.querySelector('.chd');
    ch.setAttribute('x1', best[2]); ch.setAttribute('x2', best[2]);
    ch.setAttribute('visibility', 'visible');
    chd.setAttribute('cx', best[2]); chd.setAttribute('cy', best[3]);
    chd.setAttribute('visibility', 'visible');
    showTip(e, fmtVal(best[1], big.dataset.kind) + ' · ' + fmtTime(best[0]));
    return;
  }
  hideCrosshairs();
  const svg = e.target.closest ? e.target.closest('.spark') : null;
  if (!svg || !svg.dataset.points) { tip.style.opacity = '0'; tip.style.display = 'none'; return; }
  const pts = JSON.parse(svg.dataset.points);
  const r = svg.getBoundingClientRect();
  const i = Math.min(pts.length - 1, Math.max(0,
    Math.round((e.clientX - r.left) / r.width * (pts.length - 1))));
  showTip(e, pts[i][1].toLocaleString(undefined, {maximumFractionDigits: 1}) +
    ' · ' + fmtTime(pts[i][0]));
});
document.querySelectorAll('.sw').forEach(b => b.addEventListener('click', () => {
  document.querySelectorAll('.sw').forEach(x =>
    x.setAttribute('aria-pressed', x === b ? 'true' : 'false'));
  document.querySelectorAll('.cpane').forEach((p, i) =>
    p.hidden = (String(i) !== b.dataset.c));
  hideCrosshairs();
}));
if (window.IntersectionObserver) {
  const io = new IntersectionObserver(entries => {
    let i = 0;
    for (const e of entries) {
      if (!e.isIntersecting) continue;
      const el = e.target;
      el.style.transitionDelay = Math.min(i++ * 55, 330) + 'ms';
      el.classList.add('in');
      el.addEventListener('transitionend', () => { el.style.transitionDelay = ''; }, {once: true});
      io.unobserve(el);
    }
  }, {rootMargin: '0px 0px -8% 0px'});
  document.querySelectorAll('.rise').forEach(el => io.observe(el));
} else {
  document.querySelectorAll('.rise').forEach(el => el.classList.add('in'));
}
"""

GLYPH = (
    '<svg width="16" height="16" viewBox="0 0 15 15" fill="none" aria-hidden="true">'
    '<circle cx="7.5" cy="7.5" r="3" fill="currentColor"/>'
    '<g stroke="currentColor" stroke-width="1.2" stroke-linecap="round">'
    '<line x1="7.5" y1="0.8" x2="7.5" y2="2.6"/><line x1="7.5" y1="12.4" x2="7.5" y2="14.2"/>'
    '<line x1="0.8" y1="7.5" x2="2.6" y2="7.5"/><line x1="12.4" y1="7.5" x2="14.2" y2="7.5"/>'
    "</g></svg>"
)

SEV_COLOR = {"crit": "critical", "warn": "warning", "info": "accent"}
SEV_WORD = {"crit": "CRITICAL", "warn": "WARNING", "info": "INFO"}


def compact(n, unit=""):
    if n is None:
        return "n/a"
    if unit == "$":
        return usd(n)
    for div, suffix in ((1e9, "B"), (1e6, "M"), (1e3, "K")):
        if abs(n) >= div:
            return f"{n / div:,.1f}{suffix}"
    return f"{n:,.10g}"


def sparkline(points, w=300, h=60):
    """12-point trend in the accent hue over a faint wash; current point
    carries an 8px dot with a 2px surface ring. Flat series sit midline."""
    pts = points[-12:]
    if len(pts) < 2:
        return f'<div class="spark" style="height:{h}px"></div>'
    vals = [v for _, v in pts]
    lo, hi = min(vals), max(vals)
    pad = 6
    if hi == lo:
        norm = lambda v: 0.5
    else:
        norm = lambda v: (v - lo) / (hi - lo)
    xy = [
        (pad + i * (w - 2 * pad) / (len(pts) - 1),
         pad + (h - 2 * pad) * (1 - norm(v)))
        for i, (_, v) in enumerate(pts)
    ]
    poly = " ".join(f"{x:.1f},{y:.1f}" for x, y in xy)
    area = f"{xy[0][0]:.1f},{h - 2} " + poly + f" {xy[-1][0]:.1f},{h - 2}"
    cx, cy = xy[-1]
    data = html.escape(json.dumps(pts), quote=True)
    return (
        f'<svg class="spark" height="{h}" viewBox="0 0 {w} {h}" '
        f'preserveAspectRatio="none" data-points="{data}">'
        f'<polygon points="{area}" fill="var(--accent)" opacity="0.10"/>'
        f'<polyline points="{poly}" fill="none" stroke="var(--accent)" stroke-width="2" '
        f'stroke-linejoin="round" stroke-linecap="round" vector-effect="non-scaling-stroke"/>'
        f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="4" fill="var(--accent)" '
        f'stroke="var(--surface)" stroke-width="2"/>'
        f"</svg>"
    )


def nice_ticks(lo, hi, target=4):
    """Round tick values covering [lo, hi]: steps of 1/2/5 × 10^k."""
    if hi == lo:
        lo, hi = lo - 1, hi + 1
    span = hi - lo
    step = 10 ** math.floor(math.log10(span / target))
    for m in (1, 2, 5, 10):
        if span / (step * m) <= target + 1:
            step *= m
            break
    ticks = []
    t = math.ceil(lo / step) * step
    while t <= hi + step * 1e-6:
        ticks.append(round(t, 10))
        t += step
    return ticks


def _fmt_value(v, kind):
    """Endpoint label: the current value, compact."""
    if kind == "usd":
        if abs(v) < 1000:
            return f"${v:,.10g}"
        return usd(v)
    return f"{v:,.10g}"


def _fmt_tick(v, step, kind):
    """Axis tick: precision follows the tick step so adjacent ticks differ."""
    def decimals(unit=1.0):
        ratio = step / unit
        return max(0, -math.floor(math.log10(ratio))) if ratio < 1 else 0
    if kind == "usd":
        for div, suf in ((1e12, "T"), (1e9, "B"), (1e6, "M"), (1e3, "K")):
            if abs(v) >= div:
                return f"${v / div:,.{decimals(div)}f}{suf}"
        return f"${v:,.{decimals()}f}"
    return f"{v:,.{decimals()}f}"


def bigchart(series, marks, kind="plain", w=1044, h=260):
    """Full-baseline line chart, time-scaled x. Single series in the accent
    hue (no legend; the switcher tab names it), hairline gridlines, clean
    y ticks, endpoint direct label, severity-colored marks where the
    anomaly engine spoke. Crosshair + tooltip ride on the JS layer."""
    if len(series) < 2:
        return '<div class="nochart">Not enough history yet; the chart grows with the baseline.</div>'
    pad_l, pad_r, pad_t, pad_b = 64, 76, 14, 26
    t0, t1 = series[0][0], series[-1][0]
    tspan = (t1 - t0) or 1
    vals = [v for _, v in series]
    lo, hi = min(vals), max(vals)
    vpad = (hi - lo) * 0.06 or abs(hi or 1) * 0.01
    lo, hi = lo - vpad, hi + vpad
    X = lambda t: pad_l + (t - t0) / tspan * (w - pad_l - pad_r)
    Y = lambda v: pad_t + (1 - (v - lo) / (hi - lo)) * (h - pad_t - pad_b)

    grid, ylabels = [], []
    ticks = nice_ticks(lo, hi)
    step = ticks[1] - ticks[0] if len(ticks) > 1 else 1
    for tv in ticks:
        y = Y(tv)
        grid.append(f'<line x1="{pad_l}" y1="{y:.1f}" x2="{w - pad_r}" y2="{y:.1f}" '
                    f'stroke="var(--grid)" stroke-width="1"/>')
        ylabels.append(f'<text x="{pad_l - 10}" y="{y + 4:.1f}" text-anchor="end" '
                       f'class="tick">{html.escape(_fmt_tick(tv, step, kind))}</text>')
    xlabels = []
    for frac in (0, 1 / 3, 2 / 3, 1):
        t = t0 + tspan * frac
        anchor = "start" if frac == 0 else ("end" if frac == 1 else "middle")
        label = datetime.fromtimestamp(t, tz=timezone.utc).strftime("%m-%d %H:%M")
        xlabels.append(f'<text x="{X(t):.1f}" y="{h - 8}" text-anchor="{anchor}" '
                       f'class="tick">{label}</text>')

    xy = [(X(t), Y(v)) for t, v in series]
    poly = " ".join(f"{x:.1f},{y:.1f}" for x, y in xy)
    base_y = h - pad_b
    area = f"{xy[0][0]:.1f},{base_y} " + poly + f" {xy[-1][0]:.1f},{base_y}"
    cx, cy = xy[-1]
    end_label = _fmt_value(series[-1][1], kind)

    mark_svg = "".join(
        f'<circle cx="{X(t):.1f}" cy="{Y(v):.1f}" r="4.5" '
        f'fill="var(--{SEV_COLOR[sev]})" stroke="var(--surface)" stroke-width="2"/>'
        for t, v, sev in marks
    )

    pts = [[t, v, round(X(t), 1), round(Y(v), 1)] for t, v in series]
    data = html.escape(json.dumps(pts), quote=True)
    return (
        f'<svg class="bigchart" viewBox="0 0 {w} {h}" data-pts="{data}" data-kind="{kind}">'
        + "".join(grid)
        + f'<line x1="{pad_l}" y1="{base_y}" x2="{w - pad_r}" y2="{base_y}" '
          f'stroke="var(--baseline)" stroke-width="1"/>'
        + "".join(ylabels) + "".join(xlabels)
        + f'<polygon points="{area}" fill="var(--accent)" opacity="0.08"/>'
        + f'<polyline points="{poly}" fill="none" stroke="var(--accent)" stroke-width="2" '
          f'stroke-linejoin="round" stroke-linecap="round"/>'
        + mark_svg
        + f'<line class="ch" y1="{pad_t}" y2="{base_y}" stroke="var(--baseline)" '
          f'stroke-width="1" visibility="hidden"/>'
        + f'<circle class="chd" r="4" fill="var(--accent)" stroke="var(--surface)" '
          f'stroke-width="2" visibility="hidden"/>'
        + f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="4" fill="var(--accent)" '
          f'stroke="var(--surface)" stroke-width="2"/>'
        + f'<text x="{cx + 10:.1f}" y="{cy + 4:.1f}" class="endlabel">{html.escape(end_label)}</text>'
        + "</svg>"
    )


def tile(label, value, series, up_good=True):
    delta = ""
    if len(series) >= 2 and series[-2][1]:
        prev, cur = series[-2][1], series[-1][1]
        pct = 100 * (cur - prev) / abs(prev)
        if abs(pct) >= 0.05:  # a flat delta is silence, not a ±0.0% chip
            good = (pct > 0) == up_good
            cls = "d-good" if good else "d-bad"
            delta = f'<span class="delta {cls}">{pct:+.1f}%</span>'
    return (
        f'<div class="tile rise"><div class="l">{html.escape(label)}</div>'
        f'<div class="v">{value}{delta}</div>'
        f"{sparkline(series) if series else ''}</div>"
    )


def table(rows, headers=("metric", "value"), num_cols=()):
    head = "".join(
        f'<th class="num">{html.escape(h)}</th>' if i in num_cols else f"<th>{html.escape(h)}</th>"
        for i, h in enumerate(headers)
    )
    body = "".join(
        "<tr>" + "".join(
            f'<td class="num">{c}</td>' if i in num_cols else f"<td>{c}</td>"
            for i, c in enumerate(row)
        ) + "</tr>"
        for row in rows
    )
    return f'<div class="card rise"><table><tr>{head}</tr>{body}</table></div>'


def build(sections, findings, baseline, status, ts, history, alert_marks=None):
    alert_marks = alert_marks or {}
    net = sections.get("network", {})
    val = sections.get("validators", {})
    eco = sections.get("economics", {})
    sup = sections.get("supply", {})
    eos = sections.get("ecosystem", {})
    when = datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    # the strip stays quiet in steady state; "baseline forming" is worth a slot
    baseline_note = ("" if baseline["status"] == "active"
                     else f' · baseline {html.escape(str(baseline["status"]))}')

    n = len(findings)
    worst = findings[0]["severity"] if findings else None
    hero_color = f"var(--{SEV_COLOR[worst]})" if worst else "var(--ink)"
    glow = (f"color-mix(in srgb, var(--{SEV_COLOR[worst]}) 13%, transparent)" if worst
            else "color-mix(in srgb, var(--accent) 11%, transparent)")
    badge = (f'<span class="badge" style="color:var(--{SEV_COLOR[worst]})">{SEV_WORD[worst]}</span>'
             if worst else '<span class="badge" style="color:var(--good)">ALL CLEAR</span>')
    verdict = ("Every watched metric is inside its normal band. <b>Nothing to do here.</b>"
               if n == 0 else
               "Read the findings below, then stop. The rest of the page is evidence.")

    price = eco.get("sol_price_usd")
    ticker = ""
    if price is not None:
        chg = eco.get("sol_24h_change_pct")
        chip = ""
        if chg is not None and abs(chg) >= 0.05:
            cls = "d-good" if chg > 0 else "d-bad"
            chip = f'<span class="delta {cls}">{chg:+.1f}%</span><span class="win">24h</span>'
        ticker = (f'<div class="ticker hero-in"><div class="l">SOL price</div>'
                  f'<div class="p">${price:,.2f}{chip}</div></div>')

    finding_html = "".join(
        f'<div class="finding rise" style="--sc:var(--{SEV_COLOR[f["severity"]]})">'
        f'<span class="sev">{SEV_WORD[f["severity"]]}</span>'
        f'<div class="headline">{html.escape(f["headline"])}</div>'
        f'<div class="detail">{html.escape(f["detail"])}</div></div>'
        for f in findings
    )

    # regular-user metrics lead the grid; operator metrics follow
    tiles = "".join([
        tile("SOL price", f"${compact(eco.get('sol_price_usd'))}",
             history.get("economics.sol_price_usd", [])),
        tile("Total value locked", usd(eco.get("tvl_usd")),
             history.get("economics.tvl_usd", [])),
        tile("DEX volume 24h", usd(eco.get("dex_volume_24h_usd")),
             history.get("economics.dex_volume_24h_usd", [])),
        tile("Transactions per second", compact(net.get("tps")), history.get("network.tps", [])),
        tile("Slot time", f"{net.get('slot_time_ms', 'n/a')} ms",
             history.get("network.slot_time_ms", []), up_good=False),
        tile("Delinquent stake", f"{val.get('delinquent_stake_pct', 'n/a')}%",
             history.get("validators.delinquent_stake_pct", []), up_good=False),
    ])

    network_rows = [
        ("Health", html.escape(str(net.get("health", "n/a")))),
        ("Slot", f"{net.get('slot', 0):,}"),
        ("Block height", f"{net.get('block_height', 0):,}"),
        ("Epoch", f"{net.get('epoch', 'n/a')} · {net.get('epoch_progress_pct', 'n/a')}% complete"),
        ("Non-vote TPS", f"{net.get('nonvote_tps', 'n/a')}"),
        ("Total transactions", f"{net.get('tx_count_total', 0):,}"),
        ("Node version", html.escape(str(net.get("node_version", "n/a")))),
    ]
    validator_rows = [
        ("Active / delinquent validators", f"{val.get('active', 0):,} / {val.get('delinquent', 0):,}"),
        ("Delinquent stake", f"{val.get('delinquent_stake_pct', 'n/a')}%"),
        ("Total stake", f"{val.get('total_stake_sol', 0):,} SOL"),
        ("Nakamoto coefficient", f"{val.get('nakamoto_coefficient', 'n/a')}"),
        ("Median commission", f"{val.get('median_commission', 'n/a')}%"),
        ("Median prioritization fee", f"{val.get('median_prioritization_fee_microlamports', 'n/a')} µlamports"),
    ]
    econ_rows = [
        ("SOL price (24h)", f"${eco.get('sol_price_usd', 'n/a'):,} · {eco.get('sol_24h_change_pct', 0):+.1f}%"
         if eco.get("sol_price_usd") is not None else "n/a"),
        ("Market cap", usd(eco.get("market_cap_usd"))),
        ("Spot volume 24h", usd(eco.get("volume_24h_usd"))),
        ("TVL", usd(eco.get("tvl_usd"))),
        ("DEX volume 24h", usd(eco.get("dex_volume_24h_usd"))),
        ("Chain fees 24h", usd(eco.get("chain_fees_24h_usd"))),
        ("Real economic value 24h", usd(eco.get("rev_24h_usd"))),
        ("Stablecoin supply", usd(eco.get("stablecoin_supply_usd"))),
        ("Circulating supply", f"{sup.get('circulating_sol', 0):,} SOL"),
    ]
    top_rows = [
        (f'<span class="mono">{html.escape(v["vote_pubkey"][:20])}…</span>',
         f"{v['stake_sol']:,}", f"{v['stake_pct']}%", f"{v['commission']}%")
        for v in val.get("top_by_stake", [])
    ]
    charts = []
    for key, name, kind in (
        ("economics.sol_price_usd", "SOL price", "usd"),
        ("network.tps", "TPS", "plain"),
        ("economics.tvl_usd", "TVL", "usd"),
    ):
        series = history.get(key, [])
        values = dict(series)
        marks = [(mt, values[mt], sev) for mt, sev in alert_marks.get(key, []) if mt in values]
        charts.append((name, bigchart(series, marks, kind=kind)))
    switch = "".join(
        f'<button class="sw" data-c="{i}" aria-pressed="{"true" if i == 0 else "false"}">'
        f"{html.escape(name)}</button>"
        for i, (name, _) in enumerate(charts)
    )
    panes = "".join(
        f'<div class="cpane"{"" if i == 0 else " hidden"}>{svg}</div>'
        for i, (_, svg) in enumerate(charts)
    )

    release_rows = [
        (html.escape(r["tag"]) + (" · pre-release" if r["prerelease"] else ""), r["date"])
        for r in eos.get("agave_releases", [])
    ]
    simd_rows = [(html.escape(s["title"]), s["date"]) for s in eos.get("recent_simds", [])]
    status_line = html.escape(
        f"status.solana.com: {eos.get('status_description', 'unavailable this run')}")
    source_rows = [(html.escape(k), html.escape(v)) for k, v in status.items()]

    return f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="dark">
<title>Heliograph · Solana state</title>
<meta name="description" content="An agent that reads Solana so you don't have to: a verdict first, findings with evidence, the dashboard as plumbing. Self-updating every 30 minutes.">
<meta property="og:title" content="Heliograph">
<meta property="og:description" content="An agent that reads Solana so you don't have to. Verdict first; the dashboard is plumbing.">
<meta property="og:url" content="https://wolfurx.github.io/heliograph/">
<meta property="og:image" content="https://wolfurx.github.io/heliograph/social.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="alternate" type="application/rss+xml" title="Heliograph findings" href="feed.xml">
<style>{CSS}</style>
<script>document.documentElement.classList.add('pre')</script>
</head><body>
<div id="tip"></div>
<div class="wrap">

<div class="bar">
  <span class="brand">{GLYPH} Heliograph</span>
  <span class="meta">{when} · run #{baseline["runs"]}{baseline_note}</span>
</div>

<section class="hero">
  <div class="glow" style="--glowc:{glow}"></div>
  <div class="row hero-in"><span class="n" style="color:{hero_color}">{n}</span>{badge}</div>
  <div class="verdict">thing{"s" if n != 1 else ""} need{"" if n != 1 else "s"} your attention. {verdict}</div>
  {ticker}
</section>

{finding_html}

<h2>Pulse</h2>
<div class="tiles">{tiles}</div>

<h2>History<span class="switch" role="group" aria-label="Chart metric">{switch}</span></h2>
<div class="card chartcard rise">{panes}</div>

<h2>Network</h2>
{table(network_rows)}

<h2>Validators</h2>
{table(validator_rows)}

<h2>Top validators by stake</h2>
{table(top_rows, headers=("vote account", "stake (SOL)", "share", "commission"), num_cols=(1, 2, 3))}

<h2>Economics</h2>
{table(econ_rows)}

<h2>Ecosystem</h2>
<div class="secnote">{status_line}</div>
<div class="duo">
{table(release_rows, headers=("agave client release", "date"), num_cols=(1,))}
{table(simd_rows, headers=("recently accepted SIMDs", "date"), num_cols=(1,))}
</div>

<h2>Sources</h2>
{table(source_rows, headers=("source", "status"))}

<footer>
  <span class="thesis">The dashboard is plumbing; the verdict is the product.</span>
  <a href="report.md">Markdown report</a>
  <a href="data.json">data.json</a>
  <a href="feed.xml">RSS alerts</a>
  <a href="https://github.com/WolfurX/heliograph">Source</a>
</footer>
</div>
<script>{JS}</script>
</body></html>
"""
