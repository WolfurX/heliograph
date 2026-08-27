"""Static dark dashboard. One self-contained file, no external assets.

Data rules follow the dataviz method (stat tiles, sparklines in de-emphasis
gray with the current point accented, severity always icon + label, text in
ink tokens never series color, tables as the full-detail channel).

The craft layer follows design-engineering practice: hierarchy from
weight + size + leading as a set, negative tracking on display text,
tabular figures only in columns, depth from a lit top edge instead of
shadows, translucent sticky chrome with a scroll-edge fade instead of a
hard border, staggered entrances on a strong ease-out curve, hover only
on hover-capable pointers, and reduced-motion/transparency fallbacks.
"""

import html
import json
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
html { scroll-behavior: smooth; }
body { background: var(--page); color: var(--ink-2);
  font: 15px/1.55 system-ui, -apple-system, "Segoe UI", sans-serif;
  -webkit-font-smoothing: antialiased; }

.topbar { position: sticky; top: 0; z-index: 5;
  background: color-mix(in srgb, var(--page) 76%, transparent);
  backdrop-filter: blur(16px) saturate(160%);
  -webkit-backdrop-filter: blur(16px) saturate(160%); }
.topbar .in { max-width: 1060px; margin: 0 auto; padding: 14px 24px;
  display: flex; align-items: baseline; gap: 14px; flex-wrap: wrap; }
.topbar::after { content: ""; position: absolute; left: 0; right: 0; bottom: -14px;
  height: 14px; pointer-events: none;
  background: linear-gradient(180deg, color-mix(in srgb, var(--page) 85%, transparent), transparent); }
.brand { color: var(--ink); font-size: 16px; font-weight: 650; letter-spacing: -0.01em;
  display: inline-flex; align-items: center; gap: 8px; }
.brand svg { color: var(--accent); }
.meta { color: var(--muted); font-size: 13px; }

.wrap { max-width: 1060px; margin: 0 auto; padding: 0 24px 72px; }

.hero { margin: 64px 0 10px; }
.hero .n { color: var(--ink); font-size: clamp(64px, 12vw, 96px); font-weight: 650;
  line-height: 0.95; letter-spacing: -0.035em; }
.hero .verdict { color: var(--ink-2); font-size: 17px; line-height: 1.5;
  margin-top: 14px; max-width: 34em; }
.hero .verdict b { color: var(--ink); font-weight: 600; }

.findings { margin: 24px 0 8px; display: grid; gap: 10px; }
.card { background: linear-gradient(180deg, rgba(255,255,255,0.035), rgba(255,255,255,0.015));
  border: 1px solid var(--border); border-top-color: var(--edge); border-radius: 12px; }
.finding { padding: 15px 18px; }
.finding .head { display: flex; align-items: baseline; gap: 10px; flex-wrap: wrap; }
.sev { font-size: 11px; font-weight: 700; letter-spacing: 0.08em; white-space: nowrap; }
.sev::before { content: ""; display: inline-block; width: 7px; height: 7px;
  border-radius: 50%; margin-right: 6px; background: currentColor; }
.sev-crit { color: var(--critical); } .sev-warn { color: var(--warning); } .sev-info { color: var(--accent); }
.finding .headline { color: var(--ink); font-weight: 500; letter-spacing: -0.005em; }
.finding .detail { color: var(--muted); font-size: 13px; margin-top: 6px;
  font-variant-numeric: tabular-nums; }

h2 { color: var(--muted); font-size: 12px; font-weight: 600; letter-spacing: 0.08em;
  text-transform: uppercase; margin: 48px 0 14px; }

.tiles { display: grid; grid-template-columns: repeat(auto-fill, minmax(236px, 1fr)); gap: 12px; }
.tile { padding: 16px 18px 12px; }
.tile .label { color: var(--muted); font-size: 13px; letter-spacing: 0; }
.tile .value { color: var(--ink); font-size: 30px; font-weight: 650;
  letter-spacing: -0.02em; line-height: 1.15; margin-top: 4px; }
.tile .delta { font-size: 13px; margin-left: 8px; font-weight: 550; letter-spacing: 0; }
.d-good { color: var(--good); } .d-bad { color: var(--critical); } .d-flat { color: var(--muted); }
.spark { margin-top: 10px; display: block; width: 100%; }

.tbl { width: 100%; border-collapse: collapse; overflow: hidden; }
.tblwrap { overflow-x: auto; border-radius: 12px; }
.tbl th, .tbl td { text-align: left; padding: 10px 16px; font-size: 14px; }
.tbl th { color: var(--muted); font-size: 11.5px; font-weight: 600;
  letter-spacing: 0.07em; text-transform: uppercase; }
.tbl td { color: var(--ink-2); border-top: 1px solid var(--grid);
  font-variant-numeric: tabular-nums; }
.tbl td:first-child { font-variant-numeric: normal; }
.tbl tr:last-child td { border-bottom: none; }
.mono { font-family: ui-monospace, "SF Mono", monospace; font-size: 12.5px; }
.num { text-align: right; }
th.num { text-align: right; }

footer { margin-top: 56px; color: var(--muted); font-size: 13px;
  border-top: 1px solid var(--grid); padding-top: 18px;
  display: flex; gap: 18px; flex-wrap: wrap; }
footer a { color: var(--ink-2); text-decoration: none;
  transition: color 140ms var(--ease); }
footer .thesis { flex: 1 1 100%; }

#tip { position: fixed; pointer-events: none; z-index: 9; display: none;
  background: color-mix(in srgb, var(--page) 88%, transparent);
  backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);
  border: 1px solid var(--edge); border-radius: 7px; padding: 5px 9px;
  font-size: 12px; color: var(--ink); font-variant-numeric: tabular-nums;
  opacity: 0; transition: opacity 100ms var(--ease); }

@media (hover: hover) and (pointer: fine) {
  .tile { transition: transform 180ms var(--ease), border-color 180ms var(--ease); }
  .tile:hover { transform: translateY(-2px); border-color: rgba(255,255,255,0.16);
    border-top-color: rgba(255,255,255,0.22); }
  footer a:hover { color: var(--accent); }
}

@media (prefers-reduced-motion: no-preference) {
  .rise { animation: rise 440ms var(--ease) backwards; }
  .tiles .tile:nth-child(1) { animation-delay: 40ms; }
  .tiles .tile:nth-child(2) { animation-delay: 80ms; }
  .tiles .tile:nth-child(3) { animation-delay: 120ms; }
  .tiles .tile:nth-child(4) { animation-delay: 160ms; }
  .tiles .tile:nth-child(5) { animation-delay: 200ms; }
  .tiles .tile:nth-child(6) { animation-delay: 240ms; }
  .findings .finding:nth-child(2) { animation-delay: 50ms; }
  .findings .finding:nth-child(3) { animation-delay: 100ms; }
}
@keyframes rise { from { opacity: 0; transform: translateY(10px); } }
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  .rise { animation: fade 200ms ease backwards; }
  .tile { transition: none; }
}
@keyframes fade { from { opacity: 0; } }
@media (prefers-reduced-transparency: reduce) {
  .topbar, #tip { backdrop-filter: none; -webkit-backdrop-filter: none;
    background: var(--page); }
}
"""

JS = """
const tip = document.getElementById('tip');
document.querySelectorAll('.spark').forEach(svg => {
  const pts = JSON.parse(svg.dataset.points);
  const unit = svg.dataset.unit || '';
  svg.addEventListener('mousemove', e => {
    const r = svg.getBoundingClientRect();
    const i = Math.min(pts.length - 1, Math.max(0,
      Math.round((e.clientX - r.left) / r.width * (pts.length - 1))));
    const [t, v] = pts[i];
    const d = new Date(t * 1000);
    tip.textContent = v.toLocaleString(undefined, {maximumFractionDigits: 1}) + unit +
      ' · ' + d.toISOString().slice(5, 16).replace('T', ' ') + ' UTC';
    tip.style.left = (e.clientX + 12) + 'px';
    tip.style.top = (e.clientY - 30) + 'px';
    tip.style.display = 'block';
    requestAnimationFrame(() => tip.style.opacity = '1');
  });
  svg.addEventListener('mouseleave', () => {
    tip.style.opacity = '0'; tip.style.display = 'none';
  });
});
"""

GLYPH = (
    '<svg width="15" height="15" viewBox="0 0 15 15" fill="none" aria-hidden="true">'
    '<circle cx="7.5" cy="7.5" r="3" fill="currentColor"/>'
    '<g stroke="currentColor" stroke-width="1.2" stroke-linecap="round">'
    '<line x1="7.5" y1="0.8" x2="7.5" y2="2.6"/><line x1="7.5" y1="12.4" x2="7.5" y2="14.2"/>'
    '<line x1="0.8" y1="7.5" x2="2.6" y2="7.5"/><line x1="12.4" y1="7.5" x2="14.2" y2="7.5"/>'
    "</g></svg>"
)

SEV_LABEL = {"crit": ("CRITICAL", "sev-crit"),
             "warn": ("WARNING", "sev-warn"),
             "info": ("INFO", "sev-info")}


def compact(n, unit=""):
    if n is None:
        return "n/a"
    if unit == "$":
        return usd(n)
    for div, suffix in ((1e9, "B"), (1e6, "M"), (1e3, "K")):
        if abs(n) >= div:
            return f"{n / div:,.1f}{suffix}"
    return f"{n:,.10g}"


def sparkline(points, w=220, h=44):
    """12-point trend: de-emphasis gray line over a faint accent wash,
    current point accented (>=8px dot with a 2px surface ring)."""
    pts = points[-12:]
    if len(pts) < 2:
        return '<div class="spark" style="height:44px"></div>'
    vals = [v for _, v in pts]
    lo, hi = min(vals), max(vals)
    pad = 6
    if hi == lo:  # flat series sits on the midline, not the floor
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
    px, py = xy[-2]
    data = html.escape(json.dumps(pts), quote=True)
    return (
        f'<svg class="spark" height="{h}" viewBox="0 0 {w} {h}" '
        f'preserveAspectRatio="none" data-points="{data}">'
        f'<polygon points="{area}" fill="var(--accent)" opacity="0.07"/>'
        f'<polyline points="{poly}" fill="none" stroke="var(--muted)" stroke-width="2" '
        f'stroke-linejoin="round" stroke-linecap="round" vector-effect="non-scaling-stroke"/>'
        f'<line x1="{px:.1f}" y1="{py:.1f}" x2="{cx:.1f}" y2="{cy:.1f}" '
        f'stroke="var(--accent)" stroke-width="2" stroke-linecap="round" '
        f'vector-effect="non-scaling-stroke"/>'
        f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="4" fill="var(--accent)" '
        f'stroke="var(--surface)" stroke-width="2"/>'
        f"</svg>"
    )


def tile(label, value, series, up_good=True, unit=""):
    delta = ""
    if len(series) >= 2 and series[-2][1]:
        prev, cur = series[-2][1], series[-1][1]
        pct = 100 * (cur - prev) / abs(prev)
        if abs(pct) < 0.05:
            delta = '<span class="delta d-flat">±0.0%</span>'
        else:
            good = (pct > 0) == up_good
            cls = "d-good" if good else "d-bad"
            delta = f'<span class="delta {cls}">{pct:+.1f}%</span>'
    return (
        f'<div class="tile card rise"><div class="label">{html.escape(label)}</div>'
        f'<div class="value">{value}{delta}</div>'
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
    return (f'<div class="tblwrap card rise"><table class="tbl">'
            f"<tr>{head}</tr>{body}</table></div>")


def build(sections, findings, baseline, status, ts, history):
    net = sections.get("network", {})
    val = sections.get("validators", {})
    eco = sections.get("economics", {})
    sup = sections.get("supply", {})
    when = datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    n = len(findings)
    if n == 0:
        verdict = ("Every watched metric is inside its normal band. "
                   "<b>Nothing to do here.</b>")
    else:
        verdict = ("Read the findings below, then stop. "
                   "The rest of the page is evidence.")
    finding_html = "".join(
        f'<div class="finding card rise"><div class="head">'
        f'<span class="sev {SEV_LABEL[f["severity"]][1]}">{SEV_LABEL[f["severity"]][0]}</span>'
        f'<span class="headline">{html.escape(f["headline"])}</span></div>'
        f'<div class="detail">{html.escape(f["detail"])}</div></div>'
        for f in findings
    )

    tiles = "".join([
        tile("Transactions per second", compact(net.get("tps")), history.get("network.tps", [])),
        tile("Slot time", f"{net.get('slot_time_ms', 'n/a')} ms",
             history.get("network.slot_time_ms", []), up_good=False, unit=" ms"),
        tile("SOL price", f"${compact(eco.get('sol_price_usd'))}",
             history.get("economics.sol_price_usd", []), unit=" $"),
        tile("Total value locked", usd(eco.get("tvl_usd")),
             history.get("economics.tvl_usd", []), unit=" $"),
        tile("DEX volume 24h", usd(eco.get("dex_volume_24h_usd")),
             history.get("economics.dex_volume_24h_usd", []), unit=" $"),
        tile("Delinquent stake", f"{val.get('delinquent_stake_pct', 'n/a')}%",
             history.get("validators.delinquent_stake_pct", []), up_good=False, unit="%"),
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
        ("Stablecoin supply", usd(eco.get("stablecoin_supply_usd"))),
        ("Circulating supply", f"{sup.get('circulating_sol', 0):,} SOL"),
    ]
    top_rows = [
        (f'<span class="mono">{html.escape(v["vote_pubkey"][:20])}…</span>',
         f"{v['stake_sol']:,}", f"{v['stake_pct']}%", f"{v['commission']}%")
        for v in val.get("top_by_stake", [])
    ]
    source_rows = [(html.escape(k), html.escape(v)) for k, v in status.items()]

    return f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="dark">
<title>Heliograph · Solana state</title>
<style>{CSS}</style>
</head><body>
<div id="tip"></div>
<div class="topbar"><div class="in">
  <span class="brand">{GLYPH} Heliograph</span>
  <span class="meta">reads Solana so you don't have to</span>
  <span class="meta">{when} · run #{baseline["runs"]} · baseline {baseline["status"]}</span>
</div></div>
<div class="wrap">

<section class="hero rise">
  <div class="n">{n}</div>
  <div class="verdict">thing{"s" if n != 1 else ""} need{"" if n != 1 else "s"} your attention. {verdict}</div>
</section>

<div class="findings">{finding_html}</div>

<h2>Pulse</h2>
<div class="tiles">{tiles}</div>

<h2>Network</h2>
{table(network_rows)}

<h2>Validators</h2>
{table(validator_rows)}

<h2>Top validators by stake</h2>
{table(top_rows, headers=("vote account", "stake (SOL)", "share", "commission"), num_cols=(1, 2, 3))}

<h2>Economics</h2>
{table(econ_rows)}

<h2>Sources</h2>
{table(source_rows, headers=("source", "status"))}

<footer>
  <span class="thesis">The dashboard is plumbing; the report is the product.</span>
  <a href="report.md">Markdown report</a>
  <a href="data.json">data.json</a>
  <a href="https://github.com/WolfurX/heliograph">Source</a>
</footer>
</div>
<script>{JS}</script>
</body></html>
"""
