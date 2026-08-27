"""History persistence: sqlite, committed to the repo so GitHub Actions runs
share one growing baseline without external storage."""

import json
import sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS snapshots (
    ts INTEGER PRIMARY KEY,
    body TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS metrics (
    ts INTEGER NOT NULL,
    name TEXT NOT NULL,
    value REAL NOT NULL,
    PRIMARY KEY (ts, name)
);
CREATE TABLE IF NOT EXISTS findings (
    ts INTEGER NOT NULL,
    metric TEXT NOT NULL,
    severity TEXT NOT NULL,
    headline TEXT NOT NULL,
    detail TEXT NOT NULL,
    PRIMARY KEY (ts, metric)
);
"""

# flat numeric series worth baselining, as section.key paths
TRACKED = [
    "network.tps",
    "network.nonvote_tps",
    "network.slot_time_ms",
    "validators.delinquent_stake_pct",
    "validators.active",
    "validators.delinquent",
    "validators.nakamoto_coefficient",
    "economics.sol_price_usd",
    "economics.tvl_usd",
    "economics.dex_volume_24h_usd",
    "economics.chain_fees_24h_usd",
    "economics.rev_24h_usd",
    "economics.stablecoin_supply_usd",
    "supply.circulating_sol",
]


class Store:
    def __init__(self, path):
        self.db = sqlite3.connect(path)
        self.db.executescript(SCHEMA)

    def save(self, ts, sections):
        self.db.execute(
            "INSERT OR REPLACE INTO snapshots (ts, body) VALUES (?, ?)",
            (ts, json.dumps(sections)),
        )
        for path in TRACKED:
            section, key = path.split(".")
            value = sections.get(section, {}).get(key)
            if isinstance(value, (int, float)):
                self.db.execute(
                    "INSERT OR REPLACE INTO metrics (ts, name, value) VALUES (?, ?, ?)",
                    (ts, path, float(value)),
                )
        self.db.commit()

    def series(self, name, limit=200):
        """Most recent `limit` points, oldest first: [(ts, value), ...]."""
        rows = self.db.execute(
            "SELECT ts, value FROM metrics WHERE name = ? ORDER BY ts DESC LIMIT ?",
            (name, limit),
        ).fetchall()
        return rows[::-1]

    def run_count(self):
        return self.db.execute("SELECT COUNT(*) FROM snapshots").fetchone()[0]

    def save_findings(self, ts, findings):
        for f in findings:
            self.db.execute(
                "INSERT OR REPLACE INTO findings (ts, metric, severity, headline, detail)"
                " VALUES (?, ?, ?, ?, ?)",
                (ts, f["metric"], f["severity"], f["headline"], f["detail"]),
            )
        self.db.commit()

    def recent_findings(self, limit=20):
        """Newest first: [(ts, metric, severity, headline, detail), ...]."""
        return self.db.execute(
            "SELECT ts, metric, severity, headline, detail FROM findings"
            " ORDER BY ts DESC LIMIT ?", (limit,)
        ).fetchall()
