# Heliograph

A heliograph is a signaling instrument: a mirror that flashes sunlight at you when someone has something to say. This one watches Solana and flashes when something matters.

**Live:** [wolfurx.github.io/heliograph](https://wolfurx.github.io/heliograph/) · [Markdown report](https://wolfurx.github.io/heliograph/report.md) · [JSON](https://wolfurx.github.io/heliograph/data.json)

## Why it looks like this

Most entries in this category will be dashboards: a grid of tiles you are supposed to open, scan, and interpret yourself. I think that model is backwards, and I wrote up the argument before this bounty existed: [The Death of the Dashboard](https://x.com/0xWolfur/status/2079386541122802084). The short version: a dashboard is a set of questions somebody froze in place, and interpretation is the hard part it leaves to you. The product was never the chart. It was the answer.

So Heliograph inverts the usual shape. Every run leads with a verdict: **"N things need your attention"**, followed by the findings as plain sentences with the evidence attached. On a quiet day it says so in one line and tells you to close the tab. The dashboard still exists, and it is a good one, but it is the supporting evidence, not the product.

## What it reads

Everything is keyless and free. No API keys, no accounts, no dependencies beyond the Python standard library.

| Source | What it provides |
|---|---|
| Solana RPC (`api.mainnet-beta.solana.com`) | health, slot, epoch progress, TPS and slot time (performance samples), validator set and stake distribution, prioritization fees, supply |
| CoinGecko public API | SOL price, 24h change, market cap, spot volume |
| DeFiLlama | chain TVL, DEX volume, chain fees, stablecoin supply |

A failed source never kills a run. Each collector is isolated; whatever fails is reported in the Sources table of every output, and the rest of the report is built from what succeeded.

## What it produces

Each run regenerates three views of the same snapshot in `docs/`:

- `index.html`: the interactive dark dashboard (verdict, findings, stat tiles with sparklines and hover detail, full metric tables)
- `report.md`: the human report, sentences first, tables second
- `data.json`: stable machine-readable schema, versioned, for anyone who wants to build on top or point their own agent at it

## Anomaly detection

Two layers, because a rule that works on day one and a rule that knows what "normal" looks like are different things:

Absolute rules fire from the first run: cluster health, slot time above 600 ms, delinquent stake above 5% (critical above 10%), SOL moving more than 8% in a day.

Relative rules compare each metric against this repo's own accumulated history using z-scores (flag at 2.5 standard deviations). They stay silent until 8 prior data points exist, then tune themselves as the baseline grows. TPS, slot time, delinquent stake, TVL, DEX volume, and stablecoin supply are tracked this way.

Every finding carries its evidence: baseline size, mean, current value, z-score. The report tells you what it thinks and shows you why, and you decide.

The history lives in a sqlite database committed to the repo (`data/heliograph.db`). That is a deliberate trick: GitHub Actions runs are stateless, but the repo itself is not, so every scheduled run inherits the full baseline without any external storage.

## Automation

A GitHub Actions workflow (`.github/workflows/pulse.yml`) runs every 30 minutes: collect, analyze, render, commit, push. GitHub Pages serves `docs/`, so the push is also the deploy. The commit history doubles as an audit log of every pulse the agent has taken.

To change the interval, edit the cron line in the workflow. To pause it, disable the workflow. That is the whole operational surface.

## Run it yourself

```
git clone https://github.com/WolfurX/heliograph
cd heliograph
python3 -m heliograph
```

Python 3.9 or later, nothing to install. One run takes a few seconds and writes the three outputs to `docs/`. Run it on any schedule you like; the baseline builds wherever the sqlite file lives.

Tests cover the anomaly math with hand-computed expected values:

```
python3 -m unittest discover -s tests
```

## Reading the output

- The number at the top is the whole report. Zero means nothing is outside its normal band and you are done.
- Findings are ordered by severity (critical, warning, info) and each states its threshold or baseline so you can disagree with it.
- "Baseline forming" in the header means the z-score rules are still collecting history and only the absolute rules are active.
