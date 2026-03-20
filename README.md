# Soccer Transfer Market Inefficiency Detector
### Using Expected Possession Value (EPV) to Find Undervalued Players

## Overview

This project applies **financial market inefficiency theory** to soccer's transfer market. Just as stock markets sometimes misprice companies, soccer clubs often overpay for flashy goal-scorers while undervaluing players who build possession, create chances, and press effectively.

Using **Expected Possession Value (EPV)** — a cutting-edge metric that goes beyond traditional Expected Goals (xG) — this analysis builds a data-driven valuation model to identify players whose market price doesn't reflect their true on-pitch contribution.

## Objective

1. Build a fair-value model for soccer players using performance metrics (EPV, xG, xA, progressive carries, pressing stats)
2. Identify **undervalued** players that clubs could acquire for below their on-pitch worth
3. Quantify the **"Hype Tax"** — how social media fame inflates transfer prices
4. Analyze market efficiency across Europe's top 5 leagues
5. Construct a "Moneyball Dream Team" of the best-value players at each position

## Dataset

A curated dataset of **41 elite young players** (ages 18–26) across Europe's top 5 leagues, including:

- **Traditional stats**: goals, assists, minutes played
- **Advanced metrics**: xG/90, xA/90, EPV added/90, progressive carries, pressures
- **Market data**: market value, transfer fee, contract length
- **Off-pitch data**: social media followers, injury history, nationality

## Methodology

1. **Feature Engineering**: Selected 12 on-pitch and contextual features that capture a player's true contribution
2. **Fair Value Model**: Trained a Linear Regression model on performance metrics to estimate what each player *should* be worth based purely on their on-pitch output
3. **Value Gap Analysis**: Compared predicted fair value against actual market value to find inefficiencies
4. **EPV Efficiency Score**: Calculated EPV-per-million-euros to identify the most cost-effective players
5. **Hype Tax Analysis**: Measured the correlation between social media following and market overvaluation
6. **Segmentation**: Analyzed inefficiencies by league, age group, and injury history

## Key Findings

- **16 undervalued players** identified, led by Adam Wharton (+121% undervalued), Evan Ferguson (+92%), and Johan Bakayoko (+55%)
- **The "Hype Tax" is real**: Players with large social media followings (Bellingham 42M, Yamal 28.5M) tend to be overvalued by 15–25%
- **Premier League players are systematically undervalued** by the model (+13.8% avg gap), suggesting the league's TV money inflates performance metrics
- **Age 20–22 is the sweet spot** for finding undervalued talent — these players show the highest average positive value gap (+16.7%)
- **A hypothetical €200M investment** in the top 5 undervalued players would yield €317M in on-pitch value — a **67% return**

## Why It Matters

The global soccer transfer market exceeds **€8 billion annually**. Clubs that leverage advanced analytics like EPV to identify market inefficiencies gain a massive competitive advantage — this is the same principle that powered **Moneyball** in baseball, applied to the world's most popular sport using 2026's most advanced metrics.

As AI-driven analytics become standard in football (with clubs like Liverpool, Manchester City, and Brentford leading adoption), understanding these valuation models is essential for careers in sports analytics, finance, and data-driven decision making.

## Project Structure

```
soccer-transfer-market-inefficiency/
├── README.md
├── analysis.py              # Full analysis pipeline
├── requirements.txt         # Python dependencies
├── data/
│   ├── players_epv_market.csv    # Raw dataset
│   └── analysis_results.csv      # Output with fair values
└── docs/
    └── TEACH_ME.md          # Step-by-step learning guide
```

## Quick Start

```bash
pip install pandas numpy scikit-learn scipy
python analysis.py
```

## Future Improvements

- **Live API Integration**: Connect to Transfermarkt or FBref APIs for real-time player data
- **Machine Learning Upgrade**: Replace Linear Regression with XGBoost or Random Forest for non-linear value relationships
- **Interactive Dashboard**: Build a Streamlit app where users can filter by league, position, and budget
- **Time-Series Analysis**: Track how value gaps change over transfer windows
- **Sentiment Analysis**: Scrape transfer rumor sites to measure media hype and its effect on pricing

## Tech Stack

Python 3 | pandas | NumPy | scikit-learn | SciPy

---

*Built as a data science portfolio project — March 2026*
