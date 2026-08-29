# Heliograph

Solana state report · generated 2026-08-29 11:01 UTC · run #37 · baseline active

## What needs your attention

- 🔵 **Slot time dropped to 316 ms, 4.1 standard deviations below its recent norm of 363 ms.**
  - evidence: baseline n=36, mean=362.8, current=316.2, z=-4.11
- 🔵 **Stablecoin supply spiked to 15,952,317,887 USD, 3.0 standard deviations above its recent norm of 15,826,183,252 USD.**
  - evidence: baseline n=36, mean=15,826,183,252.5, current=15,952,317,887.0, z=+3.02

## Network

The chain looks healthy: 3,233 TPS (1,068 non-vote) at 316.2 ms per slot, epoch 1024 is 51.41% done.

| metric | value |
|---|---|
| Health | ok |
| Slot | 442,590,076 |
| Block height | 420,637,974 |
| Epoch | 1024 (51.41% complete) |
| TPS (all / non-vote) | 3,232.8 / 1,067.7 |
| Slot time | 316.2 ms |
| Node version | 4.2.1 |

## Validators

689 validators are voting, 8 are delinquent (0% of stake, nothing alarming). It takes 18 validators to control a third of stake.

| metric | value |
|---|---|
| Active / delinquent | 689 / 8 |
| Delinquent stake | 0.0% |
| Total stake | 436,134,289 SOL |
| Nakamoto coefficient | 18 |
| Median commission | 5% |
| Median prioritization fee | 0 µlamports |

## Economics

A quiet day: SOL at $103.51 (-2.5% 24h), $5.85B locked, $2.59B traded on DEXs.

| metric | value |
|---|---|
| SOL price | $103.51 (-2.5% 24h) |
| Market cap | $60.47B |
| TVL | $5.85B |
| DEX volume 24h | $2.59B (-30.0% 1d) |
| Chain fees 24h | $15.47M |
| Real economic value 24h | $6.46M |
| Stablecoin supply | $15.95B |

## Supply

| metric | value |
|---|---|
| Circulating | 584,161,629 SOL |
| Non-circulating | 48,917,540 SOL |
| Total | 633,079,169 SOL |

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
