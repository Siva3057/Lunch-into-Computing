#!/usr/bin/env python3
"""Global temperature anomalies: load, clean, analyse, visualise.

Dataset: datasets/global-temp (GitHub), two public sources of global
land+ocean temperature anomalies (degrees C):
  * GISTEMP  - NASA GISS, 1880-present, baseline = 1951-1980 mean
  * GCAG     - NOAA Climate at a Glance, 1850-present, baseline = 20th-century mean
Raw files (download once, e.g. with curl):
  https://raw.githubusercontent.com/datasets/global-temp/main/data/annual.csv
  https://raw.githubusercontent.com/datasets/global-temp/main/data/monthly.csv

Usage:  python3 -I analysis.py <data_dir> <output_dir>
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

DATA_DIR = Path(sys.argv[1])
OUT_DIR = Path(sys.argv[2])
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Chart tokens (validated light-mode palette; GISTEMP = blue, GCAG = orange everywhere)
SURFACE, INK, INK2 = "#fcfcfb", "#0b0b0b", "#52514e"
GRID, AXIS = "#e1e0d9", "#c3c2b7"
BLUE, ORANGE, RED = "#2a78d6", "#eb6834", "#e34948"
COLOR = {"GISTEMP": BLUE, "GCAG": ORANGE}
NAME = {"GISTEMP": "NASA GISTEMP", "GCAG": "NOAA GCAG"}

report = []


def emit(text=""):
    print(text)
    report.append(text)


# --------------------------------------------------------------------------
# 1. LOAD AND CLEAN
# --------------------------------------------------------------------------
emit("=== 1. LOAD AND CLEAN ===")
ann = pd.read_csv(DATA_DIR / "annual.csv").rename(columns={"Mean": "Anomaly"})
mon = pd.read_csv(DATA_DIR / "monthly.csv").rename(columns={"Mean": "Anomaly"})
emit(f"Raw rows: annual={len(ann)}, monthly={len(mon)}")

# Types: monthly 'Year' is a 'YYYY-MM' string -> real dates
mon["Date"] = pd.to_datetime(mon["Year"], format="%Y-%m")
mon = mon.drop(columns="Year")
mon["Year"] = mon["Date"].dt.year
mon["Month"] = mon["Date"].dt.month

# Missing values and duplicates
emit(f"Missing values: annual={int(ann.isna().sum().sum())}, monthly={int(mon.isna().sum().sum())}")
dup_a = int(ann.duplicated(["Source", "Year"]).sum())
dup_m = int(mon.duplicated(["Source", "Date"]).sum())
emit(f"Duplicate keys: annual={dup_a}, monthly={dup_m}")
ann = ann.dropna().drop_duplicates(["Source", "Year"]).sort_values(["Source", "Year"]).reset_index(drop=True)
mon = mon.dropna().drop_duplicates(["Source", "Date"]).sort_values(["Source", "Date"]).reset_index(drop=True)

# Partial years: only keep years with all 12 months for annual statistics
months = mon.groupby(["Source", "Year"]).size().rename("Months").reset_index()
ann = ann.merge(months, on=["Source", "Year"], how="left")
partial = ann[ann["Months"] != 12]
for _, r in partial.iterrows():
    emit(f"Excluded partial year: {r.Source} {int(r.Year)} ({int(r.Months)} of 12 months)")
ann_c = ann[ann["Months"] == 12].copy()

# Consistency check: provided annual mean vs mean of the monthly values
from_monthly = mon.groupby(["Source", "Year"])["Anomaly"].mean().rename("FromMonthly").reset_index()
chk = ann_c.merge(from_monthly, on=["Source", "Year"])
emit(f"Max |annual - mean(monthly)| = {(chk.Anomaly - chk.FromMonthly).abs().max():.4f} C (sanity check)")

# The two sources use different baselines -> rebase both to 1951-1980 so they are comparable
base = ann_c[ann_c["Year"].between(1951, 1980)].groupby("Source")["Anomaly"].mean()
emit("1951-1980 mean in each source's own baseline: " + ", ".join(f"{k}={v:.3f}" for k, v in base.items()))
ann_c["Rebased"] = ann_c["Anomaly"] - ann_c["Source"].map(base)
mon["Rebased"] = mon["Anomaly"] - mon["Source"].map(base)
emit("All 'Rebased' values below are anomalies relative to the 1951-1980 mean.")

ann_c.to_csv(OUT_DIR / "cleaned_annual.csv", index=False)
mon.to_csv(OUT_DIR / "cleaned_monthly.csv", index=False)

# --------------------------------------------------------------------------
# 2. ANALYSIS
# --------------------------------------------------------------------------
emit("\n=== 2. ANALYSIS ===")

# 2a. Descriptive statistics
rows = []
for s, g in ann_c.groupby("Source"):
    rows.append({
        "Source": s, "Years": len(g), "From": g.Year.min(), "To": g.Year.max(),
        "Mean": g.Rebased.mean(), "Median": g.Rebased.median(), "Std": g.Rebased.std(),
        "Min": g.Rebased.min(), "MinYear": int(g.loc[g.Rebased.idxmin(), "Year"]),
        "Max": g.Rebased.max(), "MaxYear": int(g.loc[g.Rebased.idxmax(), "Year"]),
    })
emit("\nAnnual anomaly statistics (C vs 1951-1980):")
emit(pd.DataFrame(rows).to_string(index=False, float_format=lambda v: f"{v:.3f}"))

# 2b. Warmest years
for s in ("GISTEMP", "GCAG"):
    top = ann_c[ann_c.Source == s].nlargest(10, "Rebased")
    emit(f"\n10 warmest years, {s}: " + ", ".join(f"{int(y)} ({v:+.2f})" for y, v in zip(top.Year, top.Rebased)))

# 2c. Warmest single month
for s, g in mon.groupby("Source"):
    r = g.loc[g.Rebased.idxmax()]
    emit(f"Warmest month, {s}: {r.Date:%Y-%m} ({r.Rebased:+.2f} C)")


# 2d. Linear trends
def trend(df, start, end):
    d = df[df.Year.between(start, end)]
    slope, _ = np.polyfit(d.Year, d.Rebased, 1)
    r = np.corrcoef(d.Year, d.Rebased)[0, 1]
    return slope * 10, r, len(d)


emit("\nLinear trend (OLS, C per decade) and correlation of anomaly with year:")
for s in ("GISTEMP", "GCAG"):
    g = ann_c[ann_c.Source == s]
    for start in (int(g.Year.min()), 1970):
        sl, r, n = trend(g, start, 2025)
        emit(f"  {s:8s} {start}-2025: {sl:+.3f} C/decade, r = {r:.3f}, n = {n}")

# 2e. Decade means (GISTEMP, 1880 onward)
ann_c["Decade"] = (ann_c.Year // 10) * 10
dec = ann_c.groupby(["Source", "Decade"])["Rebased"].agg(["mean", "count"]).reset_index()
dec.to_csv(OUT_DIR / "decade_means.csv", index=False)
gdec = dec[dec.Source == "GISTEMP"].set_index("Decade")
emit("\nDecade means, GISTEMP (C vs 1951-1980):")
emit(gdec.to_string(float_format=lambda v: f"{v:.3f}"))
emit(f"(2020s covers {int(gdec.loc[2020, 'count'])} complete years only.)")

# 2f. Correlation between the two sources
wide = ann_c.pivot(index="Year", columns="Source", values="Rebased").dropna()
r_src = wide["GISTEMP"].corr(wide["GCAG"])
diff = wide["GCAG"] - wide["GISTEMP"]
emit(f"\nGISTEMP vs GCAG annual anomalies, {wide.index.min()}-{wide.index.max()} (n={len(wide)}): "
     f"Pearson r = {r_src:.3f}, mean difference (GCAG-GISTEMP) = {diff.mean():+.3f} C, "
     f"std of difference = {diff.std():.3f} C")

(OUT_DIR / "summary.txt").write_text("\n".join(report) + "\n")


# --------------------------------------------------------------------------
# 3. VISUALISATIONS
# --------------------------------------------------------------------------
def style(ax):
    ax.set_facecolor(SURFACE)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(AXIS)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.tick_params(colors=INK2, length=0, labelsize=10)
    ax.xaxis.label.set_color(INK2)
    ax.yaxis.label.set_color(INK2)


def title(fig, main, sub):
    fig.text(0.015, 0.965, main, ha="left", va="top", fontsize=15, fontweight="bold", color=INK)
    fig.text(0.015, 0.905, sub, ha="left", va="top", fontsize=10.5, color=INK2)


# --- Chart 1: annual anomalies, both sources ---
fig, ax = plt.subplots(figsize=(10, 5.8), facecolor=SURFACE)
style(ax)
for s in ("GCAG", "GISTEMP"):
    g = ann_c[ann_c.Source == s]
    ax.plot(g.Year, g.Rebased, color=COLOR[s], linewidth=2, label=NAME[s], solid_capstyle="round")
ax.axhline(0, color=AXIS, linewidth=1)
last = ann_c[ann_c.Year == 2025].set_index("Source")["Rebased"]
offsets = {"GISTEMP": 9, "GCAG": -9}
for s in ("GISTEMP", "GCAG"):
    ax.plot(2025, last[s], "o", color=COLOR[s], markersize=7, markeredgecolor=SURFACE, markeredgewidth=1.5)
    ax.annotate(NAME[s], (2025, last[s]), xytext=(10, offsets[s]), textcoords="offset points",
                color=INK2, fontsize=10, va="center")
peak = ann_c[ann_c.Source == "GISTEMP"].loc[lambda d: d.Rebased.idxmax()]
ax.annotate(f"{int(peak.Year)}: {peak.Rebased:+.2f} °C", (peak.Year, peak.Rebased), xytext=(-8, 10),
            textcoords="offset points", color=INK2, fontsize=10, ha="right")
ax.set_xlim(1848, 2030)
ax.set_xticks(range(1850, 2030, 20))
ax.set_ylabel("Anomaly vs 1951–1980 mean (°C)")
ax.legend(frameon=False, loc="upper left", labelcolor=INK2, fontsize=10)
fig.subplots_adjust(top=0.82, left=0.08, right=0.85, bottom=0.12)
title(fig, "Global temperature is now more than 1 °C above the 1951–1980 mean",
      "Annual global land+ocean anomaly, two independent agencies rebased to a common baseline")
fig.savefig(OUT_DIR / "01_annual_trend.png", dpi=200, facecolor=SURFACE)
plt.close(fig)

# --- Chart 2: decade means (GISTEMP) ---
fig, ax = plt.subplots(figsize=(10, 5.8), facecolor=SURFACE)
style(ax)
vals = gdec["mean"].values
x = np.arange(len(gdec))
ax.bar(x, vals, color=[RED if v > 0 else BLUE for v in vals], edgecolor=SURFACE, linewidth=2, width=0.82)
ax.axhline(0, color=AXIS, linewidth=1)
for i in (0, int(np.argmin(vals)), len(vals) - 1):
    v = vals[i]
    ax.annotate(f"{v:+.2f}", (i, v), xytext=(0, 5 if v > 0 else -5), textcoords="offset points",
                ha="center", va="bottom" if v > 0 else "top", color=INK2, fontsize=10)
ax.set_xticks(x)
ax.set_xticklabels([f"{d}s" + ("*" if gdec.loc[d, "count"] < 10 else "") for d in gdec.index])
ax.set_ylabel("Mean anomaly vs 1951–1980 (°C)")
ax.set_ylim(min(vals) - 0.12, max(vals) + 0.15)
fig.subplots_adjust(top=0.82, left=0.08, right=0.97, bottom=0.15)
title(fig, "Every decade since the 1980s has been warmer than the one before",
      "Mean annual anomaly per decade, NASA GISTEMP (blue = below baseline, red = above)")
fig.text(0.015, 0.02, "* 2020s = 2020–2025 only", color=INK2, fontsize=9.5)
fig.savefig(OUT_DIR / "02_decade_means.png", dpi=200, facecolor=SURFACE)
plt.close(fig)

# --- Chart 3: GISTEMP vs GCAG ---
fig, ax = plt.subplots(figsize=(7, 7), facecolor=SURFACE)
style(ax)
ax.grid(axis="x", color=GRID, linewidth=0.8)
lim = (min(wide.min()) - 0.1, max(wide.max()) + 0.1)
ax.plot(lim, lim, color=INK2, linestyle="--", linewidth=1.5, zorder=2)
ax.scatter(wide["GISTEMP"], wide["GCAG"], s=48, color=BLUE, edgecolor=SURFACE, linewidth=1.2, zorder=3)
ax.set_xlim(lim)
ax.set_ylim(lim)
ax.set_aspect("equal", adjustable="box")
ax.set_xlabel("NASA GISTEMP anomaly (°C)")
ax.set_ylabel("NOAA GCAG anomaly (°C)")
ax.text(0.04, 0.95, f"Pearson r = {r_src:.3f}\nn = {len(wide)} years ({wide.index.min()}–{wide.index.max()})",
        transform=ax.transAxes, va="top", color=INK2, fontsize=10.5)
ax.text(0.97, 0.03, "dashed line: y = x", transform=ax.transAxes, ha="right", color=INK2, fontsize=9.5)
fig.subplots_adjust(top=0.84, left=0.12, right=0.96, bottom=0.10)
title(fig, "The two agencies agree almost perfectly",
      "Annual anomalies, NOAA GCAG vs NASA GISTEMP (both rebased to 1951–1980)")
fig.savefig(OUT_DIR / "03_source_correlation.png", dpi=200, facecolor=SURFACE)
plt.close(fig)

print("\nWrote:", ", ".join(sorted(p.name for p in OUT_DIR.iterdir())))
