import streamlit as st

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
import streamlit as st
from utils.data_processing import mergeyears
import plotly.express as px
st.title("Attacks Against Land Defenders")
st.caption("by Caroline, Fernanda and Annika")

data = mergeyears

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# ── DATA ──────────────────────────────────────────────────────────────────────
data = [
    {"Country": "Argentina",          "Year": 2021, "Incidents": 1,  "Criminality": 4.38, "Resilience": 6.33, "Region": "Other"},
    {"Country": "Bolivia",            "Year": 2021, "Incidents": 1,  "Criminality": 4.30, "Resilience": 4.88, "Region": "Latin America"},
    {"Country": "Brazil",             "Year": 2021, "Incidents": 26, "Criminality": 6.50, "Resilience": 5.04, "Region": "Latin America"},
    {"Country": "Brazil",             "Year": 2023, "Incidents": 25, "Criminality": 6.77, "Resilience": 4.92, "Region": "Latin America"},
    {"Country": "Chile",              "Year": 2021, "Incidents": 1,  "Criminality": 4.60, "Resilience": 6.42, "Region": "Other"},
    {"Country": "Colombia",           "Year": 2021, "Incidents": 33, "Criminality": 7.66, "Resilience": 5.83, "Region": "Latin America"},
    {"Country": "Colombia",           "Year": 2023, "Incidents": 79, "Criminality": 7.75, "Resilience": 5.63, "Region": "Latin America"},
    {"Country": "Dem. Rep. Congo",    "Year": 2021, "Incidents": 8,  "Criminality": 7.75, "Resilience": 2.29, "Region": "Africa"},
    {"Country": "Dem. Rep. Congo",    "Year": 2023, "Incidents": 2,  "Criminality": 7.35, "Resilience": 2.38, "Region": "Africa"},
    {"Country": "Ecuador",            "Year": 2021, "Incidents": 3,  "Criminality": 6.25, "Resilience": 5.71, "Region": "Latin America"},
    {"Country": "Ecuador",            "Year": 2023, "Incidents": 1,  "Criminality": 7.07, "Resilience": 4.88, "Region": "Latin America"},
    {"Country": "Gabon",              "Year": 2021, "Incidents": 1,  "Criminality": 4.90, "Resilience": 3.17, "Region": "Africa"},
    {"Country": "Ghana",              "Year": 2023, "Incidents": 1,  "Criminality": 5.80, "Resilience": 5.46, "Region": "Africa"},
    {"Country": "Guatemala",          "Year": 2021, "Incidents": 4,  "Criminality": 6.48, "Resilience": 4.42, "Region": "Latin America"},
    {"Country": "Guatemala",          "Year": 2023, "Incidents": 4,  "Criminality": 6.60, "Resilience": 4.08, "Region": "Latin America"},
    {"Country": "Honduras",           "Year": 2021, "Incidents": 8,  "Criminality": 6.98, "Resilience": 3.92, "Region": "Latin America"},
    {"Country": "Honduras",           "Year": 2023, "Incidents": 18, "Criminality": 7.05, "Resilience": 4.08, "Region": "Latin America"},
    {"Country": "India",              "Year": 2021, "Incidents": 14, "Criminality": 5.53, "Resilience": 5.25, "Region": "Asia/Other"},
    {"Country": "India",              "Year": 2023, "Incidents": 5,  "Criminality": 5.75, "Resilience": 5.42, "Region": "Asia/Other"},
    {"Country": "Indonesia",          "Year": 2023, "Incidents": 3,  "Criminality": 6.85, "Resilience": 4.25, "Region": "Asia/Other"},
    {"Country": "Kenya",              "Year": 2021, "Incidents": 1,  "Criminality": 6.95, "Resilience": 5.21, "Region": "Africa"},
    {"Country": "Mexico",             "Year": 2021, "Incidents": 54, "Criminality": 7.56, "Resilience": 4.46, "Region": "Latin America"},
    {"Country": "Mexico",             "Year": 2023, "Incidents": 18, "Criminality": 7.57, "Resilience": 4.21, "Region": "Latin America"},
    {"Country": "Nicaragua",          "Year": 2021, "Incidents": 15, "Criminality": 6.06, "Resilience": 2.46, "Region": "Latin America"},
    {"Country": "Nicaragua",          "Year": 2023, "Incidents": 10, "Criminality": 5.72, "Resilience": 2.08, "Region": "Latin America"},
    {"Country": "Panama",             "Year": 2023, "Incidents": 4,  "Criminality": 6.98, "Resilience": 4.67, "Region": "Latin America"},
    {"Country": "Paraguay",           "Year": 2023, "Incidents": 2,  "Criminality": 7.52, "Resilience": 3.42, "Region": "Latin America"},
    {"Country": "Peru",               "Year": 2021, "Incidents": 7,  "Criminality": 6.35, "Resilience": 4.58, "Region": "Latin America"},
    {"Country": "Peru",               "Year": 2023, "Incidents": 4,  "Criminality": 6.40, "Resilience": 4.38, "Region": "Latin America"},
    {"Country": "Philippines",        "Year": 2021, "Incidents": 19, "Criminality": 6.84, "Resilience": 4.13, "Region": "Asia/Other"},
    {"Country": "Philippines",        "Year": 2023, "Incidents": 17, "Criminality": 6.63, "Resilience": 4.21, "Region": "Asia/Other"},
    {"Country": "Rwanda",             "Year": 2023, "Incidents": 1,  "Criminality": 3.60, "Resilience": 5.54, "Region": "Africa"},
    {"Country": "United States",      "Year": 2023, "Incidents": 1,  "Criminality": 5.67, "Resilience": 7.13, "Region": "Asia/Other"},
    {"Country": "Venezuela",          "Year": 2021, "Incidents": 4,  "Criminality": 6.64, "Resilience": 1.92, "Region": "Latin America"},
    {"Country": "Venezuela",          "Year": 2023, "Incidents": 1,  "Criminality": 6.72, "Resilience": 1.88, "Region": "Latin America"},
]

df = pd.DataFrame(data)
df["Year"] = df["Year"].astype(str)   # treat year as categorical (for legend + filter)

# ── COLOR & SYMBOL MAPS ───────────────────────────────────────────────────────
region_colors = {
    "Latin America": "#ff6b35",
    "Africa":        "#00bfff",
    "Asia/Other":    "#a855f7",
    "Other":         "#94a3b8",
}

# Circles = 2021, Diamonds = 2023
symbol_map = {"2021": "circle", "2023": "diamond"}

# ── CUSTOM HOVER TEXT ─────────────────────────────────────────────────────────
df["hover"] = (
    "<b>" + df["Country"] + " (" + df["Year"] + ")</b><br>"
    + "Incidents: <b>" + df["Incidents"].astype(str) + "</b><br>"
    + "Criminality Score: <b>" + df["Criminality"].astype(str) + " / 10</b>  "
    + "(1 = low risk, 10 = high risk)<br>"
    + "Resilience Score: <b>" + df["Resilience"].astype(str) + " / 10</b>  "
    + "(1 = low, 10 = highly resilient)<br>"
    + "Region: " + df["Region"]
)

# ── SCATTER PLOT ──────────────────────────────────────────────────────────────
fig = px.scatter(
    df,
    x="Criminality",
    y="Resilience",
    size="Incidents",
    color="Region",
    symbol="Year",
    symbol_map=symbol_map,
    color_discrete_map=region_colors,
    hover_name="Country",
    custom_data=["hover"],
    size_max=55,
    title="Global Crime Intelligence — Criminality vs. Resilience (2021 & 2023)",
    labels={
        "Criminality": "Criminality Score  (1 = low risk  →  10 = high risk)",
        "Resilience":  "Resilience Score  (1 = low  →  10 = highly resilient)",
    },
)

# Fully custom tooltip
fig.update_traces(hovertemplate="%{customdata[0]}<extra></extra>")

# ── QUADRANT SHADING ──────────────────────────────────────────────────────────
mid_x, mid_y = 5.75, 4.5

quadrants = [
    dict(x0=2.5,   x1=mid_x, y0=mid_y, y1=8,
         color="rgba(0,191,255,0.06)",
         label="Low crime · High resilience",  lx=2.6,  ly=7.75),
    dict(x0=mid_x, x1=9.0,   y0=mid_y, y1=8,
         color="rgba(168,85,247,0.06)",
         label="High crime · High resilience", lx=5.85, ly=7.75),
    dict(x0=2.5,   x1=mid_x, y0=1.0,   y1=mid_y,
         color="rgba(148,163,184,0.05)",
         label="Low crime · Low resilience",   lx=2.6,  ly=1.15),
    dict(x0=mid_x, x1=9.0,   y0=1.0,   y1=mid_y,
         color="rgba(255,71,87,0.08)",
         label="High crime · Low resilience ⚠", lx=5.85, ly=1.15),
]

for q in quadrants:
    fig.add_shape(
        type="rect",
        x0=q["x0"], x1=q["x1"], y0=q["y0"], y1=q["y1"],
        fillcolor=q["color"], line_width=0, layer="below",
    )
    fig.add_annotation(
        x=q["lx"], y=q["ly"], text=q["label"],
        showarrow=False,
        font=dict(size=9, color="rgba(200,200,200,0.4)"),
        xanchor="left",
    )

# Divider lines between quadrants
fig.add_shape(type="line",
    x0=mid_x, x1=mid_x, y0=1, y1=8,
    line=dict(color="rgba(255,255,255,0.12)", dash="dot", width=1))
fig.add_shape(type="line",
    x0=2.5, x1=9, y0=mid_y, y1=mid_y,
    line=dict(color="rgba(255,255,255,0.12)", dash="dot", width=1))

# ── COUNTRY LABELS (only for high-incident countries) ─────────────────────────
for _, row in df[df["Incidents"] >= 10].iterrows():
    fig.add_annotation(
        x=row["Criminality"],
        y=row["Resilience"],
        text=row["Country"],
        showarrow=False,
        font=dict(size=8, color="rgba(220,220,220,0.65)"),
        yshift=20,
        xanchor="center",
    )

# ── LAYOUT ────────────────────────────────────────────────────────────────────
fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#0a0c10",
    plot_bgcolor="#111318",
    font=dict(family="monospace", color="#c8cad0"),
    title=dict(
        font=dict(size=17, family="sans-serif"),
        x=0.5,
        xanchor="center",
    ),
    xaxis=dict(
        range=[2.5, 9.0],
        gridcolor="#1e2330",
        zerolinecolor="#1e2330",
        tickformat=".1f",
        dtick=0.5,
    ),
    yaxis=dict(
        range=[1.0, 8.0],
        gridcolor="#1e2330",
        zerolinecolor="#1e2330",
        tickformat=".1f",
        dtick=0.5,
    ),
    legend=dict(
        bgcolor="rgba(17,19,24,0.85)",
        bordercolor="#2a2f3d",
        borderwidth=1,
        title_text="Region / Year",
        title_font_size=11,
    ),
    hoverlabel=dict(
        bgcolor="#181c24",
        bordercolor="#e8ff47",
        font=dict(family="monospace", size=12),
    ),
    margin=dict(l=60, r=40, t=70, b=70),
)

# ── RUN ───────────────────────────────────────────────────────────────────────
# Opens automatically in your default browser:
fig.show()

# To save as a standalone shareable HTML file, uncomment the line below:
# fig.write_html("crime_scatterplot.html")