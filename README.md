# Python-Based Stock Market Analysis of Major Technology Companies

## Project Overview

This repository contains a small, reproducible Python data analysis project created for **ACC102 Track 2: GitHub Data Analysis Project**. The project examines the historical stock price behaviour of five major technology companies:

- AAPL
- MSFT
- NVDA
- GOOGL
- AMZN

Using five years of daily market data from Yahoo Finance, the project focuses on simple but useful indicators of performance and risk, including price trend, daily return, cumulative return, rolling volatility, moving averages, correlation, and maximum drawdown.

## Analytical Problem

The project asks a straightforward question:

**What can five years of daily stock price data tell beginner investors or business students about the trend, risk, and return behaviour of major technology companies?**

Rather than building a prediction model, the project uses descriptive analysis to compare the five stocks and explain what the observed patterns may mean for a non-specialist audience.

## Target Audience

This analysis is intended for:

- beginner retail investors who want a simple introduction to stock performance metrics
- business students learning how Python can support financial data analysis
- classmates or instructors reviewing a clear and reproducible undergraduate assignment

## Data Source

- **Source:** Yahoo Finance, accessed through the `yfinance` library
- **Frequency:** Daily historical prices
- **Time period:** Last 5 years from the run date
- **Primary price field:** Adjusted close when available, otherwise close

Because the data is downloaded when the script or notebook is run, exact values may change slightly depending on the download date.

## Project Structure

```text
pydataproject/
├── data/
│   └── raw/
├── outputs/
│   ├── figures/
│   └── tables/
├── notebook.ipynb
├── analysis.py
├── README.md
├── requirements.txt
├── reflection_draft.md
├── demo_script.md
└── .gitignore
```

## Main Analytical Steps

1. Download five years of daily stock price data for the five selected companies.
2. Extract the adjusted close series and clean missing values.
3. Calculate daily returns and cumulative returns.
4. Measure rolling 30-day volatility.
5. Compute 20-day and 50-day moving averages.
6. Calculate the correlation matrix of daily returns.
7. Measure maximum drawdown for each stock.
8. Save figures and summary tables for reporting.

## Key Findings

The precise figures depend on the date the analysis is run, so the strongest findings should be taken from the generated notebook and output tables. In general, this project is designed to highlight a few realistic themes:

- major technology stocks can produce very different long-run returns even within the same sector
- higher-return stocks often also show larger price swings and deeper temporary losses
- technology stocks often move in the same direction, which limits diversification within a tech-only portfolio
- simple indicators such as volatility, moving averages, and drawdown can help beginners interpret risk more clearly than price alone

These are educational observations rather than investment recommendations.

## How to Run the Project

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Python script

```bash
python analysis.py
```

This downloads the latest available data, performs the analysis, and saves figures and tables in the `outputs/` folder.

### 3. Run the notebook

```bash
jupyter notebook notebook.ipynb
```

Run the notebook from top to bottom to reproduce the project in a presentation-friendly format.

## Tools and Libraries Used

- Python
- pandas
- numpy
- matplotlib
- yfinance
- Jupyter Notebook

## Limitations

- The project is based on historical prices only and does not predict future returns.
- The analysis only covers five large technology companies, so it does not represent the whole market.
- Price-based metrics do not include company fundamentals such as earnings, debt, or valuation.
- Correlations and volatility can change over time, especially during unusual market conditions.
- Yahoo Finance is convenient and widely used for learning, but it is still a secondary public data source.

## Assignment Note

This repository was created as a mini assignment submission for **ACC102 Track 2**. It aims to show a complete but manageable workflow covering data acquisition, cleaning, transformation, analysis, visualisation, and interpretation in Python.
