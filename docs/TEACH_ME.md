# How This Project Works — A Step-by-Step Guide

## What We're Doing (The Big Picture)

Imagine you're a soccer club's director of football with a €200M transfer budget. You want to sign the best players, but the market is irrational — some players are overpriced because they're famous, and some gems are hidden because they don't score flashy goals.

This project builds a **pricing model** (like a stock valuation model in finance) that estimates what a player is truly worth based on their **on-pitch performance data**, then compares that to their actual market price. The gap between the two is the "market inefficiency" — and that's where smart clubs make their money.

---

## Key Concepts You Need to Know

### 1. Expected Possession Value (EPV)

**What it is**: EPV measures how much a player increases their team's probability of scoring during every moment they're involved in a possession. Unlike xG (which only measures shots), EPV captures *everything* — passes, dribbles, movement, defensive work.

**Why it matters**: A midfielder who never shoots but constantly moves the ball into dangerous areas has high EPV. Traditional stats miss these players completely. EPV is the frontier of football analytics in 2026.

**How to think about it**: If xG tells you "this shot had a 20% chance of going in," EPV tells you "this player's involvement in play increased the team's chance of scoring by 0.87 per 90 minutes." It's a much fuller picture.

### 2. Market Value vs. Fair Value

**Market value** = what the market says a player is worth (influenced by hype, age, nationality, league, social media, etc.)

**Fair value** = what our model says a player is worth based purely on performance data

**Value gap** = Fair Value - Market Value. Positive = undervalued. Negative = overvalued.

### 3. Linear Regression (The Model)

**What it does**: Draws the "best fit line" through the relationship between player performance features and their market value. It learns: "For every +0.1 increase in EPV/90, market value tends to increase by X million euros."

**Why we use it**: It's interpretable. You can see exactly which features drive value and by how much. For a portfolio project, this transparency matters more than a black-box neural network.

**The R² score** tells you how much of the market value variation the model explains. A score of 0.7 means the model explains 70% of why some players cost more than others.

---

## The Calculations, Explained

### EPV Efficiency Score
```
EPV per Million = EPV_added_per90 / market_value_eur_millions
```
This is like **price-to-earnings ratio** in stocks. A player with EPV/90 of 0.68 who costs €18M (Pellistri) gives you 0.0378 EPV per million — the best bang for your buck. A player with EPV/90 of 0.87 who costs €180M (Yamal) gives you only 0.0048 EPV per million.

### Value Gap Percentage
```
Value Gap % = ((Fair Value - Market Value) / Market Value) × 100
```
Adam Wharton's fair value is €77.5M but his market price is €35M. That's a +121% gap — the model says the market is pricing him at less than half his on-pitch worth.

### The Hype Tax (Pearson Correlation)
```
r = correlation(social_media_followers, value_gap_percent)
```
We found r = -0.238, meaning more followers weakly correlates with being overvalued. The negative sign means: more famous → more likely to be overpriced. The p-value of 0.13 means this isn't statistically significant at the 95% level, but the trend is there — with more data, this would likely become significant.

---

## How to Read the Results

### Undervalued Players
If a player shows +50% value gap, it means the market prices them at roughly half what their on-pitch metrics justify. This could be because they play for a smaller club, don't score flashy goals, or lack social media presence.

### Overvalued Players
If a player shows -25% value gap, the market overprices them by about a quarter. This often correlates with brand value (Bellingham, Yamal) or playing for a mega-club.

### League Efficiency
The Premier League showing +13.8% average undervaluation suggests that PL players systematically outperform their price tags — likely because the league's competitive intensity pushes higher performance metrics.

---

## What to Look For if You Build Something Like This Again

1. **Check your R² score** — if it's very low, your features may not capture what drives market value
2. **Watch for overfitting** — if training R² is great but cross-validation is bad, the model memorized instead of learned
3. **Feature selection matters** — adding social media followers as a feature (instead of analyzing it separately) would have made the model "learn" the hype tax and hide it
4. **Always cross-validate** — never trust a single train/test split
5. **Domain knowledge beats algorithms** — knowing that EPV matters more than raw goals is what makes this analysis meaningful

---

## Concepts This Project Teaches

| Concept | Where It Shows Up |
|---------|-------------------|
| Linear Regression | Fair value model |
| Cross-Validation | Model reliability check |
| Feature Engineering | Selecting EPV, xG, xA as inputs |
| Market Efficiency Theory | From finance, applied to transfers |
| Correlation Analysis | Hype Tax (social media vs. value) |
| Segmentation Analysis | By league, age, injury |
| Data-Driven Decision Making | Moneyball Dream Team |
| Statistical Significance | P-values in hype analysis |

---

*This guide is part of the Soccer Transfer Market Inefficiency Detector project — March 2026*
