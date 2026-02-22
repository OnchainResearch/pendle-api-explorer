import pandas as pd

df = pd.read_csv("pendle_history.csv")

print(df.head(10))
print(df.shape)
print(df["Date"].unique())

top10_per_day = (
    df.sort_values("TVL", ascending=False)
    .groupby("Date")
    .head(10)
)

top10_per_day.sort_values(["Date", "TVL"], ascending=[True, False]).to_csv("pendle_top10_history.csv", index=False)
print("CSV exported: pendle_top10_history.csv")
