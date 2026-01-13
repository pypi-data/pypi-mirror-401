import pandas as pd


def infer_column_roles(df: pd.DataFrame) -> dict:
    roles = {}
    row_count = len(df)

    for col in df.columns:
        series = df[col].dropna()

        if series.empty:
            roles[col] = "empty"
            continue

        unique_count = series.nunique()
        unique_ratio = unique_count / row_count

        # Guard for very small datasets
        if row_count < 20 and pd.api.types.is_numeric_dtype(series):
            roles[col] = "numeric-continuous"
            continue

        # Identifier-like columns (NON-numeric only)
        if unique_ratio > 0.95 and not pd.api.types.is_numeric_dtype(series):
            roles[col] = "identifier"
            continue

        # Numeric columns
        if pd.api.types.is_numeric_dtype(series):
            if unique_count <= 10:
                roles[col] = "numeric-discrete"
            else:
                roles[col] = "numeric-continuous"
            continue

        # Categorical / text columns
        avg_len = series.astype(str).str.len().mean()

        if unique_count == 2:
            roles[col] = "categorical-binary"
        elif avg_len > 20:
            roles[col] = "text"
        else:
            roles[col] = "categorical"

    return roles
