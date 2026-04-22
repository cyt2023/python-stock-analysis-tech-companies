# Reflection Draft

## Analytical Problem and Intended Audience

This project was designed around a practical question: how can historical stock price data be analysed in Python to help people understand differences in return and risk across major technology companies? I wanted the analysis to be useful for beginner retail investors and business students rather than experienced finance professionals. Because of that, I focused on clear, interpretable metrics instead of highly technical modelling. The aim was not to recommend which stock to buy, but to show how data analysis can support a more informed view of market behaviour.

The chosen audience influenced both the scope and presentation. A beginner audience is more likely to benefit from visual comparisons, short explanations, and familiar company names. For that reason, I selected five large technology firms that are widely known: Apple, Microsoft, NVIDIA, Alphabet, and Amazon. These companies are often discussed in financial news, so they provide a useful starting point for explaining ideas such as volatility, cumulative return, and drawdown in a way that feels relevant.

## Why This Dataset Was Chosen

I selected Yahoo Finance data through the `yfinance` package because it is easy to access, free to use, and practical for a small student project. It also allows the analysis to be reproduced on a normal laptop without requiring an API key or a paid data subscription. That was important because the project brief emphasised a GitHub-ready submission that other people could run themselves.

I chose a five-year period of daily prices because it is long enough to show meaningful changes over time without making the dataset unnecessarily large. A shorter period might miss larger market cycles, while a much longer period could make the project more difficult to explain clearly. Daily data also provides enough detail to calculate returns and rolling volatility while remaining manageable for an introductory analysis.

## Python Methods Used

The project followed a simple data analysis workflow. First, I downloaded the stock data using `yfinance`. Then I handled the column structure returned by the library, because stock downloads can come back with multi-index columns. After extracting adjusted close prices, I cleaned the data by sorting the index, forward-filling isolated missing values, and dropping any remaining incomplete rows.

Next, I transformed the data into a set of measures that could be compared across the five companies. These included daily returns, cumulative returns, rolling 30-day volatility, 20-day and 50-day moving averages, the correlation matrix of daily returns, and maximum drawdown. I also created a summary table that combined starting price, ending price, total return, average daily return, annualised volatility, and maximum drawdown.

For visualisation, I used `matplotlib` only. This kept the project simple and aligned with the assignment requirements. The figures were designed to answer slightly different questions: price trend charts show broad movement over time, cumulative return charts allow clearer performance comparison, return distributions show how daily movements vary, rolling volatility highlights risk over time, moving averages show trend direction, and the correlation heatmap summarises how closely the stocks move together.

## Main Insights Produced

The exact numerical results depend on the date the project is run, but the analysis is intended to generate several useful types of insight. First, it shows that even within the same sector, stock performance can differ substantially over a five-year period. This helps illustrate that it is not enough to think only in terms of “technology stocks” as one single group.

Second, the project makes the trade-off between return and risk more visible. A stock with stronger cumulative growth may also display higher rolling volatility and a more severe maximum drawdown. This is useful for beginner investors because strong performance can appear attractive until the downside risk is visualised alongside it.

Third, the correlation analysis highlights that these companies are all part of the same broad sector and may react to similar market conditions. That means holding several large technology stocks does not automatically create strong diversification. This is a useful lesson for students learning portfolio concepts.

## Limitations and Reliability Issues

There are several limitations that should be recognised. The most important is that this is a historical analysis. It explains what happened in the past, but it does not forecast future stock prices. Markets are affected by changing economic conditions, regulation, company strategy, and investor sentiment, so the past is only a partial guide.

Another limitation is the narrow dataset. The project only considers five large technology companies, which means the conclusions should not be generalised to all sectors or all firms. In addition, the analysis uses price-based indicators only. It does not include financial statement data, valuation ratios, dividends in a broader sense, macroeconomic indicators, or company-specific news.

There are also reliability issues related to the source and download process. Yahoo Finance is widely used for educational work, but it remains a public secondary source. If the internet connection fails or Yahoo Finance is temporarily unavailable, the analysis cannot run until the data is downloaded successfully. For that reason, I wrote the script so that download failures produce a clear error message rather than a confusing result.

## Personal Learning and Decision-Making

One of the main things I learned from this project was the importance of balancing ambition with clarity. At the start, it would have been easy to add more technical indicators or attempt a forecasting model, but that would have made the project less coherent and harder to explain. I decided that a smaller, well-executed analysis would be more appropriate for an undergraduate assignment.

I also learned that data preparation matters as much as the final charts. A project can look polished, but if the underlying price series is extracted incorrectly, all later calculations become unreliable. Handling the `yfinance` column structure carefully helped me appreciate how small technical decisions affect the overall quality of an analysis.

Another useful lesson was that interpretation should stay moderate. It is tempting to make strong claims when visual patterns look obvious, but a more responsible approach is to describe what the data shows while recognising uncertainty and limitations. That is especially important in a financial context.

## AI Use Disclosure

This document is a draft and should be edited to match my final submission.

AI-assisted support was used during the planning, coding, and drafting stages of this project. The support included help with structuring the Python workflow, improving code readability, generating markdown drafts, and refining explanations for the notebook and repository files.

Suggested details to complete before submission:

- **Date(s) of AI use:** [add date]
- **Tool/model used:** [add tool or model name]
- **How AI was used:** [briefly describe what support was provided]
- **What I checked myself:** [briefly describe your own review, testing, and editing]

The final interpretation, review, and submission decisions should remain my own responsibility.
