"""
Soccer Transfer Market Inefficiency Dashboard
Interactive tool to explore player valuations using EPV analytics.
Deploy: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler

# ── Page Config ──
st.set_page_config(
    page_title="Transfer Market Inefficiency Detector",
    page_icon="⚽",
    layout="wide"
)

st.title("⚽ Soccer Transfer Market Inefficiency Detector")
st.markdown("*Using Expected Possession Value (EPV) to find undervalued players the market misprices.*")
st.markdown("---")

# ── Load Data ──
@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv("data/players_epv_market.csv")
    return df

@st.cache_data
def run_model(df: pd.DataFrame) -> pd.DataFrame:
    features = [
        'age', 'epv_added_per90', 'xg_per90', 'xa_per90',
        'progressive_carries_per90', 'pressures_per90',
        'pass_completion_pct', 'minutes_played',
        'goals', 'assists', 'contract_years_remaining',
        'injury_days_last_season'
    ]
    X = df[features].copy()
    y = df['market_value_eur_millions'].copy()

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = Ridge(alpha=10.0)
    model.fit(X_scaled, y)

    df = df.copy()
    df['fair_value'] = model.predict(X_scaled).clip(min=5)
    df['value_gap_pct'] = ((df['fair_value'] - df['market_value_eur_millions']) / df['market_value_eur_millions'] * 100)
    df['epv_per_million'] = df['epv_added_per90'] / df['market_value_eur_millions']

    df['status'] = df['value_gap_pct'].apply(
        lambda x: '🟢 Undervalued' if x > 10
        else ('🔴 Overvalued' if x < -10 else '⚪ Fair')
    )
    return df

df = load_data()
df = run_model(df)

# ── Sidebar Filters ──
st.sidebar.header("🔍 Filters")

leagues = st.sidebar.multiselect(
    "League",
    options=sorted(df['league'].unique()),
    default=sorted(df['league'].unique())
)

positions = st.sidebar.multiselect(
    "Position",
    options=sorted(df['position'].unique()),
    default=sorted(df['position'].unique())
)

age_range = st.sidebar.slider(
    "Age Range",
    min_value=int(df['age'].min()),
    max_value=int(df['age'].max()),
    value=(int(df['age'].min()), int(df['age'].max()))
)

max_budget = st.sidebar.slider(
    "Max Budget (€M)",
    min_value=10,
    max_value=200,
    value=200,
    step=5
)

# ── Apply Filters ──
filtered = df[
    (df['league'].isin(leagues)) &
    (df['position'].isin(positions)) &
    (df['age'] >= age_range[0]) &
    (df['age'] <= age_range[1]) &
    (df['market_value_eur_millions'] <= max_budget)
]

# ── Key Metrics ──
col1, col2, col3, col4 = st.columns(4)
col1.metric("Players Shown", len(filtered))
col2.metric("Avg Market Value", f"€{filtered['market_value_eur_millions'].mean():.0f}M")
col3.metric("Avg Fair Value", f"€{filtered['fair_value'].mean():.0f}M")
undervalued_count = len(filtered[filtered['value_gap_pct'] > 10])
col4.metric("Undervalued Players", undervalued_count)

st.markdown("---")

# ── Main Table ──
tab1, tab2, tab3 = st.tabs(["📊 All Players", "🟢 Best Bargains", "🔥 Hype Tax"])

with tab1:
    st.subheader("Player Valuations")
    display_cols = [
        'player_name', 'age', 'position', 'league', 'club',
        'market_value_eur_millions', 'fair_value', 'value_gap_pct',
        'epv_added_per90', 'status'
    ]
    st.dataframe(
        filtered[display_cols]
        .sort_values('value_gap_pct', ascending=False)
        .rename(columns={
            'player_name': 'Player',
            'age': 'Age',
            'position': 'Pos',
            'league': 'League',
            'club': 'Club',
            'market_value_eur_millions': 'Market (€M)',
            'fair_value': 'Fair Value (€M)',
            'value_gap_pct': 'Gap %',
            'epv_added_per90': 'EPV/90',
            'status': 'Status'
        })
        .style.format({'Market (€M)': '€{:.0f}M', 'Fair Value (€M)': '€{:.1f}M', 'Gap %': '{:+.1f}%', 'EPV/90': '{:.2f}'}),
        use_container_width=True,
        hide_index=True
    )

with tab2:
    st.subheader("🟢 Most Undervalued Players")
    st.markdown("*Players whose on-pitch production exceeds their market price.*")
    bargains = filtered[filtered['value_gap_pct'] > 5].sort_values('value_gap_pct', ascending=False)
    for _, row in bargains.iterrows():
        with st.container():
            c1, c2, c3, c4 = st.columns([3, 2, 2, 2])
            c1.markdown(f"**{row['player_name']}** ({row['position']}, {row['club']})")
            c2.metric("Market", f"€{row['market_value_eur_millions']:.0f}M")
            c3.metric("Fair Value", f"€{row['fair_value']:.1f}M")
            c4.metric("Undervalued By", f"{row['value_gap_pct']:+.0f}%")

with tab3:
    st.subheader("🔥 The Hype Tax")
    st.markdown("*Players with the biggest gap between social media fame and on-pitch value.*")

    hype = filtered.copy()
    hype['hype_score'] = hype['social_media_followers_millions'] * (-hype['value_gap_pct'].clip(upper=0) / 100)
    hype = hype.nlargest(10, 'hype_score')

    for _, row in hype.iterrows():
        with st.container():
            c1, c2, c3, c4 = st.columns([3, 2, 2, 2])
            c1.markdown(f"**{row['player_name']}** ({row['club']})")
            c2.metric("Followers", f"{row['social_media_followers_millions']:.1f}M")
            c3.metric("Overvalued By", f"{row['value_gap_pct']:+.0f}%")
            c4.metric("Hype Tax Score", f"{row['hype_score']:.1f}")

# ── League Comparison ──
st.markdown("---")
st.subheader("📈 League-Level Market Efficiency")

league_stats = filtered.groupby('league').agg(
    avg_market=('market_value_eur_millions', 'mean'),
    avg_fair=('fair_value', 'mean'),
    avg_gap=('value_gap_pct', 'mean'),
    avg_epv=('epv_added_per90', 'mean'),
    count=('player_name', 'count')
).round(1)

st.dataframe(
    league_stats.rename(columns={
        'avg_market': 'Avg Market (€M)',
        'avg_fair': 'Avg Fair Value (€M)',
        'avg_gap': 'Avg Gap %',
        'avg_epv': 'Avg EPV/90',
        'count': 'Players'
    }),
    use_container_width=True
)

# ── Footer ──
st.markdown("---")
st.markdown(
    "*Built by Gabe Cardona | Data from 2025-26 season | "
    "[GitHub](https://github.com/Gmoney250/soccer-transfer-market-inefficiency)*"
)
