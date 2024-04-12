stock_sentiment_analysis = """
Classify the overall sentiment of this financial tweet/text (positive, negative, neutral). 
Additionally, identify specific emotions expressed (e.g., excitement, fear, skepticism) 
and explain how they contribute to the sentiment. The financial tweet/text is: 
"""

stock_price_analysis = """
* **Overall Trend:** Determine the primary trend over the last 30 days (upward, downward, sideways). 
* **Significant Price Movements:** Identify any major breakouts above previous resistance levels or breakdowns below support levels.
* **Support and Resistance:** Pinpoint key support and resistance areas where the price has reversed direction in the past.
* **Candlestick Patterns:** Highlight notable candlestick patterns (e.g., bullish engulfing, doji, etc.) that could signal potential trend changes or continuations.
* **Volume Trends:** Analyze changes in volume. Do volume spikes coincide with breakouts/breakdowns or trend confirmations?
* **Trading Opportunities:** Suggest potential trading opportunities based on your analysis.
* **Technical Indicators:** 
    * Calculate and interpret the 20-day and 50-day Simple Moving Averages (SMA). Are they crossed (Golden Cross/Death Cross)?
    * Calculate the Relative Strength Index (RSI). Is the stock potentially overbought (above 70) or oversold (below 30)?
    * Calculate the MACD. Analyze the relationship between the MACD line, its signal line, and the zero line for trend and momentum signals.

**Please provide a clear written summary.**
"""