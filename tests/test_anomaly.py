"""Anomaly math verified against hand-computed values (not the code's own)."""

import unittest

from heliograph import anomaly
from heliograph.render_html import nice_ticks
from heliograph.store import Store


class TestNiceTicks(unittest.TestCase):
    def test_round_hundred_span(self):
        # span 100 over ~4 ticks -> step 20: 0,20,40,60,80,100 by hand
        self.assertEqual(nice_ticks(0, 100), [0, 20, 40, 60, 80, 100])

    def test_tps_band(self):
        # span 400 -> step 100: 3900..4300 by hand
        self.assertEqual(nice_ticks(3900, 4300), [3900, 4000, 4100, 4200, 4300])

    def test_flat_input_widens(self):
        ticks = nice_ticks(5, 5)
        self.assertGreaterEqual(len(ticks), 2)
        self.assertTrue(all(4 <= t <= 6 for t in ticks))


class TestZScore(unittest.TestCase):
    def test_hand_computed(self):
        # mean 17, sample stdev sqrt(168/7)=4.898979; (2-17)/4.898979 = -3.0619
        history = [10, 12, 14, 16, 18, 20, 22, 24]
        self.assertAlmostEqual(anomaly.zscore(history, 2), -3.0619, places=3)

    def test_thin_baseline_is_silent(self):
        self.assertIsNone(anomaly.zscore([10] * 7, 100))

    def test_flat_baseline_is_silent(self):
        self.assertIsNone(anomaly.zscore([10] * 8, 100))


class TestAbsoluteRules(unittest.TestCase):
    def _analyze(self, sections):
        findings, _ = anomaly.analyze(sections, Store(":memory:"), ts=1)
        return {f["metric"]: f["severity"] for f in findings}

    def test_delinquent_stake_crit_over_10(self):
        out = self._analyze({"validators": {"delinquent_stake_pct": 12.0, "delinquent": 40}})
        self.assertEqual(out["validators.delinquent_stake_pct"], "crit")

    def test_delinquent_stake_warn_between_5_and_10(self):
        out = self._analyze({"validators": {"delinquent_stake_pct": 6.0, "delinquent": 20}})
        self.assertEqual(out["validators.delinquent_stake_pct"], "warn")

    def test_price_swing_warn_at_9pct(self):
        out = self._analyze({"economics": {"sol_price_usd": 100, "sol_24h_change_pct": -9.0}})
        self.assertEqual(out["economics.sol_price_usd"], "warn")

    def test_slow_slots_warn(self):
        out = self._analyze({"network": {"slot_time_ms": 700.0, "health": "ok"}})
        self.assertEqual(out["network.slot_time_ms"], "warn")

    def test_statuspage_incident_is_critical(self):
        out = self._analyze({"ecosystem": {
            "status_indicator": "major",
            "incidents": [{"name": "Cluster halt", "impact": "major", "status": "investigating"}],
        }})
        self.assertEqual(out["ecosystem.status"], "crit")

    def test_statuspage_minor_is_warning(self):
        out = self._analyze({"ecosystem": {"status_indicator": "minor", "incidents": []}})
        self.assertEqual(out["ecosystem.status"], "warn")

    def test_statuspage_operational_is_silent(self):
        out = self._analyze({"ecosystem": {"status_indicator": "none", "incidents": []}})
        self.assertEqual(out, {})

    def test_quiet_day_no_findings(self):
        out = self._analyze({
            "network": {"health": "ok", "slot_time_ms": 380.0},
            "validators": {"delinquent_stake_pct": 0.5},
            "economics": {"sol_price_usd": 100, "sol_24h_change_pct": 1.2},
        })
        self.assertEqual(out, {})


class TestRelativeRules(unittest.TestCase):
    def test_tps_collapse_flagged_against_own_history(self):
        store = Store(":memory:")
        # baseline mean 4000, sample stdev sqrt(45000/7)=80.18 -> z(1000) = -37.4
        for ts, tps in enumerate([4000, 4100, 3900, 4050, 3950, 4000, 4100, 3900], start=1):
            store.save(ts, {"network": {"tps": tps}})
        store.save(9, {"network": {"tps": 1000}})
        findings, baseline = anomaly.analyze({"network": {"tps": 1000}}, store, ts=9)
        by_metric = {f["metric"]: f for f in findings}
        self.assertIn("network.tps", by_metric)
        self.assertEqual(by_metric["network.tps"]["severity"], "warn")
        self.assertIn("dropped", by_metric["network.tps"]["headline"])
        self.assertEqual(baseline["status"], "active")

    def test_high_z_but_immaterial_move_stays_silent(self):
        # jitter baseline: mean 100.05, stdev 0.0535 -> z(100.4) ≈ 6.5,
        # but the move is 0.35% < 0.5% floor, so no finding
        store = Store(":memory:")
        for ts, v in enumerate([100.0, 100.1, 100.0, 100.1, 100.0, 100.1, 100.0, 100.1], start=1):
            store.save(ts, {"network": {"tps": v}})
        store.save(9, {"network": {"tps": 100.4}})
        findings, _ = anomaly.analyze({"network": {"tps": 100.4}}, store, ts=9)
        self.assertEqual([f for f in findings if f["metric"] == "network.tps"], [])

    def test_high_z_and_material_move_flagged(self):
        # same baseline, current 101: move 0.95% >= floor, z ≈ 17.8 -> flagged
        store = Store(":memory:")
        for ts, v in enumerate([100.0, 100.1, 100.0, 100.1, 100.0, 100.1, 100.0, 100.1], start=1):
            store.save(ts, {"network": {"tps": v}})
        store.save(9, {"network": {"tps": 101.0}})
        findings, _ = anomaly.analyze({"network": {"tps": 101.0}}, store, ts=9)
        self.assertTrue(any(f["metric"] == "network.tps" for f in findings))

    def test_steady_tps_stays_silent(self):
        store = Store(":memory:")
        for ts, tps in enumerate([4000, 4100, 3900, 4050, 3950, 4000, 4100, 3900, 4020], start=1):
            store.save(ts, {"network": {"tps": tps}})
        findings, _ = anomaly.analyze({"network": {"tps": 4020}}, store, ts=9)
        self.assertEqual([f for f in findings if f["metric"] == "network.tps"], [])


if __name__ == "__main__":
    unittest.main()
