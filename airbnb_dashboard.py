import html

import altair as alt
import pandas as pd
import pydeck as pdk
import streamlit as st

st.set_page_config(page_title="Sydney STRA Compliance", layout="wide", page_icon="🔴")

RED = "#C8102E"
RED_DARK = "#8F0B21"
RED_SOFT = "#F4C9D0"
INK = "#1A1414"
MUTED = "#7A6E6E"
LINE = "#E8E1DF"
PAPER = "#FFFFFF"
TINT = "#F7F3F2"

# --- STYLE ---
st.markdown(
    f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=Inter+Tight:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"], .stApp {{ font-family: 'Inter Tight', sans-serif; color: {INK}; }}
.stApp {{ background: #FBEEF0; }}
#MainMenu, footer, header[data-testid="stHeader"] {{ visibility: hidden; height: 0; }}
.block-container {{ padding: 1.5rem 2.5rem 3rem; max-width: 1400px; }}

/* Sidebar */
section[data-testid="stSidebar"] {{ background: {RED_DARK}; border-right: 0; }}
section[data-testid="stSidebar"] .block-container {{ padding: 2rem 1.4rem; }}
section[data-testid="stSidebar"] label p, section[data-testid="stSidebar"] label span,
section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {{
    font-size: 0.72rem; letter-spacing: 0.08em; text-transform: uppercase;
    color: #FFFFFF !important; font-weight: 500;
}}
section[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] p {{ color: #FFFFFF !important; text-transform: none; letter-spacing: 0; font-size: 0.9rem; }}
section[data-testid="stSidebar"] [data-testid="stSliderTickBarMin"], section[data-testid="stSidebar"] [data-testid="stSliderTickBarMax"],
section[data-testid="stSidebar"] [data-testid="stSliderThumbValue"] {{ color: #FFFFFF !important; }}
.side-brand {{ font-family: 'Fraunces', serif; font-size: 1.5rem; font-weight: 600; color: #FFFFFF; line-height: 1.1; }}
.side-brand span {{ color: {RED_SOFT}; }}
.side-note {{ font-size: 0.82rem; color: {RED_SOFT}; margin: 0.5rem 0 1.6rem; line-height: 1.45; }}
span[data-baseweb="tag"] {{ background: {RED} !important; color: #fff !important; border-radius: 3px !important; }}

/* Masthead */
.hero {{ background: {RED}; color: #FFFFFF; padding: 2rem 2.4rem 2.2rem; border-radius: 6px; margin-bottom: 1.2rem;
    border-bottom: 6px solid {RED_DARK}; }}
.eyebrow {{ font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; letter-spacing: 0.14em;
    text-transform: uppercase; color: {RED_SOFT}; }}
.title {{ font-family: 'Fraunces', serif; font-weight: 600; font-size: 3rem; line-height: 1.05;
    margin: 0.35rem 0 0.6rem; letter-spacing: -0.015em; color: #FFFFFF; }}
.lede {{ font-size: 1rem; color: #FFE9EC; max-width: 46rem; line-height: 1.5; }}

/* KPIs */
.kpis {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 1.4rem; }}
.kpi {{ padding: 1.1rem 1.3rem 1.2rem; border-radius: 6px; background: #FFFFFF; border-top: 4px solid {RED}; color: {INK}; }}
.kpi .k-label {{ font-size: 0.72rem; letter-spacing: 0.08em; text-transform: uppercase; color: {MUTED}; font-weight: 500; }}
.kpi .k-value {{ font-family: 'Fraunces', serif; font-size: 2.5rem; font-weight: 500; line-height: 1.15; margin-top: 0.35rem; }}
.kpi .k-sub {{ font-size: 0.8rem; color: {MUTED}; margin-top: 0.1rem; }}
.kpi.c1 {{ background: {RED}; border-top-color: {RED_DARK}; color: #fff; }}
.kpi.c2 {{ background: {RED_DARK}; border-top-color: {RED}; color: #fff; }}
.kpi.c3 {{ background: {RED_SOFT}; border-top-color: {RED}; }}
.kpi.c1 .k-label, .kpi.c1 .k-sub, .kpi.c2 .k-label, .kpi.c2 .k-sub {{ color: #FFE0E4; }}
.kpi.c4 .k-value {{ color: {RED}; }}

/* Panels */
div[data-testid="stColumn"] {{ background: #FFFFFF; border-radius: 6px; padding: 1.1rem 1.3rem 1.3rem; }}
.sec {{ display: flex; align-items: baseline; justify-content: space-between;
    border-bottom: 2px solid {RED}; padding-bottom: 0.55rem; margin-bottom: 0.9rem; }}
.sec h3 {{ font-family: 'Fraunces', serif; font-size: 1.35rem; font-weight: 600; margin: 0; padding: 0; color: {RED_DARK}; }}
.sec .hint {{ font-size: 0.8rem; color: {MUTED}; }}

/* Host table */
.hosts {{ width: 100%; border-collapse: collapse; font-size: 0.88rem; }}
.hosts th {{ text-align: left; font-size: 0.68rem; letter-spacing: 0.08em; text-transform: uppercase;
    color: {MUTED}; font-weight: 500; padding: 0 0.5rem 0.5rem 0; border-bottom: 2px solid {RED_DARK}; }}
.hosts td {{ padding: 0.5rem 0.5rem 0.5rem 0; border-bottom: 1px solid {LINE}; vertical-align: middle; }}
.hosts .rk {{ font-family: 'JetBrains Mono', monospace; color: {MUTED}; font-size: 0.75rem; width: 1.8rem; }}
.hosts .nm {{ font-weight: 600; }}
.hosts .id {{ font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: {MUTED}; }}
.hosts .num {{ font-family: 'JetBrains Mono', monospace; text-align: right; width: 2.2rem; }}
.hosts .barcell {{ width: 38%; }}
.bar {{ height: 8px; background: {RED_SOFT}; }}
.bar > div {{ height: 100%; background: {RED}; }}
.flag {{ color: {RED}; font-weight: 600; }}
.scroll {{ max-height: 520px; overflow-y: auto; padding-right: 0.4rem; }}

.empty {{ padding: 3rem 0; color: {MUTED}; border-top: 1px solid {LINE}; }}
.foot {{ margin-top: 2.5rem; padding-top: 0.8rem; border-top: 1px solid {LINE}; font-size: 0.75rem; color: {MUTED}; }}
</style>
""",
    unsafe_allow_html=True,
)


# --- DATA ---
@st.cache_data
def load_data():
    df = pd.read_csv("listings_clean.csv", low_memory=False)
    df["estimated_revenue_l365d"] = pd.to_numeric(df["estimated_revenue_l365d"], errors="coerce").fillna(0)
    df["estimated_occupancy_l365d"] = pd.to_numeric(df["estimated_occupancy_l365d"], errors="coerce").fillna(0)
    df["calculated_host_listings_count"] = pd.to_numeric(df["calculated_host_listings_count"], errors="coerce").fillna(1)
    df["is_multi_host"] = df["calculated_host_listings_count"] > 1
    return df


try:
    df = load_data()
except FileNotFoundError:
    st.error("Could not find 'listings_clean.csv'. Place the data file in the same folder as this script.")
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.markdown('<div class="side-brand">STRA<span>.</span>Watch</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="side-note">Set the filters to narrow down the listings.</div>',
        unsafe_allow_html=True,
    )
    all_lgas = sorted(df["lga"].dropna().unique().tolist())
    selected_lgas = st.multiselect("Area (LGA)", options=all_lgas, default=[], placeholder="All areas")
    host_scale = st.radio(
        "Host scale",
        ["All Hosts", "Single-Listing (Mom & Pop)", "Multi-Listing (Commercial)"],
        index=2,
    )
    selected_license = st.selectbox(
        "Licence status", ["All", "Has License (PID-STRA)", "Exempt", "Missing/Unlicensed"], index=0
    )
    min_avail = st.slider("Min. calendar availability (days)", 0, 365, 180)

# --- FILTERS ---
f = df.copy()
if selected_lgas:
    f = f[f["lga"].isin(selected_lgas)]
if host_scale == "Single-Listing (Mom & Pop)":
    f = f[~f["is_multi_host"]]
elif host_scale == "Multi-Listing (Commercial)":
    f = f[f["is_multi_host"]]

lic = f["license"].astype(str)
if selected_license == "Exempt":
    f = f[lic.str.contains("Exempt", case=False, na=False)]
elif selected_license == "Missing/Unlicensed":
    f = f[f["license"].isna() | (lic.str.strip() == "")]
elif selected_license == "Has License (PID-STRA)":
    f = f[lic.str.contains("PID-STRA", case=False, na=False)]
f = f[f["availability_365"] >= min_avail]

# --- MASTHEAD ---
st.markdown(
    """
<div class="hero">
<div class="eyebrow">Dashboard &middot; Sydney short-term rentals</div>
<div class="title">Sydney Short-Stay<br>Market Dashboard</div>
<div class="lede">Explore who operates Sydney's short-term rentals: commercial hosts, where they cluster and how many hold a licence. Use the filters on the left.</div>
</div>
""",
    unsafe_allow_html=True,
)

# --- KPIs ---
total = len(f)
hosts = f["host_id"].nunique()
top20 = f["host_id"].value_counts().head(20).sum() if total else 0
conc = top20 / total * 100 if total else 0
unlic = int((f["license_status"] == "no license info").sum()) if total else 0


def kpi(label, value, sub, cls=""):
    return (
        f'<div class="kpi {cls}"><div class="k-label">{label}</div>'
        f'<div class="k-value">{value}</div><div class="k-sub">{sub}</div></div>'
    )


st.markdown(
    '<div class="kpis">'
    + kpi("Priority listings", f"{total:,}", f"of {len(df):,} in the dataset", "c1")
    + kpi("Unique hosts", f"{hosts:,}", f"{total / hosts:.1f} listings per host" if hosts else "&nbsp;", "c2")
    + kpi("Held by top 20 hosts", f"{top20:,}", "listings in this view", "c3")
    + kpi("Top-20 concentration", f"{conc:.1f}%", f"{unlic:,} listings with no licence info", "c4")
    + "</div>",
    unsafe_allow_html=True,
)

if total == 0:
    st.markdown('<div class="empty">No listings match the current filters. Loosen one of them in the sidebar.</div>', unsafe_allow_html=True)
    st.stop()

# --- MAP + HOSTS ---
col_map, col_hosts = st.columns([3, 2], gap="large")

with col_map:
    st.markdown(
        '<div class="sec"><h3>Where they cluster</h3><span class="hint">Each dot is one listing</span></div>',
        unsafe_allow_html=True,
    )
    pts = f[["latitude", "longitude", "host_id"]].dropna()
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=pts,
        get_position="[longitude, latitude]",
        get_fill_color=[200, 16, 46, 120],
        get_radius=90,
        radius_min_pixels=2,
        radius_max_pixels=8,
    )
    view = pdk.ViewState(latitude=pts["latitude"].median(), longitude=pts["longitude"].median(), zoom=10.3)
    st.pydeck_chart(
        pdk.Deck(layers=[layer], initial_view_state=view, map_style="light", height=520),
        width="stretch",
    )

with col_hosts:
    st.markdown(
        '<div class="sec"><h3>Top 20 hosts</h3><span class="hint">By listings in view</span></div>',
        unsafe_allow_html=True,
    )
    g = f.groupby("host_id")
    top = (
        g.agg(
            name=("host_name", "first"),
            n=("id", "count"),
            nolic=("license_status", lambda s: (s == "no license info").sum()),
        )
        .sort_values("n", ascending=False)
        .head(20)
        .reset_index()
    )
    mx = top["n"].max()
    rows = ""
    for i, r in enumerate(top.itertuples(), 1):
        flag = f' <span class="flag">&middot; {r.nolic} unlicensed</span>' if r.nolic else ""
        rows += (
            f'<tr><td class="rk">{i:02d}</td>'
            f'<td><div class="nm">{html.escape(str(r.name))}</div>'
            f'<div class="id">{r.host_id}{flag}</div></td>'
            f'<td class="barcell"><div class="bar"><div style="width:{r.n / mx * 100:.0f}%"></div></div></td>'
            f'<td class="num">{r.n}</td></tr>'
        )
    st.markdown(
        f'<div class="scroll"><table class="hosts"><thead><tr><th></th><th>Host</th><th></th>'
        f'<th style="text-align:right">Listings</th></tr></thead><tbody>{rows}</tbody></table></div>',
        unsafe_allow_html=True,
    )

# --- BREAKDOWNS ---
st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
c1, c2 = st.columns([3, 2], gap="large")


def style(chart, h):
    return (
        chart.properties(height=h)
        .configure_view(strokeWidth=0)
        .configure_axis(
            labelFont="Inter Tight", titleFont="Inter Tight", labelColor=MUTED, titleColor=MUTED,
            domainColor=LINE, tickColor=LINE, gridColor=LINE, labelFontSize=12,
        )
        .configure_axisY(grid=False)
    )


with c1:
    st.markdown(
        '<div class="sec"><h3>Listings by area</h3><span class="hint">Ten busiest LGAs in view</span></div>',
        unsafe_allow_html=True,
    )
    lga = f["lga"].value_counts().head(10).rename_axis("lga").reset_index(name="listings")
    bars = alt.Chart(lga).mark_bar(color=RED, size=14).encode(
        y=alt.Y("lga:N", sort="-x", title=None),
        x=alt.X("listings:Q", title=None),
        tooltip=["lga", "listings"],
    )
    labels = bars.mark_text(align="left", dx=5, font="JetBrains Mono", fontSize=11, color=INK).encode(text="listings:Q")
    st.altair_chart(style(bars + labels, 300), width="stretch")

with c2:
    st.markdown(
        '<div class="sec"><h3>Licence status</h3><span class="hint">Share of listings in view</span></div>',
        unsafe_allow_html=True,
    )
    ls = f["license_status"].value_counts().rename_axis("status").reset_index(name="listings")
    ls["share"] = ls["listings"] / ls["listings"].sum()
    colors = {"registered (PID-STRA)": INK, "self-declared exempt": RED_SOFT, "no license info": RED}
    chart = alt.Chart(ls).mark_bar(size=14).encode(
        y=alt.Y("status:N", sort="-x", title=None),
        x=alt.X("share:Q", title=None, axis=alt.Axis(format="%")),
        color=alt.Color(
            "status:N", legend=None,
            scale=alt.Scale(domain=list(colors), range=list(colors.values())),
        ),
        tooltip=["status", "listings", alt.Tooltip("share:Q", format=".1%")],
    )
    st.altair_chart(style(chart, 300), width="stretch")

st.markdown(
    '<div class="foot">Source: listings_clean.csv. Priority = filters set in the sidebar. '
    '"Unlicensed" = no licence information on the listing.</div>',
    unsafe_allow_html=True,
)
