# Heliograph

Solana state report · generated 2026-09-18 05:49 UTC · run #163 · baseline active

## What needs your attention

- 🟠 **Stablecoin supply dropped to 15,226,738,274 USD, 2.6 standard deviations below its recent norm of 15,944,821,820 USD.**
  - evidence: baseline n=162, mean=15,944,821,820.0, current=15,226,738,274.0, z=-2.59
- 🔵 **Slot time dropped to 268 ms, 2.9 standard deviations below its recent norm of 327 ms.**
  - evidence: baseline n=162, mean=326.7, current=268.0, z=-2.91

## Network

The chain looks healthy: 4,266 TPS (1,751 non-vote) at 268.0 ms per slot, epoch 1037 is 2.19% done.

| metric | value |
|---|---|
| Health | ok |
| Slot | 447,993,474 |
| Block height | 426,034,504 |
| Epoch | 1037 (2.19% complete) |
| TPS (all / non-vote) | 4,265.7 / 1,750.6 |
| Slot time | 268.0 ms |
| Node version | 4.3.0-rc.0 |

## Validators

677 validators are voting, 11 are delinquent (0.04% of stake, nothing alarming). It takes 18 validators to control a third of stake.

| metric | value |
|---|---|
| Active / delinquent | 677 / 11 |
| Delinquent stake | 0.04% |
| Total stake | 439,612,408 SOL |
| Nakamoto coefficient | 18 |
| Median commission | 5% |
| Median prioritization fee | 0 µlamports |

## Economics

A moving day: SOL at $105.39 (+5.9% 24h), $5.97B locked, $2.55B traded on DEXs.

| metric | value |
|---|---|
| SOL price | $105.39 (+5.9% 24h) |
| Market cap | $61.93B |
| TVL | $5.97B |
| DEX volume 24h | $2.55B (-8.8% 1d) |
| Chain fees 24h | $13.89M |
| Real economic value 24h | $5.64M |
| Stablecoin supply | $15.23B |

## Supply

| metric | value |
|---|---|
| Circulating | 587,297,769 SOL |
| Non-circulating | 47,000,977 SOL |
| Total | 634,298,746 SOL |

## Ecosystem

Cluster status: All Systems Operational.

Daily active wallets: 2,677,019 (2026-09-16, via Dune).

Recent agave client releases:

- v4.3.0-rc.1 · 2026-09-11
- v4.4.0-alpha.4 (pre-release) · 2026-09-10
- v4.3.0-rc.0 · 2026-09-04
- v4.4.0-alpha.3 (pre-release) · 2026-09-03
- v4.4.0-alpha.2 (pre-release) · 2026-08-28

Recently accepted SIMDs (upcoming protocol changes):


## Sources

| source | status |
|---|---|
| solana_rpc_network | ok |
| solana_rpc_validators | ok |
| solana_rpc_supply | ok |
| coingecko | ok |
| defillama_tvl | ok |
| defillama_dex | ok |
| defillama_fees | ok |
| defillama_stablecoins | ok |
| defillama_rev | ok |
| solana_statuspage | ok |
| github_agave_releases | ok |
| github_simds | ok |
| dune_active_wallets | ok |

---
*Heliograph reads Solana so you don't have to. The dashboard is plumbing; this page is the product.*
