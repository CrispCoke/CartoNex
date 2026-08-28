import json
from pathlib import Path


def filter_plot_numbers(input_path: str, output_path: str) -> None:
    input_file = Path(input_path)
    output_file = Path(output_path)

    with open(input_file, "r", encoding="utf-8") as file:
        numbers = json.load(file)

    filtered = []

    for item in numbers:
        number = item["plot_number"]
        confidence = item["confidence"]

        # Ignore obvious map metadata
        if number in {"1987", "4000"}:
            continue

        # Keep likely plot numbers
        if not 100 <= int(number) <= 999:
            continue

        # Require reasonable OCR confidence
        if confidence < 70:
            continue

        filtered.append(item)

    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(filtered, file, indent=2)

    print(f"Filtered plot numbers: {len(filtered)}")
    print(f"Saved to: {output_file}")


if __name__ == "__main__":
    filter_plot_numbers(
        "data/processed/plot_numbers.json",
        "data/processed/plot_numbers_filtered.json"
    )