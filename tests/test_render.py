"""The stake donut's pure parts: arc geometry and slice assembly."""

import unittest

from heliograph.render_html import _arcpath, stakepie


class StakePie(unittest.TestCase):
    VAL = {
        "top_by_stake": [
            {"vote_pubkey": "A" * 44, "stake_sol": 100, "stake_pct": 10.0, "commission": 5},
            {"vote_pubkey": "B" * 44, "stake_sol": 50, "stake_pct": 5.0, "commission": 0},
        ],
        "total_stake_sol": 1000, "active": 100,
    }

    def test_arcpath_quarter_circle(self):
        # 0deg is 12 o'clock (160,10); 90deg is 3 o'clock (310,160) - by hand
        d = _arcpath(160, 160, 150, 96, 0, 90)
        self.assertTrue(d.startswith("M160.00 10.00A150 150 0 0 1 310.00 160.00"))

    def test_arcpath_large_flag(self):
        self.assertIn(" 1 1 ", _arcpath(160, 160, 150, 96, 0, 200).split("A")[1])

    def test_slice_count_and_center(self):
        out = stakepie(self.VAL)
        self.assertEqual(out.count('class="pslice"'), 3)  # 2 ranks + everyone else
        self.assertIn(">15.0%<", out)                     # 10 + 5, by hand
        self.assertIn("all other validators (98)", out)
        self.assertIn("850 SOL", out)                     # 1000 - 150, by hand

    def test_no_validators(self):
        self.assertIn("unavailable", stakepie({"top_by_stake": []}))
