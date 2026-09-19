# Heliograph

Solana state report · generated 2026-09-19 01:31 UTC · run #169 · baseline active

## What needs your attention

- 🟠 **SOL is up 11.4% in 24h to $113.36. Moves this size usually have a cause worth knowing.**
  - evidence: 24h change +11.4%, threshold warn>=8% crit>=15%
- 🔵 **Slot time dropped to 268 ms, 2.5 standard deviations below its recent norm of 325 ms.**
  - evidence: baseline n=168, mean=324.5, current=267.8, z=-2.50
- 🔵 **TVL spiked to 6,396,297,697 USD, 5.6 standard deviations above its recent norm of 5,858,468,305 USD.**
  - evidence: baseline n=168, mean=5,858,468,304.8, current=6,396,297,697.0, z=+5.61

## Network

The chain looks healthy: 4,537 TPS (2,020 non-vote) at 267.8 ms per slot, epoch 1037 is 63.74% done.

| metric | value |
|---|---|
| Health | ok |
| Slot | 448,259,366 |
| Block height | 426,300,237 |
| Epoch | 1037 (63.74% complete) |
| TPS (all / non-vote) | 4,537.3 / 2,020.1 |
| Slot time | 267.8 ms |
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

A volatile day: SOL at $113.36 (+11.4% 24h), $6.40B locked, $3.09B traded on DEXs.

| metric | value |
|---|---|
| SOL price | $113.36 (+11.4% 24h) |
| Market cap | $66.60B |
| TVL | $6.40B |
| DEX volume 24h | $3.09B (+19.0% 1d) |
| Chain fees 24h | $15.27M |
| Real economic value 24h | $6.10M |
| Stablecoin supply | $15.50B |

## Supply

| metric | value |
|---|---|
| Circulating | 587,296,639 SOL |
| Non-circulating | 47,001,249 SOL |
| Total | 634,297,889 SOL |

## Ecosystem

Cluster status: All Systems Operational.

Daily active wallets: 3,035,062 (2026-09-17, via Dune).

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
