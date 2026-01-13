import pandas as pd
import numpy as np
from math import log2


def _entropy(series: pd.Series) -> float:
    values = series.value_counts(normalize=True)
    return -sum(p * log2(p) for p in values if p > 0)


def detect_signal_loss(df: pd.DataFrame) -> list[dict]:
    findings = []
    row_count = len(df)

    for col in df.columns:
        series = df[col].dropna()

        if series.empty:
            continue

        # Numeric columns
        if pd.api.types.is_numeric_dtype(series):
            std = float(series.std())
            unique_ratio = series.nunique() / row_count

            if std == 0:
                severity = "CRITICAL"
                message = "Signal collapsed. All values are identical."
            elif unique_ratio < 0.01:
                severity = "WARNING"
                message = "Low variability detected. Column has very few unique values."
            else:
                continue

            findings.append({
                "column": col,
                "type": "numeric",
                "severity": severity,
                "details": {
                    "std": std,
                    "unique_ratio": round(unique_ratio, 4)
                },
                "message": message
            })

        # Categorical columns
        else:
            entropy = _entropy(series)
            max_entropy = log2(series.nunique()) if series.nunique() > 1 else 0
            top_ratio = series.value_counts(normalize=True).iloc[0]

            if entropy == 0:
                severity = "CRITICAL"
                message = "Signal collapsed. Single dominant category."
            elif max_entropy > 0 and entropy < 0.3 * max_entropy:
                severity = "WARNING"
                message = "Low information diversity detected."
            else:
                continue

            findings.append({
                "column": col,
                "type": "categorical",
                "severity": severity,
                "details": {
                    "entropy": round(entropy, 4),
                    "top_value_ratio": round(top_ratio, 4)
                },
                "message": message
            })

    return findings
