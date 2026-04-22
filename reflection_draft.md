# Reflection Draft

## Analytical Problem and Intended Audience

In this project, I wanted to look at a simple but useful question: what can historical stock price data tell us about the performance and risk of major technology companies? I chose this topic because stock prices are easy to understand at a basic level, but at the same time they can be analysed in different ways using Python. Instead of trying to predict future prices, I focused on describing past trends clearly and comparing the behaviour of five well-known companies.

The main audience I had in mind was beginner retail investors and business students. I did not want the project to become too technical, because that would make it harder to explain and less suitable for an ACC102 mini assignment. For that reason, I kept the analysis focused on a few core ideas such as return, volatility, correlation, and drawdown. These are simple enough to explain, but still useful for understanding how stocks behave over time.

## Why I Chose This Dataset

I used Yahoo Finance data through the `yfinance` library because it is free, easy to access, and practical for a student project. One reason I liked it is that someone else can run the same code later without needing a paid database or API key. That makes the project more reproducible and more suitable for GitHub.

I chose five years of daily data for Apple, Microsoft, NVIDIA, Alphabet, and Amazon. I selected these companies because they are large technology firms that most people already know, so the project feels more relevant and easier to follow. I also thought five companies was a reasonable number: enough to compare different patterns, but not so many that the project would become messy.

## Python Methods Used

The workflow was fairly straightforward. First, I downloaded the daily stock data using `yfinance`. Then I cleaned it and extracted the adjusted closing price series. After that, I calculated daily returns, cumulative returns, rolling 30-day volatility, 20-day and 50-day moving averages, the correlation matrix, and maximum drawdown. I also created a summary table to compare the main statistics across the five stocks.

For visualisation, I used `matplotlib` only. I wanted the charts to be clear and readable rather than overly styled. The output includes a price trend chart, cumulative return comparison, daily return distributions, rolling volatility chart, moving average chart, and a correlation heatmap. I think these visuals made the results easier to understand than using tables alone.

## Main Insights Produced

The project showed quite clearly that the five stocks did not behave in the same way, even though they all belong to the technology sector. The most striking result was that NVIDIA had by far the strongest total return over the five-year period, but it also had the highest volatility and the deepest maximum drawdown. That made the risk-return trade-off very visible.

Another useful finding was that the stocks were generally positively correlated. This means that owning only large technology stocks may not provide as much diversification as some beginners might expect. I also found that looking at cumulative return was much more informative than looking at price level alone, because it showed the relative growth of each stock from the starting point.

## Limitations and Reliability Issues

There are a few important limitations in this project. First, it is based only on historical price data, so it cannot predict future performance. Second, it only includes five large technology companies, so the conclusions should not be applied to the whole stock market. Third, it focuses on price behaviour and does not include company fundamentals such as earnings, valuation, or debt.

There were also some practical reliability issues during the project. At one point, the Yahoo Finance download failed and returned empty data. I had to adjust the script so that it handled download problems more clearly and more robustly. This reminded me that working with real data is not always smooth, and part of data analysis is dealing with those practical issues rather than only writing formulas.

## Personal Learning and Decision-Making

One thing I learned from this project is that simple analysis can still be meaningful if it is done carefully. At the start, I considered whether I should include more advanced techniques, but I decided that would make the project less focused. In the end, I think keeping the scope manageable was the right decision.

I also learned that cleaning and structuring data is just as important as making charts. If the adjusted closing prices had been extracted incorrectly, the later calculations would not have been reliable. Another lesson for me was that interpretation should stay moderate. It is easy to make strong claims from a chart, but in a finance-related project it is better to explain patterns carefully and acknowledge uncertainty.

Overall, this project helped me understand how Python can be used for a complete data analysis workflow, from downloading data to producing final outputs for GitHub. It also gave me a better sense of how return and risk should be considered together, rather than separately.

## AI Use Disclosure

AI-assisted support was used during this project for code structuring, debugging, markdown drafting, and improving the presentation of the repository files. This included support with the Python script, notebook structure, README writing, and reflection drafting.

My own role was to decide the project topic, review the outputs, run the code locally, check whether the results made sense, and choose what should finally be included in the repository. I also reviewed the written content and adjusted it to fit the assignment.

Before final submission, I should complete the details below so the disclosure is accurate:

- **Date(s) of AI use:** [add date]
- **Tool/model used:** [add tool or model name]
- **How AI was used:** [brief summary]
- **What I personally checked or changed:** [brief summary]
