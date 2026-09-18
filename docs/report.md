# Heliograph

Solana state report · generated 2026-09-18 18:19 UTC · run #166 · baseline active

## What needs your attention

- 🟠 **SOL is up 10.8% in 24h to $112.42. Moves this size usually have a cause worth knowing.**
  - evidence: 24h change +10.8%, threshold warn>=8% crit>=15%
- 🟠 **Stablecoin supply dropped to 15,191,561,516 USD, 2.5 standard deviations below its recent norm of 15,931,272,575 USD.**
  - evidence: baseline n=165, mean=15,931,272,575.0, current=15,191,561,516.0, z=-2.53
- 🔵 **Slot time dropped to 268 ms, 2.7 standard deviations below its recent norm of 326 ms.**
  - evidence: baseline n=165, mean=325.6, current=268.1, z=-2.67
- 🔵 **TVL spiked to 6,166,004,311 USD, 3.9 standard deviations above its recent norm of 5,851,517,387 USD.**
  - evidence: baseline n=165, mean=5,851,517,386.9, current=6,166,004,311.0, z=+3.88

## Network

The chain looks healthy: 5,005 TPS (2,493 non-vote) at 268.1 ms per slot, epoch 1037 is 41.32% done.

| metric | value |
|---|---|
| Health | ok |
| Slot | 448,162,494 |
| Block height | 426,203,425 |
| Epoch | 1037 (41.32% complete) |
| TPS (all / non-vote) | 5,004.8 / 2,492.9 |
| Slot time | 268.1 ms |
| Node version | 4.3.0-rc.0 |

## Validators

676 validators are voting, 12 are delinquent (0.04% of stake, nothing alarming). It takes 18 validators to control a third of stake.

| metric | value |
|---|---|
| Active / delinquent | 676 / 12 |
| Delinquent stake | 0.04% |
| Total stake | 439,612,408 SOL |
| Nakamoto coefficient | 18 |
| Median commission | 5% |
| Median prioritization fee | 0 µlamports |

## Economics

A volatile day: SOL at $112.42 (+10.8% 24h), $6.17B locked, $2.59B traded on DEXs.

| metric | value |
|---|---|
| SOL price | $112.42 (+10.8% 24h) |
| Market cap | $66.02B |
| TVL | $6.17B |
| DEX volume 24h | $2.59B (-7.4% 1d) |
| Chain fees 24h | $14.68M |
| Real economic value 24h | $6.23M |
| Stablecoin supply | $15.19B |

## Supply

| metric | value |
|---|---|
| Circulating | 587,296,958 SOL |
| Non-circulating | 47,001,254 SOL |
| Total | 634,298,212 SOL |

## Ecosystem

Cluster status: All Systems Operational.

Daily active wallets: 2,677,019 (2026-09-16, via Dune).

Recent agave client releases:

- v4.4.0-alpha.5 (pre-release) · 2026-09-18
- v4.3.0 (pre-release) · 2026-09-18
- v4.3.0-rc.1 · 2026-09-11
- v4.4.0-alpha.4 (pre-release) · 2026-09-10
- v4.3.0-rc.0 · 2026-09-04

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
