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

import streamlit as st
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="Land Defender Attacks", layout="wide")

# ── DATA ──────────────────────────────────────────────────────────────────────
data = [
    {"Country": "Argentina",       "Year": 2021, "Incidents": 1,  "Region": "Other"},
    {"Country": "Bolivia",         "Year": 2021, "Incidents": 1,  "Region": "Latin America"},
    {"Country": "Brazil",          "Year": 2021, "Incidents": 26, "Region": "Latin America"},
    {"Country": "Brazil",          "Year": 2023, "Incidents": 25, "Region": "Latin America"},
    {"Country": "Chile",           "Year": 2021, "Incidents": 1,  "Region": "Other"},
    {"Country": "Colombia",        "Year": 2021, "Incidents": 33, "Region": "Latin America"},
    {"Country": "Colombia",        "Year": 2023, "Incidents": 79, "Region": "Latin America"},
    {"Country": "Dem. Rep. Congo", "Year": 2021, "Incidents": 8,  "Region": "Africa"},
    {"Country": "Dem. Rep. Congo", "Year": 2023, "Incidents": 2,  "Region": "Africa"},
    {"Country": "Ecuador",         "Year": 2021, "Incidents": 3,  "Region": "Latin America"},
    {"Country": "Ecuador",         "Year": 2023, "Incidents": 1,  "Region": "Latin America"},
    {"Country": "Gabon",           "Year": 2021, "Incidents": 1,  "Region": "Africa"},
    {"Country": "Ghana",           "Year": 2023, "Incidents": 1,  "Region": "Africa"},
    {"Country": "Guatemala",       "Year": 2021, "Incidents": 4,  "Region": "Latin America"},
    {"Country": "Guatemala",       "Year": 2023, "Incidents": 4,  "Region": "Latin America"},
    {"Country": "Honduras",        "Year": 2021, "Incidents": 8,  "Region": "Latin America"},
    {"Country": "Honduras",        "Year": 2023, "Incidents": 18, "Region": "Latin America"},
    {"Country": "India",           "Year": 2021, "Incidents": 14, "Region": "Asia/Other"},
    {"Country": "India",           "Year": 2023, "Incidents": 5,  "Region": "Asia/Other"},
    {"Country": "Indonesia",       "Year": 2023, "Incidents": 3,  "Region": "Asia/Other"},
    {"Country": "Kenya",           "Year": 2021, "Incidents": 1,  "Region": "Africa"},
    {"Country": "Mexico",          "Year": 2021, "Incidents": 54, "Region": "Latin America"},
    {"Country": "Mexico",          "Year": 2023, "Incidents": 18, "Region": "Latin America"},
    {"Country": "Nicaragua",       "Year": 2021, "Incidents": 15, "Region": "Latin America"},
    {"Country": "Nicaragua",       "Year": 2023, "Incidents": 10, "Region": "Latin America"},
    {"Country": "Panama",          "Year": 2023, "Incidents": 4,  "Region": "Latin America"},
    {"Country": "Paraguay",        "Year": 2023, "Incidents": 2,  "Region": "Latin America"},
    {"Country": "Peru",            "Year": 2021, "Incidents": 7,  "Region": "Latin America"},
    {"Country": "Peru",            "Year": 2023, "Incidents": 4,  "Region": "Latin America"},
    {"Country": "Philippines",     "Year": 2021, "Incidents": 19, "Region": "Asia/Other"},
    {"Country": "Philippines",     "Year": 2023, "Incidents": 17, "Region": "Asia/Other"},
    {"Country": "Rwanda",          "Year": 2023, "Incidents": 1,  "Region": "Africa"},
    {"Country": "United States",   "Year": 2023, "Incidents": 1,  "Region": "Asia/Other"},
    {"Country": "Venezuela",       "Year": 2021, "Incidents": 4,  "Region": "Latin America"},
    {"Country": "Venezuela",       "Year": 2023, "Incidents": 1,  "Region": "Latin America"},
]

df = pd.DataFrame(data)

# ── BUILD COMPARISON TABLE ────────────────────────────────────────────────────
df21 = df[df["Year"] == 2021].set_index("Country")[["Incidents", "Region"]].rename(columns={"Incidents": "inc_2021"})
df23 = df[df["Year"] == 2023].set_index("Country")[["Incidents", "Region"]].rename(columns={"Incidents": "inc_2023"})

comp = df21.join(df23, how="outer", lsuffix="_21", rsuffix="_23")
comp["Region"] = comp["Region_21"].fillna(comp["Region_23"])
comp = comp[["inc_2021", "inc_2023", "Region"]].fillna(0)
comp["inc_2021"] = comp["inc_2021"].astype(int)
comp["inc_2023"] = comp["inc_2023"].astype(int)
comp["change"] = comp["inc_2023"] - comp["inc_2021"]
comp["pct_change"] = comp.apply(
    lambda r: ((r["inc_2023"] - r["inc_2021"]) / r["inc_2021"] * 100)
              if r["inc_2021"] > 0 else float("nan"),
    axis=1,
)
comp = comp.sort_values(["inc_2021", "inc_2023"], ascending=False)
countries = comp.index.tolist()

# ── COLORS ────────────────────────────────────────────────────────────────────
region_colors = {
    "Latin America": "#ff6b35",
    "Africa":        "#00bfff",
    "Asia/Other":    "#a855f7",
    "Other":         "#94a3b8",
}
bar_colors = [region_colors.get(comp.loc[c, "Region"], "#94a3b8") for c in countries]

# ── HOVER TEXT ────────────────────────────────────────────────────────────────
def change_label(row):
    if row["inc_2021"] == 0:
        return "New in 2023"
    diff = row["change"]
    pct  = row["pct_change"]
    arrow = "▲" if diff > 0 else ("▼" if diff < 0 else "—")
    sign  = "+" if diff > 0 else ""
    return f"{arrow} {sign}{diff} attacks ({sign}{pct:.0f}%)"

hover_21 = [
    f"<b>{c}</b><br>2021 Attacks: <b>{comp.loc[c,'inc_2021']}</b><br>"
    f"Region: {comp.loc[c,'Region']}<br>vs 2023: {change_label(comp.loc[c])}"
    for c in countries
]
hover_23 = [
    f"<b>{c}</b><br>2023 Attacks: <b>{comp.loc[c,'inc_2023']}</b><br>"
    f"Region: {comp.loc[c,'Region']}<br>Change from 2021: {change_label(comp.loc[c])}"
    for c in countries
]

# ── PAGE HEADER ───────────────────────────────────────────────────────────────
st.title("🌍 Land Defender Attacks — 2021 vs 2023")
st.markdown("Hover over bars for details. Labels show the change between years.")

# ── FILTER SIDEBAR ────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Filters")
    regions = ["All"] + sorted(comp["Region"].unique().tolist())
    selected_region = st.selectbox("Filter by Region", regions)
    sort_by = st.radio("Sort countries by", ["2021 incidents", "2023 incidents", "Change (absolute)"])

# Apply region filter
mask = [True] * len(countries)
if selected_region != "All":
    mask = [comp.loc[c, "Region"] == selected_region for c in countries]

filtered_countries = [c for c, m in zip(countries, mask) if m]

# Apply sort
sort_map = {
    "2021 incidents":     "inc_2021",
    "2023 incidents":     "inc_2023",
    "Change (absolute)":  "change",
}
filtered_comp = comp.loc[filtered_countries].sort_values(sort_map[sort_by], ascending=False)
filtered_countries = filtered_comp.index.tolist()

f_colors   = [region_colors.get(filtered_comp.loc[c, "Region"], "#94a3b8") for c in filtered_countries]
f_hover_21 = [hover_21[countries.index(c)] for c in filtered_countries]
f_hover_23 = [hover_23[countries.index(c)] for c in filtered_countries]

# ── FIGURE ────────────────────────────────────────────────────────────────────
fig = go.Figure()

fig.add_trace(go.Bar(
    name="2021",
    x=filtered_countries,
    y=filtered_comp["inc_2021"].tolist(),
    marker=dict(color=f_colors, opacity=0.45, line=dict(color=f_colors, width=1.5)),
    hovertemplate="%{customdata}<extra></extra>",
    customdata=f_hover_21,
    width=0.38,
    offset=-0.2,
))

fig.add_trace(go.Bar(
    name="2023",
    x=filtered_countries,
    y=filtered_comp["inc_2023"].tolist(),
    marker=dict(
        color=f_colors,
        opacity=1.0,
        line=dict(color=f_colors, width=1.5),
        pattern=dict(shape="/", fgcolor="rgba(255,255,255,0.15)", size=6),
    ),
    hovertemplate="%{customdata}<extra></extra>",
    customdata=f_hover_23,
    width=0.38,
    offset=0.18,
))

# Change labels above bars
for c in filtered_countries:
    row = filtered_comp.loc[c]
    if row["inc_2021"] == 0 or row["inc_2023"] == 0:
        continue
    diff = row["change"]
    if diff == 0:
        continue
    y_top = max(row["inc_2021"], row["inc_2023"])
    color = "#ff4757" if diff > 0 else "#00d2ff"
    sign  = "+" if diff > 0 else ""
    fig.add_annotation(
        x=c, y=y_top + 1.5,
        text=f"{sign}{int(diff)}",
        showarrow=False,
        font=dict(size=9, color=color, family="monospace"),
        xanchor="center", yanchor="bottom",
    )

fig.update_layout(
    barmode="overlay",
    template="plotly_dark",
    paper_bgcolor="#0e1117",
    plot_bgcolor="#0e1117",
    font=dict(family="monospace", color="#c8cad0", size=11),
    xaxis=dict(tickangle=-35, gridcolor="#1e2330", tickfont=dict(size=10)),
    yaxis=dict(title="Number of Attacks", gridcolor="#1e2330", zeroline=False),
    legend=dict(
        bgcolor="rgba(17,19,24,0.85)",
        bordercolor="#2a2f3d",
        borderwidth=1,
        orientation="h",
        yanchor="bottom", y=1.01,
        xanchor="right", x=1,
    ),
    hoverlabel=dict(bgcolor="#181c24", bordercolor="#e8ff47", font=dict(family="monospace", size=12)),
    margin=dict(l=60, r=40, t=60, b=120),
    height=520,
)

# ── RENDER IN STREAMLIT ───────────────────────────────────────────────────────
st.plotly_chart(fig, use_container_width=True)

# ── SUMMARY METRICS ───────────────────────────────────────────────────────────
st.divider()
col1, col2, col3, col4 = st.columns(4)

total_21 = filtered_comp["inc_2021"].sum()
total_23 = filtered_comp["inc_2023"].sum()
total_change = total_23 - total_21
biggest_increase = filtered_comp.loc[filtered_comp["change"].idxmax()]
biggest_decrease = filtered_comp.loc[filtered_comp["change"].idxmin()]

col1.metric("Total Attacks 2021", total_21)
col2.metric("Total Attacks 2023", total_23, delta=int(total_change))
col3.metric("Biggest Increase", biggest_increase.name, delta=f"+{int(biggest_increase['change'])}")
col4.metric("Biggest Decrease", biggest_decrease.name, delta=int(biggest_decrease["change"]))


#resilience and criminality 

import streamlit as st
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="Criminality & Resilience Scores", layout="wide")

# ── DATA ──────────────────────────────────────────────────────────────────────
data = [
    {"Country": "Argentina",       "Year": 2021, "Criminality": 4.38, "Resilience": 6.33, "Region": "Other"},
    {"Country": "Bolivia",         "Year": 2021, "Criminality": 4.30, "Resilience": 4.88, "Region": "Latin America"},
    {"Country": "Brazil",          "Year": 2021, "Criminality": 6.50, "Resilience": 5.04, "Region": "Latin America"},
    {"Country": "Brazil",          "Year": 2023, "Criminality": 6.77, "Resilience": 4.92, "Region": "Latin America"},
    {"Country": "Chile",           "Year": 2021, "Criminality": 4.60, "Resilience": 6.42, "Region": "Other"},
    {"Country": "Colombia",        "Year": 2021, "Criminality": 7.66, "Resilience": 5.83, "Region": "Latin America"},
    {"Country": "Colombia",        "Year": 2023, "Criminality": 7.75, "Resilience": 5.63, "Region": "Latin America"},
    {"Country": "Dem. Rep. Congo", "Year": 2021, "Criminality": 7.75, "Resilience": 2.29, "Region": "Africa"},
    {"Country": "Dem. Rep. Congo", "Year": 2023, "Criminality": 7.35, "Resilience": 2.38, "Region": "Africa"},
    {"Country": "Ecuador",         "Year": 2021, "Criminality": 6.25, "Resilience": 5.71, "Region": "Latin America"},
    {"Country": "Ecuador",         "Year": 2023, "Criminality": 7.07, "Resilience": 4.88, "Region": "Latin America"},
    {"Country": "Gabon",           "Year": 2021, "Criminality": 4.90, "Resilience": 3.17, "Region": "Africa"},
    {"Country": "Ghana",           "Year": 2023, "Criminality": 5.80, "Resilience": 5.46, "Region": "Africa"},
    {"Country": "Guatemala",       "Year": 2021, "Criminality": 6.48, "Resilience": 4.42, "Region": "Latin America"},
    {"Country": "Guatemala",       "Year": 2023, "Criminality": 6.60, "Resilience": 4.08, "Region": "Latin America"},
    {"Country": "Honduras",        "Year": 2021, "Criminality": 6.98, "Resilience": 3.92, "Region": "Latin America"},
    {"Country": "Honduras",        "Year": 2023, "Criminality": 7.05, "Resilience": 4.08, "Region": "Latin America"},
    {"Country": "India",           "Year": 2021, "Criminality": 5.53, "Resilience": 5.25, "Region": "Asia/Other"},
    {"Country": "India",           "Year": 2023, "Criminality": 5.75, "Resilience": 5.42, "Region": "Asia/Other"},
    {"Country": "Indonesia",       "Year": 2023, "Criminality": 6.85, "Resilience": 4.25, "Region": "Asia/Other"},
    {"Country": "Kenya",           "Year": 2021, "Criminality": 6.95, "Resilience": 5.21, "Region": "Africa"},
    {"Country": "Mexico",          "Year": 2021, "Criminality": 7.56, "Resilience": 4.46, "Region": "Latin America"},
    {"Country": "Mexico",          "Year": 2023, "Criminality": 7.57, "Resilience": 4.21, "Region": "Latin America"},
    {"Country": "Nicaragua",       "Year": 2021, "Criminality": 6.06, "Resilience": 2.46, "Region": "Latin America"},
    {"Country": "Nicaragua",       "Year": 2023, "Criminality": 5.72, "Resilience": 2.08, "Region": "Latin America"},
    {"Country": "Panama",          "Year": 2023, "Criminality": 6.98, "Resilience": 4.67, "Region": "Latin America"},
    {"Country": "Paraguay",        "Year": 2023, "Criminality": 7.52, "Resilience": 3.42, "Region": "Latin America"},
    {"Country": "Peru",            "Year": 2021, "Criminality": 6.35, "Resilience": 4.58, "Region": "Latin America"},
    {"Country": "Peru",            "Year": 2023, "Criminality": 6.40, "Resilience": 4.38, "Region": "Latin America"},
    {"Country": "Philippines",     "Year": 2021, "Criminality": 6.84, "Resilience": 4.13, "Region": "Asia/Other"},
    {"Country": "Philippines",     "Year": 2023, "Criminality": 6.63, "Resilience": 4.21, "Region": "Asia/Other"},
    {"Country": "Rwanda",          "Year": 2023, "Criminality": 3.60, "Resilience": 5.54, "Region": "Africa"},
    {"Country": "United States",   "Year": 2023, "Criminality": 5.67, "Resilience": 7.13, "Region": "Asia/Other"},
    {"Country": "Venezuela",       "Year": 2021, "Criminality": 6.64, "Resilience": 1.92, "Region": "Latin America"},
    {"Country": "Venezuela",       "Year": 2023, "Criminality": 6.72, "Resilience": 1.88, "Region": "Latin America"},
]

df = pd.DataFrame(data)

# ── SESSION STATE for selected country ───────────────────────────────────────
if "selected_country" not in st.session_state:
    st.session_state.selected_country = None

# ── BUILD COMPARISON TABLE ────────────────────────────────────────────────────
def build_comp(metric):
    d21 = df[df["Year"] == 2021].set_index("Country")[[metric, "Region"]].rename(columns={metric: "v_2021"})
    d23 = df[df["Year"] == 2023].set_index("Country")[[metric, "Region"]].rename(columns={metric: "v_2023"})
    c = d21.join(d23, how="outer", lsuffix="_21", rsuffix="_23")
    c["Region"] = c["Region_21"].fillna(c["Region_23"])
    c = c[["v_2021", "v_2023", "Region"]]
    c["change"] = (c["v_2023"] - c["v_2021"]).round(2)
    return c

comp_crim = build_comp("Criminality")
comp_res  = build_comp("Resilience")

region_colors = {
    "Latin America": "#ff6b35",
    "Africa":        "#00bfff",
    "Asia/Other":    "#a855f7",
    "Other":         "#94a3b8",
}

# ── CHART BUILDER ─────────────────────────────────────────────────────────────
def make_chart(comp, metric_label, higher_is_worse, filtered_countries, selected_country):
    fig = go.Figure()

    for year, opacity_base, offset, pattern in [
        ("2021", 0.4, -0.2, ""),
        ("2023", 1.0,  0.18, "/"),
    ]:
        val_col = f"v_{year}"
        colors, opacities, line_widths = [], [], []

        for c in filtered_countries:
            base_color = region_colors.get(comp.loc[c, "Region"], "#94a3b8")
            if selected_country is None or c == selected_country:
                colors.append(base_color)
                opacities.append(opacity_base)
                line_widths.append(2.5 if c == selected_country else 1.5)
            else:
                # Dim all non-selected countries
                colors.append("rgba(100,100,100,0.3)")
                opacities.append(0.2)
                line_widths.append(0.5)

        values = [
            comp.loc[c, val_col] if pd.notna(comp.loc[c, val_col]) else 0
            for c in filtered_countries
        ]

        hover_texts = []
        for c in filtered_countries:
            row = comp.loc[c]
            v = row[val_col]
            diff = row["change"]
            v_str = f"{v:.2f}" if pd.notna(v) else "N/A"
            if pd.notna(diff) and diff != 0:
                sign = "+" if diff > 0 else ""
                if higher_is_worse:
                    verdict = "⚠ Worsened" if diff > 0 else "✓ Improved"
                else:
                    verdict = "✓ Improved" if diff > 0 else "⚠ Worsened"
                change_str = f"{sign}{diff:.2f} ({verdict})"
            else:
                change_str = "— No change"
            hover_texts.append(
                f"<b>{c}</b><br>{year} {metric_label}: <b>{v_str} / 10</b><br>"
                f"Region: {row['Region']}<br>Change 2021→2023: {change_str}"
                f"<br><i>Click to highlight across charts</i>"
            )

        fig.add_trace(go.Bar(
            name=year,
            x=filtered_countries,
            y=values,
            marker=dict(
                color=colors,
                opacity=opacities,
                line=dict(color=colors, width=line_widths),
                pattern=dict(shape=pattern, fgcolor="rgba(255,255,255,0.15)", size=6)
                if pattern else {},
            ),
            hovertemplate="%{customdata}<extra></extra>",
            customdata=hover_texts,
            width=0.38,
            offset=offset,
        ))

    # Change labels
    for c in filtered_countries:
        row = comp.loc[c]
        if pd.isna(row.get("v_2021")) or pd.isna(row.get("v_2023")):
            continue
        diff = row["change"]
        if pd.isna(diff) or diff == 0:
            continue
        y_top = max(v for v in [row["v_2021"], row["v_2023"]] if pd.notna(v))
        is_dimmed = selected_country is not None and c != selected_country
        if higher_is_worse:
            color = "#ff4757" if diff > 0 else "#00d2ff"
        else:
            color = "#00d2ff" if diff > 0 else "#ff4757"
        sign = "+" if diff > 0 else ""
        fig.add_annotation(
            x=c, y=y_top + 0.15,
            text=f"{sign}{diff:.2f}",
            showarrow=False,
            font=dict(
                size=9,
                color=color if not is_dimmed else "rgba(150,150,150,0.3)",
                family="monospace"
            ),
            xanchor="center", yanchor="bottom",
        )

    # Highlight selected country with a box
    if selected_country and selected_country in filtered_countries:
        row = comp.loc[selected_country]
        y_max = max(v for v in [row.get("v_2021", 0), row.get("v_2023", 0)] if pd.notna(v))
        fig.add_shape(
            type="rect",
            x0=filtered_countries.index(selected_country) - 0.45,
            x1=filtered_countries.index(selected_country) + 0.45,
            y0=0, y1=y_max + 0.6,
            xref="x", yref="y",
            line=dict(color="#e8ff47", width=1.5, dash="dot"),
            fillcolor="rgba(232,255,71,0.04)",
        )
        fig.add_annotation(
            x=selected_country, y=y_max + 0.8,
            text=f"◀ {selected_country}",
            showarrow=False,
            font=dict(size=9, color="#e8ff47", family="monospace"),
            xanchor="center",
        )

    fig.add_hline(y=5, line=dict(color="rgba(255,255,255,0.08)", dash="dot", width=1))

    fig.update_layout(
        barmode="overlay",
        template="plotly_dark",
        paper_bgcolor="#0e1117",
        plot_bgcolor="#0e1117",
        font=dict(family="monospace", color="#c8cad0", size=11),
        xaxis=dict(tickangle=-35, gridcolor="#1e2330", tickfont=dict(size=10)),
        yaxis=dict(
            title=f"{metric_label} (1–10)",
            gridcolor="#1e2330",
            zeroline=False,
            range=[0, 11.2],
        ),
        legend=dict(
            bgcolor="rgba(17,19,24,0.85)",
            bordercolor="#2a2f3d",
            borderwidth=1,
            orientation="h",
            yanchor="bottom", y=1.01,
            xanchor="right", x=1,
        ),
        hoverlabel=dict(
            bgcolor="#181c24",
            bordercolor="#e8ff47",
            font=dict(family="monospace", size=12),
        ),
        margin=dict(l=60, r=60, t=40, b=120),
        height=460,
    )
    return fig

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Filters")
    all_regions = sorted(set(comp_crim["Region"].dropna()) | set(comp_res["Region"].dropna()))
    selected_region = st.selectbox("Filter by Region", ["All"] + all_regions, key="scores_region_filter")

    sort_by = st.radio(
        "Sort countries by",
        ["Criminality 2021", "Criminality 2023", "Criminality change",
         "Resilience 2021",  "Resilience 2023",  "Resilience change"],
        key="scores_sort",
    )
    sort_map = {
        "Criminality 2021":   ("crim", "v_2021"),
        "Criminality 2023":   ("crim", "v_2023"),
        "Criminality change": ("crim", "change"),
        "Resilience 2021":    ("res",  "v_2021"),
        "Resilience 2023":    ("res",  "v_2023"),
        "Resilience change":  ("res",  "change"),
    }
    sort_source, sort_col = sort_map[sort_by]

    st.markdown("---")

    # Country selector — this is the main interaction driver
    all_countries = sorted(set(comp_crim.index) | set(comp_res.index))
    country_options = ["None (show all)"] + all_countries
    current_idx = 0
    if st.session_state.selected_country in all_countries:
        current_idx = all_countries.index(st.session_state.selected_country) + 1

    chosen = st.selectbox(
        "🔍 Highlight a country",
        country_options,
        index=current_idx,
        key="country_selector",
    )
    if chosen == "None (show all)":
        st.session_state.selected_country = None
    else:
        st.session_state.selected_country = chosen

    if st.button("✕ Clear selection"):
        st.session_state.selected_country = None
        st.rerun()

    st.markdown("---")
    st.markdown("🟠 Latin America")
    st.markdown("🔵 Africa")
    st.markdown("🟣 Asia/Other")
    st.markdown("⚪ Other")
    st.markdown("---")
    st.caption("Faded = 2021 · Striped = 2023\n\n🔴 label = worsened · 🔵 label = improved\n\n🟡 box = selected country")

# ── FILTER & SORT ─────────────────────────────────────────────────────────────
all_countries = sorted(set(comp_crim.index) | set(comp_res.index))

if selected_region != "All":
    all_countries = [
        c for c in all_countries
        if (c in comp_crim.index and comp_crim.loc[c, "Region"] == selected_region)
        or (c in comp_res.index  and comp_res.loc[c,  "Region"] == selected_region)
    ]

ref_comp = comp_crim if sort_source == "crim" else comp_res
valid   = [c for c in all_countries if c in ref_comp.index]
invalid = [c for c in all_countries if c not in ref_comp.index]
sorted_countries = ref_comp.loc[valid].sort_values(sort_col, ascending=False).index.tolist() + invalid

selected = st.session_state.selected_country

# ── PAGE ──────────────────────────────────────────────────────────────────────
st.title("📊 Criminality & Resilience Scores — 2021 vs 2023")

if selected:
    st.info(f"🟡 Highlighting **{selected}** across both charts. Use the sidebar or the button to clear.")
else:
    st.markdown(
        "Select a country from the **sidebar dropdown** to highlight it across both charts simultaneously. "
        "🔴 red label = worsened · 🔵 blue label = improved"
    )

# ── CRIMINALITY ───────────────────────────────────────────────────────────────
st.subheader("🔴 Criminality Score")
st.caption("Scale 1–10 · Higher = more criminal environment · Increase = negative")

crim_countries = [c for c in sorted_countries if c in comp_crim.index]
fig_crim = make_chart(comp_crim, "Criminality", higher_is_worse=True,
                      filtered_countries=crim_countries, selected_country=selected)

# Capture click events
crim_event = st.plotly_chart(fig_crim, use_container_width=True,
                              on_select="rerun", key="crim_chart")

# Handle click → update selected country
if crim_event and crim_event.get("selection", {}).get("points"):
    clicked = crim_event["selection"]["points"][0].get("x")
    if clicked:
        st.session_state.selected_country = clicked
        st.rerun()

st.divider()

# ── RESILIENCE ────────────────────────────────────────────────────────────────
st.subheader("🔵 Resilience Score")
st.caption("Scale 1–10 · Higher = stronger institutions · Increase = positive")

res_countries = [c for c in sorted_countries if c in comp_res.index]
fig_res = make_chart(comp_res, "Resilience", higher_is_worse=False,
                     filtered_countries=res_countries, selected_country=selected)

res_event = st.plotly_chart(fig_res, use_container_width=True,
                             on_select="rerun", key="res_chart")

if res_event and res_event.get("selection", {}).get("points"):
    clicked = res_event["selection"]["points"][0].get("x")
    if clicked:
        st.session_state.selected_country = clicked
        st.rerun()

# ── COUNTRY DETAIL CARD ───────────────────────────────────────────────────────
if selected:
    st.divider()
    st.subheader(f"📋 Detail: {selected}")
    c1, c2, c3, c4, c5, c6 = st.columns(6)

    if selected in comp_crim.index:
        row = comp_crim.loc[selected]
        c1.metric("Criminality 2021", f"{row['v_2021']:.2f}" if pd.notna(row['v_2021']) else "N/A")
        c2.metric("Criminality 2023", f"{row['v_2023']:.2f}" if pd.notna(row['v_2023']) else "N/A",
                  delta=f"{row['change']:+.2f}" if pd.notna(row['change']) else None,
                  delta_color="inverse")

    if selected in comp_res.index:
        row = comp_res.loc[selected]
        c3.metric("Resilience 2021", f"{row['v_2021']:.2f}" if pd.notna(row['v_2021']) else "N/A")
        c4.metric("Resilience 2023", f"{row['v_2023']:.2f}" if pd.notna(row['v_2023']) else "N/A",
                  delta=f"{row['change']:+.2f}" if pd.notna(row['change']) else None)

    region = comp_crim.loc[selected, "Region"] if selected in comp_crim.index else comp_res.loc[selected, "Region"]
    c5.metric("Region", region)
    