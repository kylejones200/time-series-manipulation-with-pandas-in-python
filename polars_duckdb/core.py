"""Time series manipulation using Polars and DuckDB."""

import duckdb
import polars as pl
import matplotlib.pyplot as plt
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(message)s')

# Mapping from pandas resample freq codes to Polars group_by_dynamic every-strings.
_FREQ_MAP = {"D": "1d", "W": "1w", "M": "1mo", "Q": "1q", "Y": "1y", "H": "1h", "T": "1m"}


def manipulate_time_series(df: pl.DataFrame, date_col: str, value_col: str) -> pl.DataFrame:
    # DuckDB window functions replace pandas .rolling(), .shift(), .pct_change().
    # ROWS BETWEEN 6 PRECEDING AND CURRENT ROW = 7-row trailing window (matches rolling(7)).
    result = duckdb.sql(f"""
        SELECT
            {date_col},
            {value_col},
            AVG({value_col})         OVER w AS rolling_mean,
            STDDEV_SAMP({value_col}) OVER w AS rolling_std,
            LAG({value_col}, 1) OVER (ORDER BY {date_col}) AS shifted,
            ({value_col} - LAG({value_col}, 1) OVER (ORDER BY {date_col}))
                / NULLIF(LAG({value_col}, 1) OVER (ORDER BY {date_col}), 0) AS pct_change
        FROM df
        WINDOW w AS (ORDER BY {date_col} ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)
        ORDER BY {date_col}
    """).pl()
    return result


def resample_time_series(
    df: pl.DataFrame,
    date_col: str,
    value_col: str,
    freq: str = "W",
) -> pl.DataFrame:
    every = _FREQ_MAP.get(freq.upper(), freq)
    return (
        df.sort(date_col)
          .group_by_dynamic(date_col, every=every)
          .agg(pl.col(value_col).mean())
    )


def plot_time_series_manipulation(
    df: pl.DataFrame,
    date_col: str,
    value_col: str,
    title: str,
    output_path: Path,
):
    if plot:
        fig, axes = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

        dates = df[date_col].to_list()

        axes[0].plot(dates, df[value_col].to_list(), label="Original", color="#4A90A4", linewidth=1.2)
        axes[0].plot(dates, df["rolling_mean"].to_list(), label="Rolling Mean (7d)", color="#D4A574", linewidth=1.2)
        axes[0].set_ylabel("Value")
        axes[0].set_title(title)
        axes[0].legend(loc="best")

        axes[1].plot(dates, df["pct_change"].to_list(), label="Percent Change", color="#8B6F9E", linewidth=1.2)
        axes[1].set_xlabel("Date")
        axes[1].set_ylabel("Percent Change")
        axes[1].legend(loc="best")

        plt.tight_layout()
        plt.savefig(output_path, dpi=100, bbox_inches="tight", facecolor="white")
        plt.close()
