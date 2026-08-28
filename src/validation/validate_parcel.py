import json
from pathlib import Path


def validate_parcels(input_path: str, output_path: str) -> None:
    input_file = Path(input_path)
    output_file = Path(output_path)

    if not input_file.exists():
        raise FileNotFoundError(f"Parcel file not found: {input_file}")

    with open(input_file, "r", encoding="utf-8") as file:
        parcels = json.load(file)

    valid_parcels = []

    for parcel in parcels:
        coordinates = parcel["geometry"]["coordinates"][0]

        # A polygon needs at least 4 points,
        # including the repeated starting point.
        if len(coordinates) < 4:
            continue

        # Check that the polygon is closed.
        if coordinates[0] != coordinates[-1]:
            coordinates.append(coordinates[0])

        parcel["geometry"]["coordinates"] = [coordinates]
        valid_parcels.append(parcel)

    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(valid_parcels, file, indent=2)

    print(f"Valid parcels: {len(valid_parcels)}")
    print(f"Removed invalid parcels: {len(parcels) - len(valid_parcels)}")
    print(f"Saved to: {output_file}")


if __name__ == "__main__":
    validate_parcels(
        "data/processed/test_parcels_georeferenced.json",
        "data/processed/test_parcels_validated.json"
    )