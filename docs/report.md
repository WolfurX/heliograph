# Heliograph

Solana state report · generated 2026-09-18 14:56 UTC · run #165 · baseline active

## What needs your attention

- 🟠 **SOL is up 9.3% in 24h to $110.7. Moves this size usually have a cause worth knowing.**
  - evidence: 24h change +9.3%, threshold warn>=8% crit>=15%
- 🟠 **Stablecoin supply dropped to 15,179,276,791 USD, 2.6 standard deviations below its recent norm of 15,935,857,915 USD.**
  - evidence: baseline n=164, mean=15,935,857,915.2, current=15,179,276,791.0, z=-2.63
- 🔵 **TPS spiked to 5,273, 3.1 standard deviations above its recent norm of 3,895.**
  - evidence: baseline n=164, mean=3,894.6, current=5,272.9, z=+3.12
- 🔵 **Slot time dropped to 267 ms, 2.8 standard deviations below its recent norm of 326 ms.**
  - evidence: baseline n=164, mean=325.9, current=266.8, z=-2.80

## Network

The chain looks healthy: 5,273 TPS (2,750 non-vote) at 266.8 ms per slot, epoch 1037 is 30.73% done.

| metric | value |
|---|---|
| Health | ok |
| Slot | 448,116,732 |
| Block height | 426,157,679 |
| Epoch | 1037 (30.73% complete) |
| TPS (all / non-vote) | 5,272.9 / 2,749.6 |
| Slot time | 266.8 ms |
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

A volatile day: SOL at $110.7 (+9.3% 24h), $6.05B locked, $2.59B traded on DEXs.

| metric | value |
|---|---|
| SOL price | $110.7 (+9.3% 24h) |
| Market cap | $65.01B |
| TVL | $6.05B |
| DEX volume 24h | $2.59B (-7.4% 1d) |
| Chain fees 24h | $14.68M |
| Real economic value 24h | $6.23M |
| Stablecoin supply | $15.18B |

## Supply

| metric | value |
|---|---|
| Circulating | 587,297,121 SOL |
| Non-circulating | 47,001,254 SOL |
| Total | 634,298,375 SOL |

## Ecosystem

Cluster status: All Systems Operational.

Daily active wallets: 2,677,019 (2026-09-16, via Dune).

Recent agave client releases:

- v4.3.0 (pre-release) · 2026-09-18
- v4.3.0-rc.1 · 2026-09-11
- v4.4.0-alpha.4 (pre-release) · 2026-09-10
- v4.3.0-rc.0 · 2026-09-04
- v4.4.0-alpha.3 (pre-release) · 2026-09-03

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
