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
.ticker { position: absolute; right: 0; top: 140px; text-align: right;
  border-left: 1px solid var(--grid); padding-left: 26px; }
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
.via { margin-left: auto; color: var(--muted); font-size: 11.5px; font-weight: 400;
  letter-spacing: .02em; text-transform: none; }
.secnote { color: var(--muted); font-size: 13px; margin: -12px 0 18px; }

.source { border-top: 1px solid var(--grid); padding: 15px 0; }
.source:last-of-type { border-bottom: 1px solid var(--grid); }
.s-head { display: flex; align-items: center; gap: 13px; }
.slogo { width: 18px; height: 18px; flex: none; color: var(--muted); }
.s-name { color: var(--ink); font-weight: 550; font-size: 15px; flex: 1; }
.s-stat { color: var(--muted); font-size: 13px; font-variant-numeric: tabular-nums; }
.s-stat::before { content: ""; display: inline-block; width: 7px; height: 7px;
  border-radius: 50%; margin-right: 8px; background: var(--sc, var(--good)); }
.s-err { color: var(--muted); font-size: 13px; margin: 6px 0 0 31px;
  font-variant-numeric: tabular-nums; }

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
  .ticker { position: static; text-align: left; margin-top: 24px;
    border-left: none; border-top: 1px solid var(--grid); padding: 16px 0 0; }
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


def _mark(viewbox, body):
    return f'<svg class="slogo" viewBox="{viewbox}" aria-hidden="true">{body}</svg>'


# Source marks, inlined so the page stays one self-contained file, all
# currentColor. Solana and GitHub: Simple Icons (CC0). CoinGecko: Arcticons
# (CC BY-SA 4.0), stroke thickened for weight parity with the filled marks.
# DeFiLlama: Microsoft Fluent Emoji high-contrast llama (MIT). Dune: drawn
# here after their circle-over-dunes brand mark.
MARKS = {
    "solana": _mark("0 0 24 24", '<path fill="currentColor" d="m23.8764 18.0313-3.962 4.1393a.9201.9201 0 0 1-.306.2106.9407.9407 0 0 1-.367.0742H.4599a.4689.4689 0 0 1-.2522-.0733.4513.4513 0 0 1-.1696-.1962.4375.4375 0 0 1-.0314-.2545.4438.4438 0 0 1 .117-.2298l3.9649-4.1393a.92.92 0 0 1 .3052-.2102.9407.9407 0 0 1 .3658-.0746H23.54a.4692.4692 0 0 1 .2523.0734.4531.4531 0 0 1 .1697.196.438.438 0 0 1 .0313.2547.4442.4442 0 0 1-.1169.2297zm-3.962-8.3355a.9202.9202 0 0 0-.306-.2106.941.941 0 0 0-.367-.0742H.4599a.4687.4687 0 0 0-.2522.0734.4513.4513 0 0 0-.1696.1961.4376.4376 0 0 0-.0314.2546.444.444 0 0 0 .117.2297l3.9649 4.1394a.9204.9204 0 0 0 .3052.2102c.1154.049.24.0744.3658.0746H23.54a.469.469 0 0 0 .2523-.0734.453.453 0 0 0 .1697-.1961.4382.4382 0 0 0 .0313-.2546.4444.4444 0 0 0-.1169-.2297zM.46 6.7225h18.7815a.9411.9411 0 0 0 .367-.0742.9202.9202 0 0 0 .306-.2106l3.962-4.1394a.4442.4442 0 0 0 .117-.2297.4378.4378 0 0 0-.0314-.2546.453.453 0 0 0-.1697-.196.469.469 0 0 0-.2523-.0734H4.7596a.941.941 0 0 0-.3658.0745.9203.9203 0 0 0-.3052.2102L.1246 5.9687a.4438.4438 0 0 0-.1169.2295.4375.4375 0 0 0 .0312.2544.4512.4512 0 0 0 .1692.196.4689.4689 0 0 0 .2518.0739z"/>'),
    "github": _mark("0 0 24 24", '<path fill="currentColor" d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/>'),
    "coingecko": _mark("0 0 48 48",
        '<g fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">'
        '<circle cx="24" cy="24" r="21.5"/>'
        '<path d="M7.051 37.228c4.519-9.359 1.828-21.471 9.117-23.377s12.056 1.345 15.87 2.467s6.978 1.716 7.682 5.27C40.729 26.693 24.13 35.71 27.664 45.5"/>'
        '<path d="M24.355 26.972c3.196 2.523 6.496 1.685 13.796-1.373m-8.302-10.062c0-2.273-4.148-4.098-6.719-2.079"/>'
        '<circle cx="21.047" cy="19.122" r="3.308"/><circle cx="21.047" cy="19.122" r="1.29"/>'
        '<path d="M42.375 22.99A18.404 18.404 0 0 0 25.033 5.628"/></g>'
        '<circle cx="34.841" cy="22.991" r="1.5" fill="currentColor"/>'),
    "defillama": _mark("0 0 32 32",
        '<path fill="currentColor" d="M6.86 8.203a.5.5 0 1 0 0-1a.5.5 0 0 0 0 1"/>'
        '<path fill="currentColor" d="m29.844 21.558l.087.084a3.47 3.47 0 0 1 1.06 2.547v5.491a2.31 2.31 0 0 1-2.31 2.31h-1.37a2.31 2.31 0 0 1-2.31-2.31v-2.151l-.644-.395l-1.775 3.222l-.021.028c-.267.355-.68.585-1.15.585h-1.03c-.624 0-.96-.645-.744-1.155l1.676-4.547l.014-.027l.001-.002a5.5 5.5 0 0 1-.784-.732A6.4 6.4 0 0 1 18.07 25h-.551l1.277 4.952l.002.008a.94.94 0 0 1-.052.581a.71.71 0 0 1-.656.428h-.004l-1.398-.01c-.127 0-.3-.02-.466-.105a.76.76 0 0 1-.397-.507l-.872-3.308a.15.15 0 0 0-.06-.087l-.003-.002a3 3 0 0 1-.143-.092a4.7 4.7 0 0 1-.747 1.39v1.442c0 1.316-1.077 2.31-2.32 2.31h-1.37c-1.225 0-2.333-.998-2.3-2.345V23.87A6.72 6.72 0 0 1 5 18.26v-5.729h-.73c-1.141 0-1.982-.641-2.46-1.238A3.68 3.68 0 0 1 1 9.031c0-.511.123-1.048.303-1.5c.158-.395.51-1.115 1.241-1.57l.004-.002l3.108-1.922q.207-.132.415-.245l-.268-.818A2.25 2.25 0 0 1 7.941 0a4.23 4.23 0 0 1 3.989 2.842l.005.015l3.342 10.103h7.974c1.142 0 2.206.333 3.101.908a2 2 0 1 1 2.35 3.006c.194.577.3 1.194.3 1.836v2.21zm-2.573.562a.94.94 0 0 1-.27-.66v-2.75c0-2.07-1.68-3.75-3.75-3.75h-8.17c-.66 0-1.27-.38-1.57-.97L10.041 3.5a2.24 2.24 0 0 0-1.53-1.425l-.034-.009A2.2 2.2 0 0 0 7.941 2c-.18 0-.3.17-.24.34L8.571 5a1 1 0 0 0-.135.016c-.136.025-.34.079-.579.164a2.96 2.96 0 0 1 1.944 2.77v1c0 1.126-.911 2.05-2.04 2.05h-.76v7.26c0 2.01 1.25 3.72 3.01 4.41v7.02c-.01.17.13.31.3.31h1.37c.137 0 .25-.08.297-.194a.3.3 0 0 0 .023-.116v-1.96q0-.057.01-.11a.67.67 0 0 1 .17-.33c.53-.52.82-1.23.82-1.97V23h5.07a4.45 4.45 0 0 0 3.33-1.5c0 .749.305 1.396.884 1.932q.222.205.496.388l3.96 2.43a.61.61 0 0 1 .26.5v2.93c0 .17.14.31.31.31h1.37c.17 0 .31-.14.31-.31v-5.51c.01-.4-.15-.8-.45-1.09zM3.03 9c.125.572.633 1 1.241 1h3.49c.57 0 1.04-.47 1.04-1.05v-1A1.96 1.96 0 0 0 5.89 6.245L3.6 7.66a1 1 0 0 0-.307.34H3.5c.28 0 .5.22.5.5s-.22.5-.5.5z"/>'),
    "dune": _mark("0 0 24 24",
        '<path fill="currentColor" d="M12 1.5a10.5 10.5 0 0 1 10.5 10.5c0 1.06-.16 2.09-.45 3.05c-2.2 1.1-4.42.36-6.87-.55c-2.77-1.03-5.83-2.16-9.4-.66l-3.83 1.61A10.5 10.5 0 0 1 12 1.5Z"/>'
        '<path fill="currentColor" d="M21.32 17.05a10.5 10.5 0 0 1-18.5-.15l3.55-1.5c2.86-1.2 5.36-.28 8.06.72c2.2.82 4.5 1.67 6.89.93Z"/>'),
}

# collector -> provider grouping for the Sources ledger
PROVIDERS = [
    ("Solana RPC", "solana", (("solana_rpc_network", "network"),
                              ("solana_rpc_validators", "validators"),
                              ("solana_rpc_supply", "supply"))),
    ("CoinGecko", "coingecko", (("coingecko", "price"),)),
    ("DeFiLlama", "defillama", (("defillama_tvl", "tvl"), ("defillama_dex", "dex volume"),
                                ("defillama_fees", "fees"), ("defillama_stablecoins", "stablecoins"),
                                ("defillama_rev", "revenue"))),
    ("Solana Status", "solana", (("solana_statuspage", "statuspage"),)),
    ("GitHub", "github", (("github_agave_releases", "agave releases"),
                          ("github_simds", "SIMDs"))),
    ("Dune", "dune", (("dune_active_wallets", "active wallets"),)),
]


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

    # SOL price lives in the hero ticker alone; the grid leads with the other
    # regular-user metrics, operator metrics follow. The active-wallets tile
    # only exists when the Dune source is configured.
    daw = eos.get("daily_active_wallets")
    tiles = "".join([
        tile("Total value locked", usd(eco.get("tvl_usd")),
             history.get("economics.tvl_usd", [])),
        tile("DEX volume 24h", usd(eco.get("dex_volume_24h_usd")),
             history.get("economics.dex_volume_24h_usd", [])),
    ] + ([tile("Daily active wallets", compact(daw),
               history.get("ecosystem.daily_active_wallets", []))]
         if daw is not None else []) + [
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

    source_html, seen = [], set()
    for pname, mark, feeds in PROVIDERS:
        present = [(k, label) for k, label in feeds if k in status]
        if not present:
            continue
        seen.update(k for k, _ in present)
        errs = [(label, status[k]) for k, label in present if status[k] != "ok"]
        n = len(present)
        stat = (f"{n - len(errs)}/{n} ok" if errs
                else ("ok" if n == 1 else f"{n}/{n} ok"))
        color = "critical" if errs else "good"
        err_html = "".join(
            f'<div class="s-err">{html.escape(label)}: {html.escape(msg)}</div>'
            for label, msg in errs)
        source_html.append(
            f'<div class="source rise"><div class="s-head">{MARKS[mark]}'
            f'<span class="s-name">{html.escape(pname)}</span>'
            f'<span class="s-stat" style="--sc:var(--{color})">{stat}</span></div>'
            f"{err_html}</div>")
    for k, v in status.items():  # future collectors the map doesn't know yet
        if k in seen:
            continue
        color = "good" if v == "ok" else "critical"
        source_html.append(
            f'<div class="source rise"><div class="s-head">'
            f'<span class="slogo"></span><span class="s-name">{html.escape(k)}</span>'
            f'<span class="s-stat" style="--sc:var(--{color})">{html.escape(v)}</span>'
            f"</div></div>")
    sources_block = "".join(source_html)
    eco_via = "via CoinGecko and DeFiLlama"
    eos_via = ("via Solana Status, GitHub, and Dune"
               if "dune_active_wallets" in status else "via Solana Status and GitHub")

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

<h2>Network<span class="via">via Solana RPC</span></h2>
{table(network_rows)}

<h2>Validators<span class="via">via Solana RPC</span></h2>
{table(validator_rows)}

<h2>Top validators by stake<span class="via">via Solana RPC</span></h2>
{table(top_rows, headers=("vote account", "stake (SOL)", "share", "commission"), num_cols=(1, 2, 3))}

<h2>Economics<span class="via">{eco_via}</span></h2>
{table(econ_rows)}

<h2>Ecosystem<span class="via">{eos_via}</span></h2>
<div class="secnote">{status_line}</div>
<div class="duo">
{table(release_rows, headers=("agave client release", "date"), num_cols=(1,))}
{table(simd_rows, headers=("recently accepted SIMDs", "date"), num_cols=(1,))}
</div>

<h2>Sources</h2>
{sources_block}

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
