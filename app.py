import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import base64
from pathlib import Path

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="High Bickington Flow – Wales & West Utilities",
    page_icon="logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------
# BRAND COLOURS (HYDROSTAR + DARK THEME)
# ------------------------------------------------------
PRIMARY_COLOUR = "#a7d730"   # HydroStar primary green
SECONDARY_COLOUR = "#499823"  # HydroStar secondary green
DARK_GREY = "#30343c"
LIGHT_GREY = "#8c919a"
BACKGROUND = "#0e1117"
PANEL_BG = "#1b222b"
TEXT_COL = "#f2f4f7"
SUBTEXT_COL = LIGHT_GREY
ACCENT_COLOUR = "#86d5f8"

COLOUR_MAP = {
    "Flow (Kscmh) F1": PRIMARY_COLOUR,
    "Flow (Kscmh) F2": SECONDARY_COLOUR,
    "Flow (Kscmh) F3": ACCENT_COLOUR,
}

# ------------------------------------------------------
# GLOBAL CSS TO FORCE DARK UI
# ------------------------------------------------------
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Hind:wght@300;400;500;600;700&display=swap');

    :root {{
        --hs-primary: {PRIMARY_COLOUR};
        --hs-secondary: {SECONDARY_COLOUR};
        --hs-bg: {BACKGROUND};
        --hs-card: {PANEL_BG};
        --hs-text: {TEXT_COL};
        --hs-subtext: {SUBTEXT_COL};
        --hs-sidebar: {DARK_GREY};
    }}

    html, body, [class*="css"] {{
        font-family: 'Hind', sans-serif;
    }}

    .stApp {{
        background:
            radial-gradient(circle at top right, rgba(167, 215, 48, 0.11) 0%, rgba(14, 17, 23, 0) 35%),
            radial-gradient(circle at bottom left, rgba(134, 213, 248, 0.08) 0%, rgba(14, 17, 23, 0) 40%),
            var(--hs-bg);
        color: var(--hs-text);
    }}
    .block-container {{
        padding-top: 1.8rem;
        padding-bottom: 2rem;
        color: var(--hs-text);
    }}
    h1, h2, h3, h4, h5, h6 {{
        color: var(--hs-text) !important;
        font-weight: 700;
        letter-spacing: 0.1px;
    }}
    p, span, label {{
        color: var(--hs-text) !important;
    }}
    .stCaption, .stMarkdown small {{
        color: var(--hs-subtext) !important;
    }}
    /* sidebar */
    section[data-testid="stSidebar"] > div {{
        background-color: var(--hs-sidebar);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }}
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown span,
    section[data-testid="stSidebar"] label {{
        color: #ffffff !important;
    }}
    /* input controls */
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div,
    div[data-baseweb="textarea"] > div {{
        background-color: rgba(255, 255, 255, 0.06);
        border-color: rgba(255, 255, 255, 0.16);
    }}
    .stDateInput > div > div,
    .stMultiSelect > div > div,
    .stSelectbox > div > div {{
        background-color: rgba(255, 255, 255, 0.06);
    }}
    .stSlider > div > div > div {{
        background-color: rgba(167, 215, 48, 0.18);
    }}
    .stSlider [data-testid="stTickBar"] > div {{
        background-color: rgba(167, 215, 48, 0.40);
    }}
    .st-bx, .stTextInput, .stNumberInput, .stDateInput, .stSelectbox, .stMultiSelect {{
        color: var(--hs-text) !important;
    }}
    .stButton > button {{
        background-color: var(--hs-primary);
        color: #1d2430;
        font-weight: 700;
        border: none;
        border-radius: 8px;
    }}
    .stButton > button:hover {{
        background-color: var(--hs-secondary);
        color: #ffffff;
    }}
    /* KPI cards */
    div[data-testid="metric-container"] {{
        background: linear-gradient(180deg, rgba(27, 34, 43, 0.96) 0%, rgba(22, 29, 37, 0.96) 100%);
        border: 1px solid rgba(255, 255, 255, 0.10);
        border-left: 5px solid var(--hs-primary);
        border-radius: 12px;
        padding: 0.85rem 1rem;
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.24);
    }}
    div[data-testid="metric-container"] label {{
        color: var(--hs-subtext) !important;
        font-size: 0.86rem !important;
        letter-spacing: 0.35px;
        text-transform: uppercase;
    }}
    div[data-testid="metric-container"] [data-testid="stMetricValue"] {{
        color: var(--hs-text) !important;
        font-weight: 700;
        line-height: 1.1;
    }}
    /* dataframes */
    div[data-testid="stDataFrame"] {{
        background-color: rgba(27, 34, 43, 0.96);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 0.2rem;
    }}
    .stPlotlyChart {{
        background-color: rgba(27, 34, 43, 0.45);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 12px;
        padding: 0.55rem 1.45rem 0.25rem 0.55rem;
        margin-bottom: 1.1rem;
        box-sizing: border-box;
    }}
    .hero-banner {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 1.2rem;
        padding: 1.1rem 1.25rem;
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.12);
        background: linear-gradient(
            90deg,
            rgba(12, 16, 24, 0.90) 0%,
            rgba(18, 30, 22, 0.88) 72%,
            rgba(29, 52, 33, 0.78) 100%
        );
        margin-bottom: 1.4rem;
    }}
    .hero-copy {{
        max-width: 68%;
    }}
    .hero-title {{
        margin: 0;
        color: var(--hs-text);
        font-size: clamp(2.0rem, 2.8vw, 2.8rem);
        line-height: 1.1;
        font-weight: 700;
    }}
    .hero-subtitle {{
        margin: 0.45rem 0 0 0;
        color: var(--hs-subtext);
        font-size: 1rem;
    }}
    .hero-logos {{
        display: flex;
        align-items: center;
        justify-content: flex-end;
        gap: 1rem;
        flex-wrap: nowrap;
    }}
    .hero-logos img {{
        height: 112px;
        width: auto;
        object-fit: contain;
        filter: drop-shadow(0 6px 14px rgba(0, 0, 0, 0.35));
    }}
    @media (max-width: 1080px) {{
        .hero-banner {{
            flex-direction: column;
            align-items: flex-start;
        }}
        .hero-copy {{
            max-width: 100%;
        }}
        .hero-logos {{
            justify-content: flex-start;
        }}
        .hero-logos img {{
            height: 88px;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ======================================================
# DATA LOADING
# ======================================================
@st.cache_data
def load_data():
    df = pd.read_parquet("High_Bickington_cleaned.parquet")
    # Ensure DateTimeIndex
    if not isinstance(df.index, pd.DatetimeIndex):
        # try common column name
        for col in ["Time", "Datetime", "timestamp"]:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], utc=True)
                df = df.set_index(col)
                break
        else:
            df.index = pd.to_datetime(df.index, utc=True)
    df = df.sort_index()
    return df

df = load_data()


def encode_logo_to_base64(path: Path):
    if not path.exists():
        return ""
    return base64.b64encode(path.read_bytes()).decode("utf-8")

# ======================================================
# SIDEBAR FILTERS
# ======================================================
min_date = df.index.min().date()
max_date = df.index.max().date()

st.sidebar.caption("Drag both handles to set the date window")
start_date, end_date = st.sidebar.slider(
    "Date range",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date),
    format="YYYY-MM-DD",
)

mask = (df.index.date >= start_date) & (df.index.date <= end_date)
df = df.loc[mask]

all_cols = list(df.columns)
selected_cols = st.sidebar.multiselect(
    "Select flow sensors",
    options=all_cols,
    default=all_cols,
)

if not selected_cols:
    st.sidebar.error("Please select at least one flow series.")
    st.stop()

df = df[selected_cols]

st.sidebar.markdown(
    f"<p style='color:{SUBTEXT_COL}; font-size:0.9rem;'>Records (filtered): "
    f"<span style='color:{TEXT_COL}; font-weight:600;'>{len(df):,}</span><br>"
    f"{df.index.min().date()} → {df.index.max().date()}</p>",
    unsafe_allow_html=True,
)

# ======================================================
# HEADER
# ======================================================
hs_logo_b64 = encode_logo_to_base64(Path("logo.png"))
wwu_logo_b64 = encode_logo_to_base64(Path("wwu.png"))

logo_html_parts = []
if hs_logo_b64:
    logo_html_parts.append(f'<img src="data:image/png;base64,{hs_logo_b64}" alt="HydroStar logo">')
if wwu_logo_b64:
    logo_html_parts.append(f'<img src="data:image/png;base64,{wwu_logo_b64}" alt="Wales and West Utilities logo">')

st.markdown(
    f"""
    <div class="hero-banner">
        <div class="hero-copy">
            <h1 class="hero-title">High Bickington Flow</h1>
            <p class="hero-subtitle">HydroStar × Wales &amp; West Utilities</p>
        </div>
        <div class="hero-logos">
            {''.join(logo_html_parts)}
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ======================================================
# SUMMARY STATISTICS
# ======================================================
st.markdown("## Summary statistics")

start_ts = df.index.min().strftime("%Y-%m-%d %H:%M")
end_ts = df.index.max().strftime("%Y-%m-%d %H:%M")

st.caption("Current filter KPIs")
metric_col1, metric_col2, metric_col3 = st.columns(3)
with metric_col1:
    st.metric("Start date", start_ts)
with metric_col2:
    st.metric("End date", end_ts)
with metric_col3:
    st.metric("Total records (filtered)", f"{len(df):,}")

st.markdown("#### Descriptive statistics by flow sensor")
desc = df.describe().T
st.dataframe(
    desc.style.format(
        {
            "count": "{:,.0f}",
            "mean": "{:,.4f}",
            "std": "{:,.4f}",
            "min": "{:,.4f}",
            "25%": "{:,.4f}",
            "50%": "{:,.4f}",
            "75%": "{:,.4f}",
            "max": "{:,.4f}",
        }
    ),
    use_container_width=True,
    height=min(350, 80 + 28 * len(desc)),
)

# ======================================================
# HELPER: DARK PLOTLY LAYOUT
# ======================================================
def apply_dark_layout(fig, title):
    fig.update_layout(
        title=dict(text=title, font=dict(size=20, color=TEXT_COL, family="Hind, sans-serif")),
        template="plotly_dark",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color=TEXT_COL, family="Hind, sans-serif"),
        colorway=[PRIMARY_COLOUR, SECONDARY_COLOUR, ACCENT_COLOUR, "#f59e0b", "#e11d48"],
        legend=dict(bgcolor="rgba(0,0,0,0)", orientation="h", yanchor="bottom", y=1.02, x=0),
        margin=dict(l=66, r=72, t=78, b=62),
        hovermode="x unified",
    )
    fig.update_xaxes(
        gridcolor="rgba(255,255,255,0.08)",
        linecolor="rgba(255,255,255,0.18)",
        automargin=True,
    )
    fig.update_yaxes(
        gridcolor="rgba(255,255,255,0.08)",
        linecolor="rgba(255,255,255,0.18)",
        automargin=True,
    )
    return fig

# ======================================================
# 1. Flow trend over time (no rolling)
# ======================================================
st.markdown("## Flow trend over time")

# 1) Choose level of detail
agg_choice = st.selectbox(
    "Time resolution",
    options=["30 minutes", "Hourly", "Daily", "Weekly"],
    index=1,  # default to Hourly
)

freq_map = {
    "30 minutes": "30min",
    "Hourly": "H",
    "Daily": "D",
    "Weekly": "W",
}
freq = freq_map[agg_choice]

# Aggregate
resampled = df.resample(freq).mean()

fig_hourly = go.Figure()
for col in resampled.columns:
    base_col = COLOUR_MAP.get(col, "#6366f1")
    fig_hourly.add_trace(
        go.Scatter(
            x=resampled.index,
            y=resampled[col],
            mode="lines",
            name=f"{col} ({agg_choice} average)",
            line=dict(color=base_col, width=2),
        )
    )

fig_hourly.update_layout(
    xaxis_title="Time",
    yaxis_title="Flow (Kscmh)",
    xaxis=dict(rangeslider=dict(visible=True)),
)

fig_hourly = apply_dark_layout(
    fig_hourly,
    f"Flow trend – {agg_choice.lower()} averages"
)

st.plotly_chart(fig_hourly, use_container_width=True)



# ======================================================
# 2. DAILY AVERAGES
# ======================================================
st.markdown("## Daily average flow")

daily = df.resample("D").mean()
fig_daily = go.Figure()
for col in daily.columns:
    fig_daily.add_trace(
        go.Scatter(
            x=daily.index,
            y=daily[col],
            mode="lines",
            name=col.split()[-1],
            line=dict(color=COLOUR_MAP.get(col, "#6366f1"), width=2.5),
        )
    )

fig_daily.update_layout(
    xaxis_title="Year",
    yaxis_title="Flow (Kscmh)",
)
fig_daily = apply_dark_layout(fig_daily, "High Bickington Gas Flow (Daily Average)")
st.plotly_chart(fig_daily, use_container_width=True)

# ======================================================
# 3. MONTHLY SEASONALITY (TS)
# ======================================================
st.markdown("## Monthly average flow (multi‑year seasonality)")

monthly = df.resample("M").mean()
fig_monthly = go.Figure()
for col in monthly.columns:
    fig_monthly.add_trace(
        go.Scatter(
            x=monthly.index,
            y=monthly[col],
            mode="lines",
            name=col,
            line=dict(color=COLOUR_MAP.get(col, "#6366f1"), width=2.5),
        )
    )

fig_monthly.update_layout(
    xaxis_title="Year",
    yaxis_title="Flow (Kscmh)",
)
fig_monthly = apply_dark_layout(fig_monthly, "Monthly Average Flow (Seasonality)")
st.plotly_chart(fig_monthly, use_container_width=True)

# ======================================================
# 4. AVERAGE FLOW BY CALENDAR MONTH
# ======================================================
st.markdown("## Average flow by calendar month (2019–2025)")

monthly_pattern = df.groupby(df.index.month).mean()
monthly_pattern.index = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                         "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

fig_mpat = go.Figure()
for col in monthly_pattern.columns:
    fig_mpat.add_trace(
        go.Scatter(
            x=monthly_pattern.index,
            y=monthly_pattern[col],
            mode="lines+markers",
            name=col,
            line=dict(color=COLOUR_MAP.get(col, "#6366f1"), width=3),
            marker=dict(size=8),
        )
    )

fig_mpat.update_layout(
    xaxis_title="Month",
    yaxis_title="Flow (Kscmh)",
)
fig_mpat = apply_dark_layout(fig_mpat, "Average Flow by Month (2019–2025)")
st.plotly_chart(fig_mpat, use_container_width=True)

# ======================================================
# 5. AVERAGE FLOW BY HOUR OF DAY
# ======================================================
st.markdown("## Average flow by hour of day")

hourly_pattern = df.groupby(df.index.hour).mean()
fig_hpat = go.Figure()
for col in hourly_pattern.columns:
    fig_hpat.add_trace(
        go.Scatter(
            x=hourly_pattern.index,
            y=hourly_pattern[col],
            mode="lines+markers",
            name=col,
            line=dict(color=COLOUR_MAP.get(col, "#6366f1"), width=2.5),
            marker=dict(size=7),
        )
    )

fig_hpat.update_layout(
    xaxis_title="Hour",
    yaxis_title="Flow (Kscmh)",
)
fig_hpat = apply_dark_layout(fig_hpat, "Average Flow by Hour of Day")
st.plotly_chart(fig_hpat, use_container_width=True)

# ======================================================
# 6. YEARLY DISTRIBUTION (BOXPLOTS)
# ======================================================
st.markdown("## Distribution of daily flow by year")

df_year = df.resample("D").mean()
df_year["Year"] = df_year.index.year

fig_box = go.Figure()
for col in df_year.columns:
    if col == "Year":
        continue
    fig_box.add_trace(
        go.Box(
            x=df_year["Year"],
            y=df_year[col],
            name=col,
            marker_color=COLOUR_MAP.get(col, "#6366f1"),
            boxmean=True,
        )
    )

fig_box.update_layout(
    xaxis_title="Year",
    yaxis_title="Flow (Kscmh)",
)
fig_box = apply_dark_layout(fig_box, "Distribution of Daily Flow by Year")
st.plotly_chart(fig_box, use_container_width=True)

# ======================================================
# 7. CORRELATION HEATMAP
# ======================================================
st.markdown("## Correlation between flow sensors")

corr = df.corr()

fig_corr = px.imshow(
    corr,
    text_auto=True,
    color_continuous_scale=[
        [0.0, ACCENT_COLOUR],
        [0.5, PANEL_BG],
        [1.0, PRIMARY_COLOUR],
    ],
    aspect="auto",
)

fig_corr.update_layout(
    xaxis_title="",
    yaxis_title="",
)
fig_corr = apply_dark_layout(fig_corr, "Correlation Between Flow Sensors")
st.plotly_chart(fig_corr, use_container_width=True)

# ======================================================
# RAW DATA
# ======================================================
with st.expander("Show raw data (first 500 rows)"):
    st.dataframe(df.head(500), use_container_width=True)
