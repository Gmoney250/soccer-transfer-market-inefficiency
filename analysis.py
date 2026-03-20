"""
=================================================================
Soccer Transfer Market Inefficiency Detector
Using Expected Possession Value (EPV) to Find Undervalued Players
=================================================================

This project applies financial market inefficiency theory to soccer's
transfer market. Using EPV (a cutting-edge metric beyond xG), we build
a data-driven valuation model to identify players whose market price
doesn't reflect their on-pitch contribution.

Author: Gabe Cardona | Portfolio Project
Date: March 2026
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# STEP 1: Load and Explore the Dataset
# ============================================================
print("=" * 70)
print("SOCCER TRANSFER MARKET INEFFICIENCY DETECTOR")
print("Using EPV Analytics to Find Undervalued Players")
print("=" * 70)

df = pd.read_csv("data/players_epv_market.csv")

print(f"\n📊 Dataset Overview:")
print(f"   Players analyzed: {len(df)}")
print(f"   Leagues covered: {df['league'].nunique()} ({', '.join(df['league'].unique())})")
print(f"   Positions: {', '.join(df['position'].unique())}")
print(f"   Average age: {df['age'].mean():.1f} years")
print(f"   Total market value: €{df['market_value_eur_millions'].sum():.0f}M")

# ============================================================
# STEP 2: Build the EPV-Based Valuation Model
# ============================================================
print("\n" + "=" * 70)
print("STEP 2: Building EPV-Based Fair Value Model")
print("=" * 70)

# Features that drive a player's TRUE on-pitch value
value_features = [
    'age', 'epv_added_per90', 'xg_per90', 'xa_per90',
    'progressive_carries_per90', 'pressures_per90',
    'pass_completion_pct', 'minutes_played',
    'goals', 'assists', 'contract_years_remaining',
    'injury_days_last_season'
]

X = df[value_features].copy()
y = df['market_value_eur_millions'].copy()

# Scale features for fair comparison
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train a regression model to estimate "fair" market value
model = LinearRegression()
model.fit(X_scaled, y)

# Cross-validation to check model reliability
cv_scores = cross_val_score(model, X_scaled, y, cv=5, scoring='r2')
print(f"\n   Model R² (cross-validated): {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")

# Feature importance: which factors drive market value most?
feature_importance = pd.DataFrame({
    'Feature': value_features,
    'Coefficient': model.coef_
}).sort_values('Coefficient', key=abs, ascending=False)

print(f"\n   Top Value Drivers (by coefficient magnitude):")
for _, row in feature_importance.head(6).iterrows():
    direction = "↑" if row['Coefficient'] > 0 else "↓"
    print(f"   {direction} {row['Feature']}: {row['Coefficient']:.2f}")

# ============================================================
# STEP 3: Calculate Fair Value & Market Inefficiency
# ============================================================
print("\n" + "=" * 70)
print("STEP 3: Detecting Market Inefficiencies")
print("=" * 70)

df['predicted_fair_value'] = model.predict(X_scaled)
df['predicted_fair_value'] = df['predicted_fair_value'].clip(lower=5)  # Floor at 5M

df['value_gap_eur_millions'] = df['predicted_fair_value'] - df['market_value_eur_millions']
df['value_gap_pct'] = (df['value_gap_eur_millions'] / df['market_value_eur_millions']) * 100

# Classify players
df['market_status'] = pd.cut(
    df['value_gap_pct'],
    bins=[-np.inf, -20, -5, 5, 20, np.inf],
    labels=['Significantly Overvalued', 'Slightly Overvalued',
            'Fairly Valued', 'Slightly Undervalued', 'Significantly Undervalued']
)

# ============================================================
# STEP 4: EPV Efficiency Score
# ============================================================
print("\n" + "=" * 70)
print("STEP 4: EPV Efficiency Ranking")
print("=" * 70)

# EPV per million euro of market value — who gives you the most bang for your buck?
df['epv_per_million'] = df['epv_added_per90'] / df['market_value_eur_millions']
df['epv_efficiency_rank'] = df['epv_per_million'].rank(ascending=False).astype(int)

print(f"\n   🏆 Top 10 Most Cost-Efficient Players (EPV per €M):")
print(f"   {'Player':<25} {'EPV/90':<10} {'Market(€M)':<12} {'EPV/€M':<10} {'Position'}")
print(f"   {'-'*75}")

top_efficient = df.nsmallest(10, 'epv_efficiency_rank')
for _, row in top_efficient.iterrows():
    print(f"   {row['player_name']:<25} {row['epv_added_per90']:<10.2f} "
          f"€{row['market_value_eur_millions']:<11.0f} {row['epv_per_million']:<10.4f} "
          f"{row['position']}")

# ============================================================
# STEP 5: Undervalued Player Detection
# ============================================================
print("\n" + "=" * 70)
print("STEP 5: Undervalued Player Report")
print("=" * 70)

undervalued = df[df['value_gap_pct'] > 5].sort_values('value_gap_pct', ascending=False)

print(f"\n   🔍 Found {len(undervalued)} undervalued players:\n")
print(f"   {'Player':<25} {'Market(€M)':<12} {'Fair Val(€M)':<14} {'Gap %':<10} {'Status'}")
print(f"   {'-'*85}")

for _, row in undervalued.iterrows():
    print(f"   {row['player_name']:<25} €{row['market_value_eur_millions']:<11.0f} "
          f"€{row['predicted_fair_value']:<13.1f} {row['value_gap_pct']:>+8.1f}%  "
          f"{row['market_status']}")

# ============================================================
# STEP 6: Overvalued Player Detection
# ============================================================
print("\n" + "=" * 70)
print("STEP 6: Overvalued Player Report")
print("=" * 70)

overvalued = df[df['value_gap_pct'] < -5].sort_values('value_gap_pct')

print(f"\n   ⚠️  Found {len(overvalued)} overvalued players:\n")
print(f"   {'Player':<25} {'Market(€M)':<12} {'Fair Val(€M)':<14} {'Gap %':<10} {'Status'}")
print(f"   {'-'*85}")

for _, row in overvalued.iterrows():
    print(f"   {row['player_name']:<25} €{row['market_value_eur_millions']:<11.0f} "
          f"€{row['predicted_fair_value']:<13.1f} {row['value_gap_pct']:>+8.1f}%  "
          f"{row['market_status']}")

# ============================================================
# STEP 7: "Moneyball" Dream Team — Best Value XI
# ============================================================
print("\n" + "=" * 70)
print("STEP 7: Moneyball Dream Team (Best Value XI)")
print("=" * 70)

# Pick the most undervalued player per position group
position_groups = {
    'GK': ['GK'],
    'CB': ['CB'],
    'FB': ['LB', 'RB'],
    'CM': ['CM', 'CDM'],
    'AM': ['AM'],
    'Wing': ['LW', 'RW'],
    'CF': ['CF']
}

print(f"\n   Best value player per position group:")
print(f"   {'Position':<10} {'Player':<25} {'Market(€M)':<12} {'Fair Val(€M)':<14} {'Gap %'}")
print(f"   {'-'*75}")

for group_name, positions in position_groups.items():
    group_df = df[df['position'].isin(positions)]
    if len(group_df) > 0:
        best = group_df.loc[group_df['value_gap_pct'].idxmax()]
        print(f"   {group_name:<10} {best['player_name']:<25} "
              f"€{best['market_value_eur_millions']:<11.0f} "
              f"€{best['predicted_fair_value']:<13.1f} {best['value_gap_pct']:>+8.1f}%")

# ============================================================
# STEP 8: The "Hype Tax" — Social Media vs. On-Pitch Value
# ============================================================
print("\n" + "=" * 70)
print("STEP 8: The Hype Tax — Social Media Inflation Analysis")
print("=" * 70)

# Correlation between social media followers and overvaluation
from scipy import stats

corr, p_value = stats.pearsonr(
    df['social_media_followers_millions'],
    df['value_gap_pct']
)

print(f"\n   Correlation between social media followers and value gap: {corr:.3f}")
print(f"   P-value: {p_value:.4f}")
print(f"   Interpretation: {'Statistically significant' if p_value < 0.05 else 'Not statistically significant'}")

# Players with highest "hype tax" (high followers + overvalued)
df['hype_score'] = df['social_media_followers_millions'] * (-df['value_gap_pct'] / 100)
hype_tax = df.nlargest(5, 'hype_score')

print(f"\n   🔥 Players with Highest 'Hype Tax' (social fame inflating price):")
for _, row in hype_tax.iterrows():
    print(f"   {row['player_name']:<25} Followers: {row['social_media_followers_millions']:.1f}M  "
          f"Value Gap: {row['value_gap_pct']:+.1f}%")

# ============================================================
# STEP 9: League-Level Inefficiency Analysis
# ============================================================
print("\n" + "=" * 70)
print("STEP 9: League-Level Market Efficiency")
print("=" * 70)

league_stats = df.groupby('league').agg(
    avg_market_value=('market_value_eur_millions', 'mean'),
    avg_fair_value=('predicted_fair_value', 'mean'),
    avg_epv=('epv_added_per90', 'mean'),
    avg_gap_pct=('value_gap_pct', 'mean'),
    player_count=('player_name', 'count')
).round(2)

print(f"\n   {'League':<20} {'Avg Market(€M)':<16} {'Avg Fair(€M)':<14} "
      f"{'Avg EPV/90':<12} {'Avg Gap %':<12} {'Players'}")
print(f"   {'-'*85}")

for league, row in league_stats.iterrows():
    print(f"   {league:<20} €{row['avg_market_value']:<15.1f} "
          f"€{row['avg_fair_value']:<13.1f} {row['avg_epv']:<12.2f} "
          f"{row['avg_gap_pct']:>+10.1f}%  {row['player_count']:.0f}")

# ============================================================
# STEP 10: Age-Value Curve Analysis
# ============================================================
print("\n" + "=" * 70)
print("STEP 10: Age-Value Depreciation Curve")
print("=" * 70)

age_groups = df.groupby(pd.cut(df['age'], bins=[17, 20, 22, 24, 27])).agg(
    avg_market_value=('market_value_eur_millions', 'mean'),
    avg_epv=('epv_added_per90', 'mean'),
    avg_gap_pct=('value_gap_pct', 'mean'),
    count=('player_name', 'count')
).round(2)

print(f"\n   {'Age Group':<15} {'Avg Market(€M)':<16} {'Avg EPV/90':<12} "
      f"{'Avg Gap %':<12} {'Count'}")
print(f"   {'-'*60}")

for age_range, row in age_groups.iterrows():
    print(f"   {str(age_range):<15} €{row['avg_market_value']:<15.1f} "
          f"{row['avg_epv']:<12.2f} {row['avg_gap_pct']:>+10.1f}%  "
          f"{row['count']:.0f}")

# ============================================================
# STEP 11: Injury Risk Discount Analysis
# ============================================================
print("\n" + "=" * 70)
print("STEP 11: Injury Risk Discount Factor")
print("=" * 70)

df['injury_category'] = pd.cut(
    df['injury_days_last_season'],
    bins=[-1, 5, 20, 50, 200],
    labels=['Minimal (0-5 days)', 'Moderate (6-20)', 'Significant (21-50)', 'Severe (50+)']
)

injury_analysis = df.groupby('injury_category', observed=True).agg(
    avg_market=('market_value_eur_millions', 'mean'),
    avg_fair=('predicted_fair_value', 'mean'),
    avg_gap=('value_gap_pct', 'mean'),
    count=('player_name', 'count')
).round(2)

print(f"\n   {'Injury Risk':<25} {'Avg Market(€M)':<16} {'Avg Fair(€M)':<14} "
      f"{'Avg Gap %':<12} {'Count'}")
print(f"   {'-'*75}")

for cat, row in injury_analysis.iterrows():
    print(f"   {str(cat):<25} €{row['avg_market']:<15.1f} "
          f"€{row['avg_fair']:<13.1f} {row['avg_gap']:>+10.1f}%  "
          f"{row['count']:.0f}")

# ============================================================
# FINAL SUMMARY
# ============================================================
print("\n" + "=" * 70)
print("FINAL SUMMARY")
print("=" * 70)

print(f"""
   📈 Model Performance: R² = {cv_scores.mean():.3f}
   💰 Total players analyzed: {len(df)}
   🟢 Undervalued players found: {len(undervalued)}
   🔴 Overvalued players found: {len(overvalued)}
   ⚖️  Fairly valued players: {len(df) - len(undervalued) - len(overvalued)}

   💡 Key Insight: EPV (Expected Possession Value) reveals player
      contributions that traditional market pricing misses.
      Clubs overpay for goals/hype and underpay for possession-
      building, progressive play, and defensive pressing.

   🏦 Investment Thesis: A club spending €200M on the top 5 most
      undervalued players would get €{undervalued.head(5)['predicted_fair_value'].sum():.0f}M in
      on-pitch value — a {((undervalued.head(5)['predicted_fair_value'].sum() / undervalued.head(5)['market_value_eur_millions'].sum()) - 1) * 100:.0f}% return on investment.
""")

# Save results
output_df = df[['player_name', 'age', 'position', 'league', 'club',
                 'market_value_eur_millions', 'epv_added_per90',
                 'predicted_fair_value', 'value_gap_eur_millions',
                 'value_gap_pct', 'market_status', 'epv_per_million',
                 'epv_efficiency_rank']].sort_values('value_gap_pct', ascending=False)

output_df.to_csv("data/analysis_results.csv", index=False)
print("   ✅ Full results saved to data/analysis_results.csv")
print("=" * 70)
