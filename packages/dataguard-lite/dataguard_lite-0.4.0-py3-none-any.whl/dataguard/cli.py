import argparse
from .core import validate_csv


def main():
    parser = argparse.ArgumentParser(description="DataGuard dataset validator")
    parser.add_argument("csv", help="Path to CSV file")
    parser.add_argument("--target", help="Target column name", default=None)
    parser.add_argument("--json", help="Save report as JSON file", default=None)
    parser.add_argument("--signal", action="store_true", help="Detect silent signal loss")
    parser.add_argument("--roles", action="store_true", help="Infer column roles")

    args = parser.parse_args()

    report = validate_csv(
        args.csv,
        target=args.target,
        signal=args.signal,
        roles=args.roles
    )

    report.summary()

    if args.json:
        report.to_json(args.json)
        print(f"Report saved to {args.json}")
