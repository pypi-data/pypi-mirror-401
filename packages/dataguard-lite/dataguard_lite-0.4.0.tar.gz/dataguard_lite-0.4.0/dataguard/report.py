import json


class ValidationReport:
    def __init__(self, results: dict):
        self.results = results

    def summary(self):
        print("DataGuard Validation Summary")
        print("-" * 35)

        for key, value in self.results.items():
            if key == "column_roles":
                print("\nInferred Column Roles:")
                for col, role in value.items():
                    print(f"  {col}: {role}")

            elif key == "signal_loss":
                print("\nSilent Signal Loss Detection:")
                if not value:
                    print("  No signal loss detected.")
                else:
                    for item in value:
                        print(f"  Column: {item['column']}")
                        print(f"    Type: {item['type']}")
                        print(f"    Severity: {item['severity']}")
                        print(f"    Message: {item['message']}")

            else:
                print(f"{key}: {value}")

    def to_dict(self) -> dict:
        return self.results

    def to_json(self, path: str):
        with open(path, "w") as f:
            json.dump(self.results, f, indent=2)
