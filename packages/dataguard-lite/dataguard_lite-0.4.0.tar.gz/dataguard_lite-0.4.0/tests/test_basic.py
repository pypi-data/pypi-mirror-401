from dataguard import validate_csv
import pandas as pd


def test_validate_csv(tmp_path):
    data = {
        "a": [1, 2, None],
        "b": [1, 1, 1]
    }

    csv_path = tmp_path / "test.csv"
    pd.DataFrame(data).to_csv(csv_path, index=False)

    report = validate_csv(csv_path)

    assert report.results["rows"] == 3
    assert report.results["duplicate_rows"] == 0
