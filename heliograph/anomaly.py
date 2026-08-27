"""Anomaly detection: the part a dashboard makes the human do by eye.

Two kinds of rules:
- absolute: thresholds that are meaningful from the very first run
  (delinquent stake, slot time, price swings, RPC health)
- relative: z-scores against this repo's own accumulated history;
  silent until MIN_BASELINE prior points exist, then self-tuning.

A finding is a judgment, not a chart: severity, one headline sentence,
and the evidence that backs it.
"""

import statistics

MIN_BASELINE = 8  # prior points needed before z-score rules speak
Z_FLAG = 2.5
MIN_REL_CHANGE = 0.005  # z alone is not enough: a near-flat baseline makes
                        # microscopic wiggles score huge z; the move must
                        # also be >= 0.5% away from the mean to matter


def zscore(history, current):
    """z of `current` against `history` (list of floats, current excluded).
    None when the baseline is too thin or flat to judge against."""
    if len(history) < MIN_BASELINE:
        return None
    mean = statistics.fmean(history)
    stdev = statistics.stdev(history)
    if stdev == 0:
        return None
    return (current - mean) / stdev


def _finding(severity, metric, headline, detail):
    return {"severity": severity, "metric": metric, "headline": headline, "detail": detail}


def _relative(findings, store, ts, metric, label, unit="", down_is_bad=True):
    pts = [v for t, v in store.series(metric) if t != ts]
    cur = next((v for t, v in store.series(metric) if t == ts), None)
    if cur is None:
        return
    z = zscore(pts, cur)
    if z is None or abs(z) < Z_FLAG:
        return
    mean_ = statistics.fmean(pts)
    if mean_ != 0 and abs(cur - mean_) / abs(mean_) < MIN_REL_CHANGE:
        return
    direction = "dropped" if z < 0 else "spiked"
    bad = (z < 0) == down_is_bad
    sev = "warn" if bad else "info"
    mean = statistics.fmean(pts)
    findings.append(_finding(
        sev, metric,
        f"{label} {direction} to {cur:,.0f}{unit}, {abs(z):.1f} standard deviations "
        f"{'below' if z < 0 else 'above'} its recent norm of {mean:,.0f}{unit}.",
        f"baseline n={len(pts)}, mean={mean:,.1f}, current={cur:,.1f}, z={z:+.2f}",
    ))


def analyze(sections, store, ts):
    """Return (findings, baseline_status)."""
    findings = []
    net = sections.get("network", {})
    val = sections.get("validators", {})
    eco = sections.get("economics", {})
    eos = sections.get("ecosystem", {})

    # --- absolute rules ---
    indicator = eos.get("status_indicator")
    if indicator and indicator != "none":
        sev = "warn" if indicator == "minor" else "crit"
        names = ", ".join(i["name"] for i in eos.get("incidents", [])) or "unnamed incident"
        findings.append(_finding(
            sev, "ecosystem.status",
            f"The Solana status page reports an active incident: {names}. "
            f"That is the operators talking; treat every other metric here in that light.",
            f"status.solana.com indicator={indicator}, "
            f"{len(eos.get('incidents', []))} open incident(s)",
        ))

    if net.get("health") not in (None, "ok"):
        findings.append(_finding(
            "crit", "network.health",
            "The RPC node reports the cluster as unhealthy. Verify on a second source before acting.",
            f"getHealth: {net['health']}",
        ))

    st = net.get("slot_time_ms")
    if st is not None and st > 600:
        findings.append(_finding(
            "warn", "network.slot_time_ms",
            f"Slots are averaging {st:.0f} ms against a 400 ms target. Block production is straining.",
            f"mean over recent performance samples: {st} ms",
        ))

    dsp = val.get("delinquent_stake_pct")
    if dsp is not None and dsp > 5:
        sev = "crit" if dsp > 10 else "warn"
        findings.append(_finding(
            sev, "validators.delinquent_stake_pct",
            f"{dsp:.1f}% of stake is delinquent ({val.get('delinquent')} validators offline). "
            f"Above 33% the cluster halts; this deserves a look now, not later.",
            f"delinquent stake {dsp}%, threshold warn>5% crit>10%",
        ))

    chg = eco.get("sol_24h_change_pct")
    if chg is not None and abs(chg) >= 8:
        sev = "crit" if abs(chg) >= 15 else "warn"
        word = "down" if chg < 0 else "up"
        findings.append(_finding(
            sev, "economics.sol_price_usd",
            f"SOL is {word} {abs(chg):.1f}% in 24h to ${eco.get('sol_price_usd'):,}. "
            f"Moves this size usually have a cause worth knowing.",
            f"24h change {chg:+.1f}%, threshold warn>=8% crit>=15%",
        ))

    # --- relative rules (need accumulated baseline) ---
    _relative(findings, store, ts, "network.tps", "TPS")
    _relative(findings, store, ts, "network.slot_time_ms", "Slot time", " ms", down_is_bad=False)
    _relative(findings, store, ts, "validators.delinquent_stake_pct", "Delinquent stake", "%", down_is_bad=False)
    _relative(findings, store, ts, "economics.tvl_usd", "TVL", " USD")
    _relative(findings, store, ts, "economics.stablecoin_supply_usd", "Stablecoin supply", " USD")
    _relative(findings, store, ts, "economics.dex_volume_24h_usd", "DEX volume", " USD")
    _relative(findings, store, ts, "economics.rev_24h_usd", "Real economic value", " USD")

    order = {"crit": 0, "warn": 1, "info": 2}
    findings.sort(key=lambda f: order[f["severity"]])

    runs = store.run_count()
    baseline = {
        "runs": runs,
        "status": "active" if runs > MIN_BASELINE else f"forming ({runs}/{MIN_BASELINE + 1} runs)",
    }
    return findings, baseline
