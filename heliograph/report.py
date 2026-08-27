"""Markdown data story. The headline output: sentences first, tables second."""

from datetime import datetime, timezone

SEV_MARK = {"crit": "🔴", "warn": "🟠", "info": "🔵"}


def usd(n):
    if n is None:
        return "n/a"
    for div, suffix in ((1e12, "T"), (1e9, "B"), (1e6, "M"), (1e3, "K")):
        if abs(n) >= div:
            return f"${n / div:,.2f}{suffix}"
    return f"${n:,.0f}"


def build(sections, findings, baseline, status, ts):
    net = sections.get("network", {})
    val = sections.get("validators", {})
    eco = sections.get("economics", {})
    sup = sections.get("supply", {})
    eos = sections.get("ecosystem", {})
    when = datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    lines = [
        "# Heliograph",
        "",
        f"Solana state report · generated {when} · run #{baseline['runs']}"
        f" · baseline {baseline['status']}",
        "",
        "## What needs your attention",
        "",
    ]

    if findings:
        for f in findings:
            lines.append(f"- {SEV_MARK[f['severity']]} **{f['headline']}**")
            lines.append(f"  - evidence: {f['detail']}")
    else:
        lines.append(
            "Nothing. Every watched metric is inside its normal band. "
            "You can skip the rest of this report."
        )
    lines.append("")

    lines += [
        "## Network",
        "",
        _network_sentence(net),
        "",
        "| metric | value |",
        "|---|---|",
        f"| Health | {net.get('health', 'n/a')} |",
        f"| Slot | {_num(net.get('slot'))} |",
        f"| Block height | {_num(net.get('block_height'))} |",
        f"| Epoch | {net.get('epoch', 'n/a')} ({net.get('epoch_progress_pct', 'n/a')}% complete) |",
        f"| TPS (all / non-vote) | {_num(net.get('tps'))} / {_num(net.get('nonvote_tps'))} |",
        f"| Slot time | {net.get('slot_time_ms', 'n/a')} ms |",
        f"| Node version | {net.get('node_version', 'n/a')} |",
        "",
        "## Validators",
        "",
        _validator_sentence(val),
        "",
        "| metric | value |",
        "|---|---|",
        f"| Active / delinquent | {_num(val.get('active'))} / {_num(val.get('delinquent'))} |",
        f"| Delinquent stake | {val.get('delinquent_stake_pct', 'n/a')}% |",
        f"| Total stake | {_num(val.get('total_stake_sol'))} SOL |",
        f"| Nakamoto coefficient | {val.get('nakamoto_coefficient', 'n/a')} |",
        f"| Median commission | {val.get('median_commission', 'n/a')}% |",
        f"| Median prioritization fee | {_num(val.get('median_prioritization_fee_microlamports'))} µlamports |",
        "",
        "## Economics",
        "",
        _economics_sentence(eco),
        "",
        "| metric | value |",
        "|---|---|",
        f"| SOL price | ${_num(eco.get('sol_price_usd'))} ({_signed(eco.get('sol_24h_change_pct'))}% 24h) |",
        f"| Market cap | {usd(eco.get('market_cap_usd'))} |",
        f"| TVL | {usd(eco.get('tvl_usd'))} |",
        f"| DEX volume 24h | {usd(eco.get('dex_volume_24h_usd'))} ({_signed(eco.get('dex_volume_change_1d_pct'))}% 1d) |",
        f"| Chain fees 24h | {usd(eco.get('chain_fees_24h_usd'))} |",
        f"| Real economic value 24h | {usd(eco.get('rev_24h_usd'))} |",
        f"| Stablecoin supply | {usd(eco.get('stablecoin_supply_usd'))} |",
        "",
        "## Supply",
        "",
        f"| metric | value |",
        "|---|---|",
        f"| Circulating | {_num(sup.get('circulating_sol'))} SOL |",
        f"| Non-circulating | {_num(sup.get('non_circulating_sol'))} SOL |",
        f"| Total | {_num(sup.get('total_sol'))} SOL |",
        "",
        "## Ecosystem",
        "",
        f"Cluster status: {eos.get('status_description', 'unavailable this run')}.",
        "",
    ]
    if eos.get("daily_active_wallets") is not None:
        lines += [
            f"Daily active wallets: {_num(eos['daily_active_wallets'])}"
            f" ({eos.get('daily_active_wallets_date', 'n/a')}, via Dune).",
            "",
        ]
    lines += [
        "Recent agave client releases:",
        "",
    ]
    for r in eos.get("agave_releases", []):
        pre = " (pre-release)" if r["prerelease"] else ""
        lines.append(f"- {r['tag']}{pre} · {r['date']}")
    lines += ["", "Recently accepted SIMDs (upcoming protocol changes):", ""]
    for s in eos.get("recent_simds", []):
        lines.append(f"- {s['title']} · {s['date']}")
    lines += [
        "",
        "## Sources",
        "",
        "| source | status |",
        "|---|---|",
    ]
    for name, st in status.items():
        lines.append(f"| {name} | {st} |")
    lines += [
        "",
        "---",
        "*Heliograph reads Solana so you don't have to. The dashboard is plumbing;"
        " this page is the product.*",
        "",
    ]
    return "\n".join(lines)


def _num(n):
    return f"{n:,}" if isinstance(n, (int, float)) else "n/a"


def _signed(n):
    return f"{n:+.1f}" if isinstance(n, (int, float)) else "n/a"


def _network_sentence(net):
    tps, st = net.get("tps"), net.get("slot_time_ms")
    if tps is None:
        return "Network metrics were unavailable this run."
    verdict = "healthy" if (net.get("health") == "ok" and (st or 0) <= 600) else "degraded"
    return (
        f"The chain looks {verdict}: {tps:,.0f} TPS "
        f"({net.get('nonvote_tps') or 0:,.0f} non-vote) at {st} ms per slot, "
        f"epoch {net.get('epoch')} is {net.get('epoch_progress_pct')}% done."
    )


def _validator_sentence(val):
    if val.get("active") is None:
        return "Validator metrics were unavailable this run."
    dsp = val.get("delinquent_stake_pct") or 0
    tone = "nothing alarming" if dsp <= 5 else "worth watching"
    return (
        f"{val['active']:,} validators are voting, {val.get('delinquent', 0):,} are delinquent "
        f"({dsp}% of stake, {tone}). "
        f"It takes {val.get('nakamoto_coefficient')} validators to control a third of stake."
    )


def _economics_sentence(eco):
    if eco.get("sol_price_usd") is None:
        return "Price data was unavailable this run."
    chg = eco.get("sol_24h_change_pct") or 0
    mood = "quiet" if abs(chg) < 3 else ("moving" if abs(chg) < 8 else "volatile")
    return (
        f"A {mood} day: SOL at ${eco['sol_price_usd']:,} ({chg:+.1f}% 24h), "
        f"{usd(eco.get('tvl_usd'))} locked, {usd(eco.get('dex_volume_24h_usd'))} traded on DEXs."
    )
