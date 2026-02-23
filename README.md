# Pendle API Explorer

**Institutional-grade data pipeline tracking the top 10 Pendle Finance pools by Total Value Locked (TVL) across all supported chains**

> Period: June 2025 → February 2026 | Daily snapshots | 10 chains | 132 active markets

---

## About this project

This project is an open-source pipeline for extracting, analysing and visualising market data from Pendle Finance's public API. Built as a case study in institutional DeFi research, it fetches live and historical TVL across all 10 supported chains, ranks markets dynamically, and produces an animated bar chart race documenting capital flow evolution over time.

---

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/OnchainResearch/pendle-api-explorer
cd pendle-api-explorer

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Ensure ffmpeg is installed (required for video export)
# Ubuntu: sudo apt install ffmpeg
# macOS:  brew install ffmpeg

# 4. Run the full pipeline
python pendle_fetcher.py     # Phase 1: Fetch markets and historical TVL
python pendle_analysis.py    # Phase 2: Compute top 10 per day
python pendle_chart.py       # Phase 3: Render and export animation
```

---

## Architecture

```
pendle-api-explorer/
├── config.py                # Chain IDs and API constants
├── pendle_fetcher.py        # Phase 1: Market discovery + TVL history collection
├── pendle_analysis.py       # Phase 2: Ranking and top 10 computation
├── pendle_chart.py          # Phase 3: Animated bar chart race
├── requirements.txt         # Python dependencies
├── pendle_markets.csv       # All active markets snapshot (132 markets on 2026-02-22)
├── pendle_history.csv       # Daily TVL history — long format (12,815 rows)
├── pendle_top10_history.csv # Top 10 markets per day — analysis-ready
├── pendle_top10_race.mp4    # Final animated output
└── notes.md                 # Journal documenting progression
```

---

## API Endpoints Used

**Chain discovery:**
```
GET https://api-v2.pendle.finance/core/v1/chains
```
Returns all supported chain IDs. Used to dynamically build the chain list rather than hardcoding.

**Market discovery (per chain):**
```
GET https://api-v2.pendle.finance/core/v1/{chainId}/markets?limit=100&skip={n}
```
Paginated endpoint returning market metadata including address, expiry, liquidity, APY fields. Iterated across all 10 chains.

**Historical TVL per market:**
```
GET https://api-v2.pendle.finance/core/v1/{chainId}/markets/{address}/historical-data?time_frame=day
```
Returns table-format response with parallel arrays: `timestamp`, `tvl`, `impliedApy`, `underlyingApy`. Daily granularity.

---

## Pendle-Specific Data Quirks

- **TVL definition:** Pendle's TVL represents the USD value of PT + SY reserves in the AMM pool — not total deposits into the yield strategy. It is specifically the liquidity available for trading.
- **Table format responses:** Historical data is returned as parallel arrays (columns), not as a list of row objects. Requires `zip()` to reassemble into row pairs.
- **Unix timestamps:** All historical timestamps are Unix epoch integers. Must be converted with `datetime.fromtimestamp()` before use.
- **Duplicate market names:** The same asset name (e.g. `weETH`) can appear on multiple chains with different contract addresses. Labels must include chain name to avoid collisions.
- **PT price convergence:** As maturity approaches, PT price converges to 1:1 with the underlying. TVL may increase near expiry without new deposits.
- **Epoch transitions:** Pendle incentive epochs reset on Thursdays at 00:00 UTC. TVL may shift around epoch boundaries as farmers rotate positions.

---

## Rate Limit Budget

Pendle API uses a Computing Unit (CU) system. All endpoints return live usage headers:
```
x-computing-unit: 5
x-ratelimit-remaining: 95
x-ratelimit-reset: 1724206817
```

| Operation | CU Cost | Count | Total CU |
|-----------|---------|-------|----------|
| Market list per chain (paginated) | 1–5 | ~30 pages | ~60 |
| Historical data per market | 1–5 | 132 markets | ~400 |
| **Total** | | | **~460** |
| Weekly limit | | | 200,000 |

The pipeline uses well under 0.5% of the weekly CU budget. A `time.sleep(0.5)` delay between historical requests prevents hitting the 100 CU/min per-minute cap.

---

## Limitations

- Analysis is constrained to the 132 markets currently active and identifiable via the API (2026-02-22). Expired markets — regardless of their historical significance — are not captured.
- Historical rankings are therefore approximations: a pool that dominated TVL in mid-2024 but has since expired would not appear in this dataset.
- Historical depth varies per market — newer markets have fewer data points. A market launched 2 weeks ago will have 14 daily rows; one live for 3 months will have ~90.
- TVL values reflect Pendle's own off-chain data and have not been cross-validated against on-chain sources.

---

## Deliverables

1. **`pendle_markets.csv`** — Snapshot of all 132 active markets with liquidity, APY, protocol, expiry and chain
2. **`pendle_history.csv`** — Full daily TVL history in long format (12,815 rows)
3. **`pendle_top10_history.csv`** — Top 10 markets by TVL per day, analysis-ready
4. **`pendle_top10_race.mp4`** — Animated bar chart race exported via ffmpeg

---

## Troubleshooting

**`ModuleNotFoundError: pandas / matplotlib`**
Run `pip install -r requirements.txt` to install all dependencies.

**`ffmpeg not found` on export:**
Install via `sudo apt install ffmpeg` (Ubuntu) or `brew install ffmpeg` (macOS). Required for MP4 export in `pendle_chart.py`.

**Empty markets on some chains:**
Expected — Optimism, Mantle and Berachain currently have 0 active markets on Pendle. The pipeline handles this gracefully without errors.

**KeyError on historical fetch:**
Usually caused by a variable name conflict with `data` — the same variable is used for paginated market responses and historical responses. Ensure historical responses are stored in a separate variable (`history`).

---

## About the author

Onchain Research | DeFi Analysis

Onchain Research focuses on onchain data analytics and automation.
Please feel free to reach out for any research collaborations or analyst roles.

📧 onchainresearch@protonmail.com
🔗 https://github.com/OnchainResearch

