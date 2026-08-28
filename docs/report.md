# Heliograph

Solana state report · generated 2026-08-28 22:59 UTC · run #35 · baseline active

## What needs your attention

- 🔵 **Slot time dropped to 318 ms, 44.3 standard deviations below its recent norm of 366 ms.**
  - evidence: baseline n=34, mean=365.5, current=317.9, z=-44.25
- 🔵 **DEX volume spiked to 3,700,129,858 USD, 5.4 standard deviations above its recent norm of 2,479,979,716 USD.**
  - evidence: baseline n=34, mean=2,479,979,715.8, current=3,700,129,858.0, z=+5.42
- 🔵 **Real economic value spiked to 7,533,724 USD, 4.1 standard deviations above its recent norm of 6,182,720 USD.**
  - evidence: baseline n=29, mean=6,182,719.8, current=7,533,724.0, z=+4.10

## Network

The chain looks healthy: 4,280 TPS (2,125 non-vote) at 317.9 ms per slot, epoch 1024 is 19.78% done.

| metric | value |
|---|---|
| Health | ok |
| Slot | 442,453,439 |
| Block height | 420,501,413 |
| Epoch | 1024 (19.78% complete) |
| TPS (all / non-vote) | 4,280.3 / 2,124.7 |
| Slot time | 317.9 ms |
| Node version | 4.2.1 |

## Validators

688 validators are voting, 9 are delinquent (0% of stake, nothing alarming). It takes 18 validators to control a third of stake.

| metric | value |
|---|---|
| Active / delinquent | 688 / 9 |
| Delinquent stake | 0.0% |
| Total stake | 436,134,289 SOL |
| Nakamoto coefficient | 18 |
| Median commission | 5% |
| Median prioritization fee | 0 µlamports |

## Economics

A moving day: SOL at $104.06 (-4.7% 24h), $5.83B locked, $3.70B traded on DEXs.

| metric | value |
|---|---|
| SOL price | $104.06 (-4.7% 24h) |
| Market cap | $60.79B |
| TVL | $5.83B |
| DEX volume 24h | $3.70B (+57.3% 1d) |
| Chain fees 24h | $16.30M |
| Real economic value 24h | $7.53M |
| Stablecoin supply | $15.89B |

## Supply

| metric | value |
|---|---|
| Circulating | 584,162,053 SOL |
| Non-circulating | 48,917,540 SOL |
| Total | 633,079,593 SOL |

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
