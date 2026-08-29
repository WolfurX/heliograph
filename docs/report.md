# Heliograph

Solana state report · generated 2026-08-29 04:06 UTC · run #36 · baseline active

## What needs your attention

- 🔵 **Slot time dropped to 316 ms, 5.9 standard deviations below its recent norm of 364 ms.**
  - evidence: baseline n=35, mean=364.2, current=315.9, z=-5.94
- 🔵 **Stablecoin supply spiked to 15,926,070,103 USD, 2.7 standard deviations above its recent norm of 15,823,329,342 USD.**
  - evidence: baseline n=35, mean=15,823,329,342.5, current=15,926,070,103.0, z=+2.66

## Network

The chain looks healthy: 3,990 TPS (1,827 non-vote) at 315.9 ms per slot, epoch 1024 is 33.22% done.

| metric | value |
|---|---|
| Health | ok |
| Slot | 442,511,494 |
| Block height | 420,559,436 |
| Epoch | 1024 (33.22% complete) |
| TPS (all / non-vote) | 3,990.1 / 1,826.7 |
| Slot time | 315.9 ms |
| Node version | 4.2.1 |

## Validators

685 validators are voting, 12 are delinquent (0.04% of stake, nothing alarming). It takes 18 validators to control a third of stake.

| metric | value |
|---|---|
| Active / delinquent | 685 / 12 |
| Delinquent stake | 0.04% |
| Total stake | 436,134,289 SOL |
| Nakamoto coefficient | 18 |
| Median commission | 5% |
| Median prioritization fee | 0 µlamports |

## Economics

A quiet day: SOL at $103.85 (-2.9% 24h), $5.87B locked, $2.62B traded on DEXs.

| metric | value |
|---|---|
| SOL price | $103.85 (-2.9% 24h) |
| Market cap | $60.66B |
| TVL | $5.87B |
| DEX volume 24h | $2.62B (-29.3% 1d) |
| Chain fees 24h | $15.45M |
| Real economic value 24h | $6.46M |
| Stablecoin supply | $15.93B |

## Supply

| metric | value |
|---|---|
| Circulating | 584,161,860 SOL |
| Non-circulating | 48,917,540 SOL |
| Total | 633,079,400 SOL |

## Ecosystem

Cluster status: All Systems Operational.

Daily active wallets: 2,647,166 (2026-08-27, via Dune).

Recent agave client releases:

- v4.4.0-alpha.2 (pre-release) · 2026-08-28
- v4.3.0-beta.3 (pre-release) · 2026-08-28
- v4.2.2 (pre-release) · 2026-08-28
- v4.3.0-beta.2 (pre-release) · 2026-08-21
- v4.3.0-beta.1 (pre-release) · 2026-08-21

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
