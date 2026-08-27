"""Data collection. Every source is keyless and stdlib-only.

Each collector returns a dict of metrics or raises; collect_all() runs them
all, records per-source status, and never lets one failed source kill a run.
"""

import json
import urllib.request
import urllib.error

RPC_URL = "https://api.mainnet-beta.solana.com"
UA = "heliograph/1.0 (+https://github.com/WolfurX/heliograph)"
TIMEOUT = 20
LAMPORTS = 1_000_000_000


def _http_json(url, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(
        url,
        data=data,
        headers={"User-Agent": UA, "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return json.load(resp)


def _rpc(method, params=None):
    body = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params or []}
    out = _http_json(RPC_URL, body)
    if "error" in out:
        raise RuntimeError(f"RPC {method}: {out['error']}")
    return out["result"]


def collect_network():
    health = "ok"
    try:
        _rpc("getHealth")
    except Exception as e:  # getHealth returns an error object when unhealthy
        health = str(e)

    epoch = _rpc("getEpochInfo")
    samples = _rpc("getRecentPerformanceSamples", [12])
    version = _rpc("getVersion")

    secs = sum(s["samplePeriodSecs"] for s in samples)
    slots = sum(s["numSlots"] for s in samples)
    txs = sum(s["numTransactions"] for s in samples)
    nonvote = None
    if samples and "numNonVoteTransactions" in samples[0]:
        nonvote = sum(s["numNonVoteTransactions"] for s in samples)

    return {
        "health": health,
        "slot": epoch["absoluteSlot"],
        "block_height": epoch["blockHeight"],
        "epoch": epoch["epoch"],
        "epoch_progress_pct": round(100 * epoch["slotIndex"] / epoch["slotsInEpoch"], 2),
        "tx_count_total": epoch.get("transactionCount"),
        "tps": round(txs / secs, 1) if secs else None,
        "nonvote_tps": round(nonvote / secs, 1) if nonvote is not None and secs else None,
        "slot_time_ms": round(1000 * secs / slots, 1) if slots else None,
        "node_version": version.get("solana-core"),
    }


def collect_validators():
    va = _rpc("getVoteAccounts")
    current, delinquent = va["current"], va["delinquent"]
    cur_stake = sum(v["activatedStake"] for v in current)
    del_stake = sum(v["activatedStake"] for v in delinquent)
    total = cur_stake + del_stake

    ranked = sorted(current, key=lambda v: v["activatedStake"], reverse=True)
    nakamoto, acc = 0, 0
    for v in ranked:
        acc += v["activatedStake"]
        nakamoto += 1
        if acc > total / 3:
            break

    top = [
        {
            "vote_pubkey": v["votePubkey"],
            "stake_sol": round(v["activatedStake"] / LAMPORTS),
            "stake_pct": round(100 * v["activatedStake"] / total, 2),
            "commission": v["commission"],
        }
        for v in ranked[:10]
    ]

    fees = _rpc("getRecentPrioritizationFees")
    fee_values = sorted(f["prioritizationFee"] for f in fees) if fees else []
    median_fee = fee_values[len(fee_values) // 2] if fee_values else None

    commissions = sorted(v["commission"] for v in current)
    return {
        "active": len(current),
        "delinquent": len(delinquent),
        "delinquent_stake_pct": round(100 * del_stake / total, 2) if total else None,
        "total_stake_sol": round(total / LAMPORTS),
        "nakamoto_coefficient": nakamoto,
        "median_commission": commissions[len(commissions) // 2] if commissions else None,
        "median_prioritization_fee_microlamports": median_fee,
        "top_by_stake": top,
    }


def collect_supply():
    supply = _rpc("getSupply", [{"excludeNonCirculatingAccountsList": True}])["value"]
    return {
        "total_sol": round(supply["total"] / LAMPORTS),
        "circulating_sol": round(supply["circulating"] / LAMPORTS),
        "non_circulating_sol": round(supply["nonCirculating"] / LAMPORTS),
    }


def collect_price():
    out = _http_json(
        "https://api.coingecko.com/api/v3/simple/price"
        "?ids=solana&vs_currencies=usd&include_24hr_change=true"
        "&include_market_cap=true&include_24hr_vol=true"
    )
    sol = out["solana"]
    return {
        "sol_price_usd": sol["usd"],
        "sol_24h_change_pct": round(sol.get("usd_24h_change", 0), 2),
        "market_cap_usd": round(sol.get("usd_market_cap", 0)),
        "volume_24h_usd": round(sol.get("usd_24h_vol", 0)),
    }


def collect_tvl():
    chains = _http_json("https://api.llama.fi/v2/chains")
    solana = next(c for c in chains if c["name"] == "Solana")
    return {"tvl_usd": round(solana["tvl"])}


def collect_dex_volume():
    out = _http_json(
        "https://api.llama.fi/overview/dexs/solana"
        "?excludeTotalDataChart=true&excludeTotalDataChartBreakdown=true"
    )
    return {
        "dex_volume_24h_usd": round(out["total24h"]),
        "dex_volume_change_1d_pct": round(out["change_1d"], 2) if out.get("change_1d") is not None else None,
    }


def collect_chain_fees():
    out = _http_json(
        "https://api.llama.fi/overview/fees/solana"
        "?excludeTotalDataChart=true&excludeTotalDataChartBreakdown=true&dataType=dailyFees"
    )
    return {"chain_fees_24h_usd": round(out["total24h"])}


def collect_stablecoins():
    out = _http_json("https://stablecoins.llama.fi/stablecoinchains")
    solana = next(c for c in out if c["name"] == "Solana")
    return {"stablecoin_supply_usd": round(solana["totalCirculatingUSD"]["peggedUSD"])}


SOURCES = {
    "solana_rpc_network": collect_network,
    "solana_rpc_validators": collect_validators,
    "solana_rpc_supply": collect_supply,
    "coingecko": collect_price,
    "defillama_tvl": collect_tvl,
    "defillama_dex": collect_dex_volume,
    "defillama_fees": collect_chain_fees,
    "defillama_stablecoins": collect_stablecoins,
}

SECTION_OF = {
    "solana_rpc_network": "network",
    "solana_rpc_validators": "validators",
    "solana_rpc_supply": "supply",
    "coingecko": "economics",
    "defillama_tvl": "economics",
    "defillama_dex": "economics",
    "defillama_fees": "economics",
    "defillama_stablecoins": "economics",
}


def collect_all():
    """Run every collector; return (sections, source_status)."""
    sections = {"network": {}, "validators": {}, "supply": {}, "economics": {}}
    status = {}
    for name, fn in SOURCES.items():
        try:
            sections[SECTION_OF[name]].update(fn())
            status[name] = "ok"
        except Exception as e:
            status[name] = f"error: {e}"
    return sections, status
