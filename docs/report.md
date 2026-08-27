# Heliograph

Solana state report · generated 2026-08-27 14:07 UTC · run #27 · baseline active

## What needs your attention

- 🟠 **SOL is up 9.8% in 24h to $106.33. Moves this size usually have a cause worth knowing.**
  - evidence: 24h change +9.8%, threshold warn>=8% crit>=15%
- 🔵 **TPS spiked to 5,166, 3.5 standard deviations above its recent norm of 3,839.**
  - evidence: baseline n=26, mean=3,838.8, current=5,166.4, z=+3.51

## Network

The chain looks healthy: 5,166 TPS (3,287 non-vote) at 364.2 ms per slot, epoch 1023 is 42.47% done.

| metric | value |
|---|---|
| Health | ok |
| Slot | 442,119,478 |
| Block height | 420,167,741 |
| Epoch | 1023 (42.47% complete) |
| TPS (all / non-vote) | 5,166.4 / 3,287.3 |
| Slot time | 364.2 ms |
| Node version | 4.2.0 |

## Validators

687 validators are voting, 10 are delinquent (0.02% of stake, nothing alarming). It takes 18 validators to control a third of stake.

| metric | value |
|---|---|
| Active / delinquent | 687 / 10 |
| Delinquent stake | 0.02% |
| Total stake | 436,884,837 SOL |
| Nakamoto coefficient | 18 |
| Median commission | 5% |
| Median prioritization fee | 0 µlamports |

## Economics

A volatile day: SOL at $106.33 (+9.8% 24h), $5.89B locked, $2.35B traded on DEXs.

| metric | value |
|---|---|
| SOL price | $106.33 (+9.8% 24h) |
| Market cap | $62.10B |
| TVL | $5.89B |
| DEX volume 24h | $2.35B (-19.9% 1d) |
| Chain fees 24h | $15.17M |
| Real economic value 24h | $6.28M |
| Stablecoin supply | $15.80B |

## Supply

| metric | value |
|---|---|
| Circulating | 584,062,685 SOL |
| Non-circulating | 48,906,816 SOL |
| Total | 632,969,501 SOL |

## Ecosystem

Cluster status: All Systems Operational.

Daily active wallets: 2,676,760 (2026-08-26, via Dune).

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
| dune_active_wallets | ok |

---
*Heliograph reads Solana so you don't have to. The dashboard is plumbing; this page is the product.*
