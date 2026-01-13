import pandas as pd
from .checks import basic_checks
from .report import ValidationReport
from .signal import detect_signal_loss
from .roles import infer_column_roles


def validate_csv(
    path: str,
    target: str | None = None,
    signal: bool = False,
    roles: bool = False
) -> ValidationReport:
    df = pd.read_csv(path)
    results = basic_checks(df, target=target)

    if roles:
        results["column_roles"] = infer_column_roles(df)

    if signal:
        results["signal_loss"] = detect_signal_loss(df)

    return ValidationReport(results)
