# Interview Talk Track — Soccer Transfer Market Inefficiency Detector

## The 2-Minute Version (for "Tell me about a project you've worked on")

"I built a data model that finds undervalued soccer players — basically applying the same logic as value investing in finance to the transfer market. The idea came from noticing that clubs spend billions on transfers but often overpay for big-name players while missing guys who quietly make their team better.

I used a metric called Expected Possession Value, or EPV, which measures how much a player improves their team's chance of scoring during every moment of play — not just when they shoot. Traditional stats like goals and assists miss a lot. A midfielder who never scores but constantly moves the ball into dangerous positions has high EPV, and the market tends to undervalue those players.

I built a regression model that estimates what a player should be worth based purely on their on-pitch output, then compared that to their actual market value. The gap between the two is the inefficiency. I found 16 undervalued players out of 41 — and the most undervalued ones tended to be creative midfielders and possession-builders, not flashy scorers. I also found that social media following correlates with being overpriced, which I called the 'Hype Tax.'

The biggest thing I learned was that the model I first chose — linear regression — didn't work well on a small dataset. The cross-validation score was actually negative, which means the model was worse than just guessing the average. That taught me that picking the right technique for your data size matters more than picking a fancy technique."

## Follow-Up Questions They Might Ask

**"Why did you choose this topic?"**
"I love soccer and I'm interested in finance, and I realized the transfer market is basically a financial market with the same kinds of inefficiencies — information asymmetry, hype-driven pricing, and irrational behavior. It felt like a natural place to combine things I care about."

**"What would you do differently?"**
"Three things. First, I'd use a larger dataset — 41 players wasn't enough for the model to generalize. Second, I'd try a Random Forest or XGBoost instead of linear regression, because they handle non-linear relationships better on small data. Third, I'd pull real data from an API like FBref instead of generating synthetic data."

**"What did you learn that surprised you?"**
"That the model failing was actually the most valuable part. Seeing a negative R² forced me to understand what cross-validation actually does and why you can't trust a model that only looks good on training data. Most tutorials only show you the success case — but learning what failure looks like is what made me a better analyst."

**"How is EPV different from expected goals?"**
"xG only measures the quality of shots — it tells you the probability that a specific shot goes in. EPV is broader. It measures how every action a player takes — passes, dribbles, movement, pressing — changes their team's probability of scoring. So a player who never shoots can still have a very high EPV if they're consistently putting the ball in dangerous areas."

**"Could this actually be used by a real club?"**
"The concept absolutely is — clubs like Liverpool, Manchester City, and Brentford already use similar models for recruitment. My version is simplified, but the framework is the same: use performance data to find players the market underprices, and avoid overpaying for brand names."

## Key Numbers to Remember
- 41 players analyzed across 5 leagues
- 16 found to be undervalued, 16 overvalued
- Top undervalued: Adam Wharton at +121% below fair value
- Hype Tax correlation: -0.24 (more followers → more overvalued)
- A €200M investment in top 5 undervalued = €317M in on-pitch value (67% ROI)
