"""The Dune collector's pure parts: row selection and timestamp parsing."""

import unittest

from heliograph.collect import _dune_ts, _latest_complete_day


ROWS = [
    {"activity_date": "2026-08-27 00:00:00.000 UTC", "daily_active_wallets": 1502959},
    {"activity_date": "2026-08-26 00:00:00.000 UTC", "daily_active_wallets": 2675872},
    {"activity_date": "2026-08-25 00:00:00.000 UTC", "daily_active_wallets": 2508175},
]


class LatestCompleteDay(unittest.TestCase):
    def test_skips_partial_execution_day(self):
        # executed on the 27th: that row is a partial day, the 26th is the answer
        day, wallets = _latest_complete_day(ROWS, "2026-08-27")
        self.assertEqual(day, "2026-08-26")
        self.assertEqual(wallets, 2675872)

    def test_stale_cache_still_yields_its_own_last_full_day(self):
        # cached execution from the 27th read days later: same answer, no
        # partial row can ever be promoted by the passage of wall-clock time
        day, wallets = _latest_complete_day(ROWS, "2026-08-27")
        self.assertEqual(day, "2026-08-26")
        self.assertEqual(wallets, 2675872)

    def test_all_rows_partial_or_empty(self):
        self.assertEqual(_latest_complete_day([], "2026-08-27"), (None, None))
        only_today = [ROWS[0]]
        self.assertEqual(_latest_complete_day(only_today, "2026-08-27"), (None, None))

    def test_null_value_rows_are_skipped(self):
        rows = [
            {"activity_date": "2026-08-26 00:00:00.000 UTC", "daily_active_wallets": None},
            {"activity_date": "2026-08-25 00:00:00.000 UTC", "daily_active_wallets": 2508175},
        ]
        day, wallets = _latest_complete_day(rows, "2026-08-27")
        self.assertEqual(day, "2026-08-25")
        self.assertEqual(wallets, 2508175)


class DuneTs(unittest.TestCase):
    def test_parses_nanosecond_iso(self):
        # 2026-08-27 08:50:23 UTC = 1787820623 (GNU date -u -d ... +%s)
        self.assertEqual(_dune_ts("2026-08-27T08:50:23.046832537Z"), 1787820623)

