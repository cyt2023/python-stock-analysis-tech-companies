"""
ACC102 Track 2 mini assignment:
Python-based stock market analysis of major technology companies.

This script downloads five years of daily stock data for AAPL, MSFT, NVDA,
GOOGL, and AMZN, prepares a clean price table, computes simple risk/return
metrics, and saves figures and summary tables for a GitHub-ready submission.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf
import warnings

try:
    from urllib3.exceptions import NotOpenSSLWarning
except Exception:  # pragma: no cover - fallback for unusual urllib3 installs
    NotOpenSSLWarning = None

TICKERS = ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN"]
PERIOD = "5y"
TRADING_DAYS = 252

BASE_DIR = Path(__file__).resolve().parent
RAW_DIR = BASE_DIR / "data" / "raw"
FIGURES_DIR = BASE_DIR / "outputs" / "figures"
TABLES_DIR = BASE_DIR / "outputs" / "tables"

PRICE_LABEL = "Adj Close"
ROLLING_VOL_WINDOW = 30
SHORT_MA = 20
LONG_MA = 50

if NotOpenSSLWarning is not None:
    warnings.filterwarnings("ignore", category=NotOpenSSLWarning)


def ensure_directories() -> None:
    """Create required project folders if they do not already exist."""
    for folder in (RAW_DIR, FIGURES_DIR, TABLES_DIR):
        folder.mkdir(parents=True, exist_ok=True)


def download_stock_data(tickers: list[str], period: str = PERIOD) -> pd.DataFrame:
    """
    Download historical daily stock data from Yahoo Finance.

    The function keeps the raw structure returned by yfinance so that the
    extraction logic can explicitly handle both multi-index and single-index
    column layouts.
    """
    batch_error: Exception | None = None

    try:
        data = yf.download(
            tickers=tickers,
            period=period,
            interval="1d",
            auto_adjust=False,
            group_by="column",
            progress=False,
            threads=False,
        )
        if not data.empty:
            return data
    except Exception as exc:
        batch_error = exc

    print("Batch download was unsuccessful. Retrying with one ticker at a time...")

    frames: list[pd.DataFrame] = []
    failed_tickers: list[str] = []

    for ticker in tickers:
        try:
            ticker_data = yf.download(
                tickers=ticker,
                period=period,
                interval="1d",
                auto_adjust=False,
                group_by="column",
                progress=False,
                threads=False,
            )
            if ticker_data.empty:
                failed_tickers.append(ticker)
                continue

            if not isinstance(ticker_data.columns, pd.MultiIndex):
                ticker_data.columns = pd.MultiIndex.from_product(
                    [ticker_data.columns, [ticker]]
                )

            frames.append(ticker_data)
        except Exception:
            failed_tickers.append(ticker)

    if frames:
        combined = pd.concat(frames, axis=1).sort_index(axis=1)
        if len(failed_tickers) > 0:
            print(
                "Downloaded partial data. Failed tickers: "
                + ", ".join(failed_tickers)
            )
        return combined

    if batch_error is not None:
        raise RuntimeError(
            "Data download failed. Yahoo Finance returned no usable data. "
            "This is usually caused by a temporary Yahoo Finance issue, "
            "network restrictions, or an unstable local Python/SSL setup."
        ) from batch_error

    raise RuntimeError(
        "Yahoo Finance returned an empty dataset. Please verify your "
        "internet connection or try again later."
    )


def extract_price_data(raw_data: pd.DataFrame, tickers: list[str]) -> pd.DataFrame:
    """
    Extract adjusted close prices, or close prices if adjusted data is absent.
    """
    if isinstance(raw_data.columns, pd.MultiIndex):
        level_0 = list(raw_data.columns.get_level_values(0))
        price_field = "Adj Close" if "Adj Close" in level_0 else "Close"
        prices = raw_data[price_field].copy()
    else:
        candidate = "Adj Close" if "Adj Close" in raw_data.columns else "Close"
        prices = raw_data[[candidate]].copy()
        if len(tickers) == 1:
            prices.columns = tickers

    missing_tickers = [ticker for ticker in tickers if ticker not in prices.columns]
    if missing_tickers:
        raise ValueError(
            "The downloaded price table is missing expected tickers: "
            + ", ".join(missing_tickers)
        )

    prices = prices[tickers].sort_index()
    prices.index = pd.to_datetime(prices.index)
    return prices


def clean_price_data(prices: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the price table with a conservative approach suitable for daily data.

    Missing values are forward-filled because some market data feeds contain
    isolated blanks. Any remaining rows with missing values are removed.
    """
    cleaned = prices.copy().ffill().dropna(how="any")
    if cleaned.empty:
        raise ValueError("No usable price data remains after cleaning.")
    return cleaned


def compute_daily_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """Compute simple daily returns."""
    return prices.pct_change().dropna(how="any")


def compute_cumulative_returns(daily_returns: pd.DataFrame) -> pd.DataFrame:
    """Compute cumulative growth relative to the first available trading day."""
    return (1 + daily_returns).cumprod() - 1


def compute_rolling_volatility(daily_returns: pd.DataFrame, window: int = ROLLING_VOL_WINDOW) -> pd.DataFrame:
    """Compute annualized rolling volatility using a 30-day window by default."""
    return daily_returns.rolling(window=window).std() * np.sqrt(TRADING_DAYS)


def compute_moving_averages(prices: pd.DataFrame, short_window: int = SHORT_MA, long_window: int = LONG_MA) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Compute short and long moving average tables."""
    ma_short = prices.rolling(window=short_window).mean()
    ma_long = prices.rolling(window=long_window).mean()
    return ma_short, ma_long


def compute_drawdown(prices: pd.DataFrame) -> pd.DataFrame:
    """Compute drawdown series for each stock."""
    running_peak = prices.cummax()
    return prices.div(running_peak).sub(1)


def compute_max_drawdown(prices: pd.DataFrame) -> pd.Series:
    """Compute the most severe drawdown observed for each stock."""
    return compute_drawdown(prices).min()


def build_summary_table(prices: pd.DataFrame, daily_returns: pd.DataFrame) -> pd.DataFrame:
    """Build a concise comparison table for risk and return metrics."""
    summary = pd.DataFrame(
        {
            "Start Price ($)": prices.iloc[0],
            "End Price ($)": prices.iloc[-1],
            "Total Return (%)": (prices.iloc[-1] / prices.iloc[0] - 1) * 100,
            "Average Daily Return (%)": daily_returns.mean() * 100,
            "Annualized Volatility (%)": daily_returns.std() * np.sqrt(TRADING_DAYS) * 100,
            "Maximum Drawdown (%)": compute_max_drawdown(prices) * 100,
        }
    )
    return summary.round(2)


def save_table(df: pd.DataFrame, filename: str) -> Path:
    """Save a dataframe to the tables folder and return the path."""
    path = TABLES_DIR / filename
    df.to_csv(path)
    return path


def format_axes(ax: plt.Axes, title: str, ylabel: str) -> None:
    """Apply a consistent style across figures."""
    ax.set_title(title, fontsize=13, fontweight="bold")
    ax.set_xlabel("Date")
    ax.set_ylabel(ylabel)
    ax.grid(alpha=0.3)


def plot_price_trend(prices: pd.DataFrame) -> Path:
    fig, ax = plt.subplots(figsize=(12, 6))
    for ticker in prices.columns:
        ax.plot(prices.index, prices[ticker], linewidth=1.8, label=ticker)
    format_axes(ax, "Technology Stock Price Trend", "Price ($)")
    ax.legend()
    fig.tight_layout()
    path = FIGURES_DIR / "01_price_trend.png"
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return path


def plot_cumulative_returns(cumulative_returns: pd.DataFrame) -> Path:
    fig, ax = plt.subplots(figsize=(12, 6))
    for ticker in cumulative_returns.columns:
        ax.plot(cumulative_returns.index, cumulative_returns[ticker] * 100, linewidth=1.8, label=ticker)
    format_axes(ax, "Cumulative Return Comparison", "Cumulative Return (%)")
    ax.axhline(0, color="black", linewidth=0.8)
    ax.legend()
    fig.tight_layout()
    path = FIGURES_DIR / "02_cumulative_returns.png"
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return path


def plot_daily_return_distributions(daily_returns: pd.DataFrame) -> Path:
    fig, axes = plt.subplots(2, 3, figsize=(14, 8))
    axes = axes.flatten()

    for index, ticker in enumerate(daily_returns.columns):
        axes[index].hist(
            daily_returns[ticker] * 100,
            bins=40,
            color="steelblue",
            edgecolor="white",
            alpha=0.85,
        )
        axes[index].set_title(ticker, fontweight="bold")
        axes[index].set_xlabel("Daily Return (%)")
        axes[index].set_ylabel("Frequency")
        axes[index].grid(alpha=0.3, axis="y")

    axes[-1].set_visible(False)
    fig.suptitle("Distribution of Daily Returns", fontsize=13, fontweight="bold")
    fig.tight_layout()
    path = FIGURES_DIR / "03_daily_return_distributions.png"
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return path


def plot_rolling_volatility(rolling_volatility: pd.DataFrame) -> Path:
    fig, ax = plt.subplots(figsize=(12, 6))
    for ticker in rolling_volatility.columns:
        ax.plot(rolling_volatility.index, rolling_volatility[ticker] * 100, linewidth=1.8, label=ticker)
    format_axes(ax, "30-Day Rolling Volatility", "Annualized Volatility (%)")
    ax.legend()
    fig.tight_layout()
    path = FIGURES_DIR / "04_rolling_volatility.png"
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return path


def plot_moving_average_chart(prices: pd.DataFrame, ma20: pd.DataFrame, ma50: pd.DataFrame, ticker: str = "AAPL") -> Path:
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(prices.index, prices[ticker], linewidth=1.5, label=f"{ticker} Price")
    ax.plot(ma20.index, ma20[ticker], linewidth=1.8, label="20-Day MA")
    ax.plot(ma50.index, ma50[ticker], linewidth=1.8, label="50-Day MA")
    format_axes(ax, f"{ticker} Price with Moving Averages", "Price ($)")
    ax.legend()
    fig.tight_layout()
    path = FIGURES_DIR / "05_aapl_moving_averages.png"
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return path


def plot_correlation_heatmap(correlation_matrix: pd.DataFrame) -> Path:
    fig, ax = plt.subplots(figsize=(7, 6))
    image = ax.imshow(correlation_matrix, cmap="coolwarm", vmin=-1, vmax=1)
    ax.set_xticks(np.arange(len(correlation_matrix.columns)))
    ax.set_yticks(np.arange(len(correlation_matrix.index)))
    ax.set_xticklabels(correlation_matrix.columns)
    ax.set_yticklabels(correlation_matrix.index)
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

    for row in range(len(correlation_matrix.index)):
        for col in range(len(correlation_matrix.columns)):
            value = correlation_matrix.iloc[row, col]
            ax.text(col, row, f"{value:.2f}", ha="center", va="center", color="black")

    ax.set_title("Correlation of Daily Returns", fontsize=13, fontweight="bold")
    fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04, label="Correlation")
    fig.tight_layout()
    path = FIGURES_DIR / "06_correlation_heatmap.png"
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return path


def run_analysis() -> dict[str, pd.DataFrame | pd.Series | Path]:
    """Run the full workflow and return key objects for reuse in the notebook."""
    ensure_directories()

    raw_data = download_stock_data(TICKERS, PERIOD)
    price_data = clean_price_data(extract_price_data(raw_data, TICKERS))
    daily_returns = compute_daily_returns(price_data)
    cumulative_returns = compute_cumulative_returns(daily_returns)
    rolling_volatility = compute_rolling_volatility(daily_returns)
    ma20, ma50 = compute_moving_averages(price_data)
    correlation_matrix = daily_returns.corr()
    drawdown = compute_drawdown(price_data)
    max_drawdown = compute_max_drawdown(price_data)
    summary_table = build_summary_table(price_data, daily_returns)

    raw_prices_path = RAW_DIR / "technology_stock_prices.csv"
    price_data.to_csv(raw_prices_path)

    summary_path = save_table(summary_table, "summary_statistics.csv")
    save_table(correlation_matrix.round(3), "correlation_matrix.csv")
    save_table((max_drawdown * 100).round(2).to_frame(name="Maximum Drawdown (%)"), "maximum_drawdown.csv")

    figure_paths = [
        plot_price_trend(price_data),
        plot_cumulative_returns(cumulative_returns),
        plot_daily_return_distributions(daily_returns),
        plot_rolling_volatility(rolling_volatility),
        plot_moving_average_chart(price_data, ma20, ma50, ticker="AAPL"),
        plot_correlation_heatmap(correlation_matrix),
    ]

    return {
        "prices": price_data,
        "daily_returns": daily_returns,
        "cumulative_returns": cumulative_returns,
        "rolling_volatility": rolling_volatility,
        "ma20": ma20,
        "ma50": ma50,
        "correlation_matrix": correlation_matrix,
        "drawdown": drawdown,
        "max_drawdown": max_drawdown,
        "summary_table": summary_table,
        "raw_prices_path": raw_prices_path,
        "summary_path": summary_path,
        "figure_paths": figure_paths,
    }


def print_console_summary(results: dict[str, pd.DataFrame | pd.Series | Path]) -> None:
    """Print a short terminal summary after the workflow finishes."""
    prices = results["prices"]
    summary_table = results["summary_table"]
    assert isinstance(prices, pd.DataFrame)
    assert isinstance(summary_table, pd.DataFrame)

    print("\nStock market analysis completed successfully.")
    print(f"Date range: {prices.index.min().date()} to {prices.index.max().date()}")
    print(f"Stocks analysed: {', '.join(prices.columns)}")
    print("\nSummary statistics:")
    print(summary_table.to_string())
    print(f"\nFigures saved to: {FIGURES_DIR}")
    print(f"Tables saved to: {TABLES_DIR}")


def main() -> None:
    try:
        results = run_analysis()
    except Exception as exc:
        print(f"\nAnalysis could not be completed: {exc}")
        print(
            "The most common cause is a temporary Yahoo Finance download issue "
            "or lack of internet access."
        )
        raise SystemExit(1) from exc

    print_console_summary(results)


if __name__ == "__main__":
    main()
