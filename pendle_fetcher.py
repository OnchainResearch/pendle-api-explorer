import requests

url = "https://api-v2.pendle.finance/core/v1/1/markets?limit=10"

response = requests.get(url)
data = response.json()

markets = data["results"]

for market in markets:
    print("---")
    print("Name         :", market["simpleName"])
    print("Protocol     :", market["protocol"])
    print("Expiry       :", market["expiry"])
    print("Liquidity    :", round(market["liquidity"]["usd"], 2), "$")
    print("Implied APY  :", round(market["impliedApy"] * 100, 2), "%")
    print("UnderlyingAPY:", round(market["underlyingApy"] * 100, 2), "%")
    print("Categories   :", market["categoryIds"])
