# Heliograph

Solana state report · generated 2026-09-18 11:04 UTC · run #164 · baseline active

## What needs your attention

- 🟠 **Stablecoin supply dropped to 15,192,824,980 USD, 2.6 standard deviations below its recent norm of 15,940,416,399 USD.**
  - evidence: baseline n=163, mean=15,940,416,399.5, current=15,192,824,980.0, z=-2.65
- 🔵 **Slot time dropped to 266 ms, 2.9 standard deviations below its recent norm of 326 ms.**
  - evidence: baseline n=163, mean=326.3, current=266.0, z=-2.92

## Network

The chain looks healthy: 3,988 TPS (1,454 non-vote) at 266.0 ms per slot, epoch 1037 is 18.67% done.

| metric | value |
|---|---|
| Health | ok |
| Slot | 448,064,669 |
| Block height | 426,105,653 |
| Epoch | 1037 (18.67% complete) |
| TPS (all / non-vote) | 3,988.1 / 1,453.8 |
| Slot time | 266.0 ms |
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

A moving day: SOL at $106.18 (+6.2% 24h), $6.04B locked, $2.55B traded on DEXs.

| metric | value |
|---|---|
| SOL price | $106.18 (+6.2% 24h) |
| Market cap | $62.36B |
| TVL | $6.04B |
| DEX volume 24h | $2.55B (-8.8% 1d) |
| Chain fees 24h | $13.90M |
| Real economic value 24h | $5.64M |
| Stablecoin supply | $15.19B |

## Supply

| metric | value |
|---|---|
| Circulating | 587,297,289 SOL |
| Non-circulating | 47,001,254 SOL |
| Total | 634,298,543 SOL |

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
