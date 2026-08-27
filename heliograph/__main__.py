"""One run: collect -> store -> analyze -> render JSON, Markdown, HTML."""

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from . import anomaly, collect, report
from .store import Store

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
DB = ROOT / "data" / "heliograph.db"
SCHEMA_VERSION = 1


def main():
    ts = int(time.time())
    sections, status = collect.collect_all()

    ok = [k for k, v in status.items() if v == "ok"]
    if not ok:
        print("every source failed, nothing to report:", status, file=sys.stderr)
        return 1

    store = Store(DB)
    store.save(ts, sections)
    findings, baseline = anomaly.analyze(sections, store, ts)

    snapshot = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": datetime.fromtimestamp(ts, tz=timezone.utc).isoformat(),
        "generated_ts": ts,
        "baseline": baseline,
        "anomalies": findings,
        **sections,
        "sources": status,
    }

    DOCS.mkdir(exist_ok=True)
    (DOCS / "data.json").write_text(json.dumps(snapshot, indent=2) + "\n")
    (DOCS / "report.md").write_text(report.build(sections, findings, baseline, status, ts))

    from . import render_html
    history = {name: store.series(name, limit=96) for name in
               ("network.tps", "network.slot_time_ms", "economics.sol_price_usd",
                "economics.tvl_usd", "validators.delinquent_stake_pct",
                "economics.dex_volume_24h_usd")}
    (DOCS / "index.html").write_text(
        render_html.build(sections, findings, baseline, status, ts, history)
    )

    worst = findings[0]["severity"] if findings else "quiet"
    print(f"run #{baseline['runs']} ok · {len(ok)}/{len(status)} sources · "
          f"{len(findings)} finding(s) · worst: {worst}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
