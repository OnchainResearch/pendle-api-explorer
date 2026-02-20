import requests
import csv

base_url = "https://api-v2.pendle.finance/core/v1/1/markets"

all_markets = []
skip = 0
limit = 100

# ---------------------------------
# Set while loop with 100 API limit
while True :
    response = requests.get(base_url, params={"limit": limit, "skip": skip})
    data = response.json()

    results = data["results"]
    all_markets.extend(results)

    skip += limit
    
    if skip >= data["total"]:
        break

# ----------------------------------------------------------------
# Filtering markets by being still active and showing correct data
from datetime import datetime, timezone

today = datetime.now(timezone.utc)

filtered_markets = []

for market in all_markets:
    #Filter 1 : skip expired markets
    expiry = datetime.fromisoformat(market["expiry"].replace("Z", "+00:00"))
    if expiry < today:
        continue

    #Filter 2 : skip suspicious liquidity (over 1 billion$)
    if market["liquidity"]["usd"] > 1_000_000_000:
        continue

    filtered_markets.append(market)

print(f"Markets after filtering: {len(filtered_markets)}")

# ---------------------------------------------
# Parsing market data overt the selected fields
sorted_markets = sorted(filtered_markets, key=lambda m: m["liquidity"]["usd"], reverse=True)

top10 = sorted_markets[:10]

for market in top10:
    print("---")
    print("Name         :", market["simpleName"])
    print("Protocol     :", market["protocol"])
    print("Expiry       :", market["expiry"])
    print("Liquidity    :", round(market["liquidity"]["usd"], 2), "$")
    print("Implied APY  :", round(market["impliedApy"] * 100, 2), "%")
    print("UnderlyingAPY:", round(market["underlyingApy"] * 100, 2), "%")
    print("Categories   :", market["categoryIds"])

# -----------------------
# Export data to csv file
with open("pendle_markets.csv", "w", newline="") as f:
    writer = csv.writer(f)

    writer.writerow(["Name", "Protocol", "Expiry", "Liquidity USD", "Implied APY", "Underlying APY", "Categories"])

    for market in sorted_markets:
        writer.writerow([
            market["simpleName"],
            market["protocol"],
            market["expiry"],
            round(market["liquidity"]["usd"], 2),
            round(market["impliedApy"] * 100, 2),
            round(market["underlyingApy"] * 100, 2),
            ", ".join(market["categoryIds"])
        ])

print("CSV exported: pendle_markets.csv")
