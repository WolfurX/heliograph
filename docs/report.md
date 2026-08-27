# Heliograph

Solana state report · generated 2026-08-27 09:04 UTC · run #18 · baseline active

## What needs your attention

- 🟠 **Delinquent stake spiked to 0%, 3.2 standard deviations above its recent norm of 0%.**
  - evidence: baseline n=17, mean=0.0, current=0.1, z=+3.16

## Network

The chain looks healthy: 3,495 TPS (1,618 non-vote) at 364.6 ms per slot, epoch 1023 is 30.93% done.

| metric | value |
|---|---|
| Health | ok |
| Slot | 442,069,633 |
| Block height | 420,117,908 |
| Epoch | 1023 (30.93% complete) |
| TPS (all / non-vote) | 3,494.6 / 1,618.3 |
| Slot time | 364.6 ms |
| Node version | 4.2.0 |

## Validators

686 validators are voting, 11 are delinquent (0.09% of stake, nothing alarming). It takes 18 validators to control a third of stake.

| metric | value |
|---|---|
| Active / delinquent | 686 / 11 |
| Delinquent stake | 0.09% |
| Total stake | 436,884,837 SOL |
| Nakamoto coefficient | 18 |
| Median commission | 5% |
| Median prioritization fee | 0 µlamports |

## Economics

A moving day: SOL at $104.49 (+7.8% 24h), $5.78B locked, $2.48B traded on DEXs.

| metric | value |
|---|---|
| SOL price | $104.49 (+7.8% 24h) |
| Market cap | $60.97B |
| TVL | $5.78B |
| DEX volume 24h | $2.48B (-15.5% 1d) |
| Chain fees 24h | $14.92M |
| Real economic value 24h | $6.19M |
| Stablecoin supply | $15.80B |

## Supply

| metric | value |
|---|---|
| Circulating | 584,062,866 SOL |
| Non-circulating | 48,906,816 SOL |
| Total | 632,969,682 SOL |

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

- SIMD-0553: Resource and Inclusion Fee · 2026-07-20
- SIMD-0550: Double disinflation · 2026-07-23
- re-amend SIMD-0340: additional inter- and intra- validation · 2026-07-31
- SIMD-0433: Loader V3: Set Program Data to ELF Length · 2026-07-31
- SIMD-0266: Efficient Token program · 2026-03-13

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
