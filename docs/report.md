# Heliograph

Solana state report · generated 2026-08-27 04:53 UTC · run #13 · baseline active

## What needs your attention

- 🟠 **TPS dropped to 3,309, 3.4 standard deviations below its recent norm of 4,118.**
  - evidence: baseline n=12, mean=4,118.2, current=3,309.3, z=-3.38
- 🔵 **Slot time dropped to 363 ms, 3.3 standard deviations below its recent norm of 366 ms.**
  - evidence: baseline n=12, mean=365.9, current=363.3, z=-3.29

## Network

The chain looks healthy: 3,309 TPS (1,427 non-vote) at 363.3 ms per slot, epoch 1023 is 21.36% done.

| metric | value |
|---|---|
| Health | ok |
| Slot | 442,028,275 |
| Block height | 420,076,578 |
| Epoch | 1023 (21.36% complete) |
| TPS (all / non-vote) | 3,309.3 / 1,427.3 |
| Slot time | 363.3 ms |
| Node version | 4.2.0 |

## Validators

686 validators are voting, 11 are delinquent (0.02% of stake, nothing alarming). It takes 18 validators to control a third of stake.

| metric | value |
|---|---|
| Active / delinquent | 686 / 11 |
| Delinquent stake | 0.02% |
| Total stake | 436,884,837 SOL |
| Nakamoto coefficient | 18 |
| Median commission | 5% |
| Median prioritization fee | 0 µlamports |

## Economics

A moving day: SOL at $100.9 (+4.3% 24h), $5.77B locked, $2.48B traded on DEXs.

| metric | value |
|---|---|
| SOL price | $100.9 (+4.3% 24h) |
| Market cap | $58.93B |
| TVL | $5.77B |
| DEX volume 24h | $2.48B (-15.5% 1d) |
| Chain fees 24h | $14.49M |
| Real economic value 24h | $6.02M |
| Stablecoin supply | $15.87B |

## Supply

| metric | value |
|---|---|
| Circulating | 584,062,999 SOL |
| Non-circulating | 48,906,816 SOL |
| Total | 632,969,815 SOL |

## Ecosystem

Cluster status: All Systems Operational.

Recent agave client releases:

- v4.3.0-beta.2 (pre-release) · 2026-08-21
- v4.3.0-beta.1 (pre-release) · 2026-08-21
- v4.2.1 · 2026-08-13
- v4.3.0-beta.0 (pre-release) · 2026-08-14
- v4.2.0 · 2026-08-07

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

---
*Heliograph reads Solana so you don't have to. The dashboard is plumbing; this page is the product.*
