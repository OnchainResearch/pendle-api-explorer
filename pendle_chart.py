import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

df = pd.read_csv("pendle_top10_history.csv")

# -------------------------------------------------------
# Add Label to avoid duplicated market with the same name

df["Label"] = df["Name"] + "(" + df["Chain"] + ")"

# ----------------------------------------------------------------------
# Sort dates in chronogical order and define the first date of the chart

dates = sorted([d for d in df["Date"].unique() if d >= "2025-06-19"])

# -----------------------------------------------------
# Attribute unique color to each market for readability

markets = df["Label"].unique()
colors = plt.cm.tab20.colors
color_map = {name: colors[i % len(colors)] for i, name in enumerate(markets)}

# ---------------------------------------
# Set chart size and adjust left position

fig, ax = plt.subplots(figsize=(12, 7))
fig.subplots_adjust(left=0.15)

# -------------------
# Set font parameters

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 11

# ---------------------------------------
# Draw chart race with graphic parameters

def draw_frame(frame_index):
    ax.clear()
    
    # -----------------------
    # Remove borders of chart
    
    for spine in ['top', 'left', 'right', 'bottom']:
        ax.spines[spine].set_visible(False)

    
    # -----------------------------
    # Chart race graphic parameters
    
    date = dates[frame_index]
    frame_data = df[df["Date"] == date].sort_values("TVL", ascending=True)

    bar_colors = [color_map.get(name, "gray") for name in frame_data["Label"]]

    ax.barh(frame_data["Label"], frame_data["TVL"], color=bar_colors)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x/1_000_000:.1f}M"))
    ax.yaxis.set_ticks_position('none')
    ax.set_title(f"TOP 10 PENDLE MARKETS BY TVL  {date}", fontsize=14)
    ax.set_xlim(0, df["TVL"].max() * 1.1)

# -------------------
# Set animation speed

ani = animation.FuncAnimation(fig, draw_frame, frames=len(dates), interval=100)

# -----------------------------------
# Export the chart race to mp4 format

ani.save("pendle_top10_race.mp4", writer="ffmpeg", fps=12, dpi=150)
print("Video exported: pendle_top10_race.mp4")

# -----------------------
# Additionnal print tests

#plt.tight_layout()
#plt.show()

