"""
Generate synthetic return-data CSV for the Fulfillment-Returns Analysis repo.
Run:  python data/generator/generate_returns.py --n 10000
"""
import argparse
import numpy as np
import pandas as pd
from pathlib import Path

def make_dataset(n_rows: int, out_path: str):
    np.random.seed(42)

    skus    = [f"SKU{i:04d}" for i in range(1, 501)]
    fcs     = ["SEA8", "PHL2", "ONT6"]
    reasons = ["Defective", "Wrong Size", "Changed Mind", "Other"]

    df = pd.DataFrame({
        "order_id": np.arange(n_rows),
        "fc":       np.random.choice(fcs, n_rows, p=[0.4, 0.35, 0.25]),
        "sku":      np.random.choice(skus, n_rows),
        "price":    np.round(np.random.gamma(4, 20, n_rows), 2)
    })

    p_ret = np.clip(0.03 + 0.0005*df["price"]
                    + np.random.normal(0, 0.01, n_rows), 0, 0.4)
    df["is_return"] = np.random.binomial(1, p_ret)
    df["return_reason"] = np.where(
        df["is_return"] == 1,
        np.random.choice(reasons, n_rows),
        ""
    )
    df["concession_cost"] = df["is_return"] * np.round(
        df["price"] * np.random.uniform(0.3, 0.9, n_rows), 2
    )

    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    print(f"✓ Saved {out_path}  ({n_rows:,} rows)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=10000,
                        help="number of synthetic orders")
    parser.add_argument("--out", type=str,
                        default="data/raw/returns_sample.csv",
                        help="output CSV path")
    args = parser.parse_args()
    make_dataset(args.n, args.out)

