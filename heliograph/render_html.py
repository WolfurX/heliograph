"""Static dark dashboard. One self-contained file, no external assets.

Design follows the reference dataviz method: stat tiles (label / value /
delta / 12-point sparkline in de-emphasis gray with the current point in
accent), one hero figure (the attention count - the thesis as a number),
status severity always as icon + label, text in ink tokens never series
color, hairline grid, tables as the full-detail channel.
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
  --border: rgba(255,255,255,0.10); --accent: #3987e5;
  --good: #0ca30c; --warning: #fab219; --serious: #ec835a; --critical: #d03b3b;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body { background: var(--page); color: var(--ink-2); font: 15px/1.55 system-ui, -apple-system, "Segoe UI", sans-serif; }
.wrap { max-width: 1080px; margin: 0 auto; padding: 40px 24px 64px; }
header h1 { color: var(--ink); font-size: 22px; font-weight: 600; letter-spacing: .2px; }
header .sub { color: var(--muted); font-size: 13px; margin-top: 4px; }
.hero { margin: 36px 0 8px; }
.hero .n { color: var(--ink); font-size: 56px; font-weight: 600; line-height: 1; }
.hero .verdict { color: var(--ink-2); font-size: 16px; margin-top: 8px; max-width: 560px; }
.findings { margin: 20px 0 8px; display: grid; gap: 10px; }
.finding { background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 14px 16px; }
.finding .head { display: flex; align-items: baseline; gap: 10px; }
.sev { font-size: 11px; font-weight: 700; letter-spacing: .8px; }
.sev-crit { color: var(--critical); } .sev-warn { color: var(--warning); } .sev-info { color: var(--accent); }
.finding .headline { color: var(--ink); font-weight: 500; }
.finding .detail { color: var(--muted); font-size: 13px; margin-top: 6px; }
h2 { color: var(--ink); font-size: 15px; font-weight: 600; margin: 40px 0 14px; }
.tiles { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 12px; }
.tile { background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 14px 16px; position: relative; }
.tile .label { color: var(--muted); font-size: 13px; }
.tile .value { color: var(--ink); font-size: 26px; font-weight: 600; margin-top: 2px; }
.tile .delta { font-size: 13px; margin-left: 8px; font-weight: 500; }
.d-good { color: var(--good); } .d-bad { color: var(--critical); } .d-flat { color: var(--muted); }
.spark { margin-top: 10px; display: block; }
.tbl { width: 100%; border-collapse: collapse; background: var(--surface); border: 1px solid var(--border); border-radius: 8px; overflow: hidden; }
.tbl th, .tbl td { text-align: left; padding: 9px 14px; border-top: 1px solid var(--grid); font-size: 14px; }
.tbl th { color: var(--muted); font-weight: 500; border-top: none; }
.tbl td { color: var(--ink-2); font-variant-numeric: tabular-nums; }
.tbl td:first-child { color: var(--ink-2); font-variant-numeric: normal; }
.tblwrap { overflow-x: auto; }
.mono { font-family: ui-monospace, monospace; font-size: 12.5px; }
footer { margin-top: 48px; color: var(--muted); font-size: 13px; border-top: 1px solid var(--grid); padding-top: 16px; }
footer a { color: var(--accent); text-decoration: none; }
#tip { position: fixed; pointer-events: none; background: var(--page); border: 1px solid var(--border);
  border-radius: 6px; padding: 5px 9px; font-size: 12px; color: var(--ink); display: none; z-index: 9; }
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
  });
  svg.addEventListener('mouseleave', () => tip.style.display = 'none');
});
"""

SEV_LABEL = {"crit": ("▲", "CRITICAL", "sev-crit"),
             "warn": ("▲", "WARNING", "sev-warn"),
             "info": ("●", "INFO", "sev-info")}


def compact(n, unit=""):
    if n is None:
        return "n/a"
    if unit == "$":
        return usd(n)
    for div, suffix in ((1e9, "B"), (1e6, "M"), (1e3, "K")):
        if abs(n) >= div:
            return f"{n / div:,.1f}{suffix}"
    return f"{n:,.10g}"


def sparkline(points, w=210, h=36):
    """12-point trend: de-emphasis gray line, current point accented
    (>=8px dot with a 2px surface ring), 2px round-capped strokes."""
    pts = points[-12:]
    if len(pts) < 2:
        return '<div class="spark" style="height:36px"></div>'
    vals = [v for _, v in pts]
    lo, hi = min(vals), max(vals)
    span = (hi - lo) or 1
    pad = 5
    xy = [
        (pad + i * (w - 2 * pad) / (len(pts) - 1),
         pad + (h - 2 * pad) * (1 - (v - lo) / span))
        for i, (_, v) in enumerate(pts)
    ]
    poly = " ".join(f"{x:.1f},{y:.1f}" for x, y in xy)
    cx, cy = xy[-1]
    px, py = xy[-2]
    data = html.escape(json.dumps(pts), quote=True)
    return (
        f'<svg class="spark" width="{w}" height="{h}" viewBox="0 0 {w} {h}" data-points="{data}">'
        f'<polyline points="{poly}" fill="none" stroke="var(--muted)" stroke-width="2" '
        f'stroke-linejoin="round" stroke-linecap="round"/>'
        f'<line x1="{px:.1f}" y1="{py:.1f}" x2="{cx:.1f}" y2="{cy:.1f}" '
        f'stroke="var(--accent)" stroke-width="2" stroke-linecap="round"/>'
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
        f'<div class="tile"><div class="label">{html.escape(label)}</div>'
        f'<div class="value">{value}{delta}</div>'
        f"{sparkline(series) if series else ''}</div>"
    )


def table(rows, headers=("metric", "value")):
    head = "".join(f"<th>{html.escape(h)}</th>" for h in headers)
    body = "".join(
        "<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>" for row in rows
    )
    return f'<div class="tblwrap"><table class="tbl"><tr>{head}</tr>{body}</table></div>'


def build(sections, findings, baseline, status, ts, history):
    net = sections.get("network", {})
    val = sections.get("validators", {})
    eco = sections.get("economics", {})
    sup = sections.get("supply", {})
    when = datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    n = len(findings)
    verdict = (
        "Every watched metric is inside its normal band. Nothing to do here."
        if n == 0 else
        "Read the findings below, then stop. The rest of the page is evidence."
    )
    finding_html = "".join(
        f'<div class="finding"><div class="head">'
        f'<span class="sev {SEV_LABEL[f["severity"]][2]}">{SEV_LABEL[f["severity"]][0]} '
        f'{SEV_LABEL[f["severity"]][1]}</span>'
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
<div class="wrap">
<header>
  <h1>Heliograph</h1>
  <div class="sub">Reads Solana so you don't have to · generated {when} · run #{baseline["runs"]} · baseline {baseline["status"]}</div>
</header>

<section class="hero">
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
{table(top_rows, headers=("vote account", "stake (SOL)", "share", "commission"))}

<h2>Economics</h2>
{table(econ_rows)}

<h2>Sources</h2>
{table(source_rows, headers=("source", "status"))}

<footer>
  The dashboard is plumbing; the <a href="report.md">report</a> is the product.
  Machine-readable: <a href="data.json">data.json</a> ·
  <a href="https://github.com/WolfurX/heliograph">source</a>
</footer>
</div>
<script>{JS}</script>
</body></html>
"""
