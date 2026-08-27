"""Static dark dashboard. One self-contained file, no external assets.

The "Signal" direction: the verdict is the page. A status-colored glow and
an oversized count lead; findings sit in plain ledger rows (hairline rules,
a small colored dot + plain-weight label - never a tinted callout box);
the metrics are large bare tiles with accent sparklines; tables carry the
full detail. Craft rules: hierarchy from weight+size+leading, negative
tracking on display sizes, tabular figures only in columns, staggered
entrances on a strong ease-out, reduced-motion and reduced-transparency
fallbacks, hover effects only on hover-capable pointers.
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

h2 { display: flex; align-items: center; gap: 10px; color: var(--ink-2); font-size: 12px;
  font-weight: 650; letter-spacing: .1em; text-transform: uppercase; margin: 56px 0 22px; }
h2::before { content: ""; width: 18px; height: 2px; background: var(--accent); }
.secnote { color: var(--muted); font-size: 13px; margin: -12px 0 18px; }

.tiles { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 30px 34px; }
.tile .l { color: var(--muted); font-size: 13px; }
.tile .v { color: var(--ink); font-size: 42px; font-weight: 700; letter-spacing: -.03em;
  line-height: 1.1; margin: 4px 0 8px; }
.delta { font-size: 14px; margin-left: 9px; font-weight: 600; }
.d-good { color: var(--good); } .d-bad { color: var(--critical); }
.spark { display: block; width: 100%; }

.card { background: linear-gradient(180deg, rgba(255,255,255,.035), rgba(255,255,255,.015));
  border: 1px solid var(--border); border-top-color: var(--edge); border-radius: 14px;
  overflow-x: auto; }
.duo { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 14px; }
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
}
@media (prefers-reduced-motion: no-preference) {
  .rise { animation: rise 400ms var(--ease) backwards; }
  .tiles .tile:nth-child(1) { animation-delay: 60ms; }
  .tiles .tile:nth-child(2) { animation-delay: 110ms; }
  .tiles .tile:nth-child(3) { animation-delay: 160ms; }
  .tiles .tile:nth-child(4) { animation-delay: 210ms; }
  .tiles .tile:nth-child(5) { animation-delay: 260ms; }
  .tiles .tile:nth-child(6) { animation-delay: 310ms; }
}
@keyframes rise { from { opacity: 0; transform: translateY(10px); } }
@keyframes focusin { from { opacity: 0; filter: blur(6px); transform: scale(.985); } }
@keyframes fade { from { opacity: 0; } }
@media (prefers-reduced-motion: reduce) {
  .rise, .hero-in { animation: fade 180ms ease backwards; }
}
@media (prefers-reduced-transparency: reduce) {
  #tip { backdrop-filter: none; -webkit-backdrop-filter: none; background: var(--page); }
}
"""

JS = """
const tip = document.getElementById('tip');
document.addEventListener('mousemove', e => {
  const svg = e.target.closest ? e.target.closest('.spark') : null;
  if (!svg || !svg.dataset.points) { tip.style.opacity = '0'; tip.style.display = 'none'; return; }
  const pts = JSON.parse(svg.dataset.points);
  const r = svg.getBoundingClientRect();
  const i = Math.min(pts.length - 1, Math.max(0,
    Math.round((e.clientX - r.left) / r.width * (pts.length - 1))));
  const [t, v] = pts[i];
  tip.textContent = v.toLocaleString(undefined, {maximumFractionDigits: 1}) +
    ' · ' + new Date(t * 1000).toISOString().slice(5, 16).replace('T', ' ') + ' UTC';
  tip.style.left = (e.clientX + 12) + 'px';
  tip.style.top = (e.clientY - 30) + 'px';
  tip.style.display = 'block';
  requestAnimationFrame(() => tip.style.opacity = '1');
});
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


def build(sections, findings, baseline, status, ts, history):
    net = sections.get("network", {})
    val = sections.get("validators", {})
    eco = sections.get("economics", {})
    sup = sections.get("supply", {})
    eos = sections.get("ecosystem", {})
    when = datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

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

    finding_html = "".join(
        f'<div class="finding rise" style="--sc:var(--{SEV_COLOR[f["severity"]]})">'
        f'<span class="sev">{SEV_WORD[f["severity"]]}</span>'
        f'<div class="headline">{html.escape(f["headline"])}</div>'
        f'<div class="detail">{html.escape(f["detail"])}</div></div>'
        for f in findings
    )

    tiles = "".join([
        tile("Transactions per second", compact(net.get("tps")), history.get("network.tps", [])),
        tile("Slot time", f"{net.get('slot_time_ms', 'n/a')} ms",
             history.get("network.slot_time_ms", []), up_good=False),
        tile("SOL price", f"${compact(eco.get('sol_price_usd'))}",
             history.get("economics.sol_price_usd", [])),
        tile("Total value locked", usd(eco.get("tvl_usd")),
             history.get("economics.tvl_usd", [])),
        tile("DEX volume 24h", usd(eco.get("dex_volume_24h_usd")),
             history.get("economics.dex_volume_24h_usd", [])),
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
<link rel="alternate" type="application/rss+xml" title="Heliograph findings" href="feed.xml">
<style>{CSS}</style>
</head><body>
<div id="tip"></div>
<div class="wrap">

<div class="bar">
  <span class="brand">{GLYPH} Heliograph</span>
  <span class="meta">{when} · run #{baseline["runs"]} · baseline {baseline["status"]}</span>
</div>

<section class="hero">
  <div class="glow" style="--glowc:{glow}"></div>
  <div class="row hero-in"><span class="n" style="color:{hero_color}">{n}</span>{badge}</div>
  <div class="verdict">thing{"s" if n != 1 else ""} need{"" if n != 1 else "s"} your attention. {verdict}</div>
</section>

{finding_html}

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
