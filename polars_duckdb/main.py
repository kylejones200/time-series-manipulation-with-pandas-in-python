#!/usr/bin/env python3
"""Time series manipulation — Polars + DuckDB rewrite of ../main.py"""

import argparse
import logging
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import polars as pl
import yaml
from core import (
    manipulate_time_series,
    plot_time_series_manipulation,
    resample_time_series,
)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def load_config(config_path: Path | None = None) -> dict:
    if config_path is None:
        config_path = Path(__file__).parent.parent / "config.yaml"
    with open(config_path) as f:
        return yaml.safe_load(f)


def main():
    parser = argparse.ArgumentParser(
        description="Time series manipulation — Polars + DuckDB"
    )
    parser.add_argument("--config", type=Path, default=None)
    parser.add_argument("--data-path", type=Path, default=None)
    parser.add_argument("--output-dir", type=Path, default=None)
    args = parser.parse_args()
    config = load_config(args.config)
    date_col = config["data"]["date_column"]
    value_col = config["data"]["value_column"]
    output_dir = (
        Path(args.output_dir)
        if args.output_dir
        else Path(config["output"]["figures_dir"])
    )
    output_dir.mkdir(exist_ok=True)
    if args.data_path and args.data_path.exists():
        df = pl.read_csv(args.data_path, try_parse_dates=True)
    elif config["data"]["generate_synthetic"]:
        rng = np.random.default_rng(config["data"]["seed"])
        n = config["data"]["n_periods"]
        start = date(2023, 1, 1)
        dates = [start + timedelta(days=i) for i in range(n)]
        values = 100 + 10 * np.sin(np.arange(n) / 30) + rng.normal(0, 3, n)
        df = pl.DataFrame({date_col: dates, value_col: values.tolist()})
    else:
        raise ValueError("No data source specified")

    df_result = manipulate_time_series(df, date_col, value_col)
    logging.info(f"Mean: {df_result[value_col].mean():.2f}")
    logging.info(f"Std:  {df_result[value_col].std():.2f}")
    resampled = resample_time_series(
        df_result,
        date_col,
        value_col,
        freq=config["manipulation"]["resample_freq"],
    )
    logging.info(
        f"Resampled length ({config['manipulation']['resample_freq']}): {len(resampled)}"
    )
    plot_time_series_manipulation(
        df_result,
        date_col,
        value_col,
        "Time Series Manipulation",
        output_dir / "manipulation.png",
    )
    logging.info(f"Analysis complete. Figures saved to {output_dir}")


if __name__ == "__main__":
    main()
