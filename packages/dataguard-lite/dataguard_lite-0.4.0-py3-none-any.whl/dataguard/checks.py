import pandas as pd


def basic_checks(df: pd.DataFrame, target: str | None = None) -> dict:
    missing_values = df.isnull().sum().to_dict()
    duplicate_rows = int(df.duplicated().sum())

    report = {
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "duplicate_rows": duplicate_rows,
        "missing_values": missing_values,
    }

    if target and target in df.columns:
        class_counts = df[target].value_counts().to_dict()
        report["target_distribution"] = class_counts

    return report
