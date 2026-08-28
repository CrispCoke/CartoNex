import json
from pathlib import Path


def validate_parcels(input_path: str, output_path: str) -> None:
    input_file = Path(input_path)
    output_file = Path(output_path)

    with open(input_file, "r", encoding="utf-8") as file:
        parcels = json.load(file)

    for parcel in parcels:
        area = parcel.get("area_pixels", 0)
        plot_number = parcel.get("plot_number")

        if area <= 0:
            parcel["validation_status"] = "INVALID"

        elif plot_number is None:
            parcel["validation_status"] = "WARNING"

        else:
            parcel["validation_status"] = "VALID"

    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(parcels, file, indent=2)

    valid = sum(
        1 for p in parcels
        if p["validation_status"] == "VALID"
    )

    warning = sum(
        1 for p in parcels
        if p["validation_status"] == "WARNING"
    )

    invalid = sum(
        1 for p in parcels
        if p["validation_status"] == "INVALID"
    )

    print(f"VALID parcels: {valid}")
    print(f"WARNING parcels: {warning}")
    print(f"INVALID parcels: {invalid}")
    print(f"Saved to: {output_file}")


if __name__ == "__main__":
    validate_parcels(
        "data/processed/parcels_with_plot_numbers.json",
        "data/processed/test_parcels_validated.json"
    )