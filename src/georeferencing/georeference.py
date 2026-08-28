import json
from pathlib import Path


def georeference_parcels(
    input_path: str,
    output_path: str,
    scale: float = 1.0,
    origin_x: float = 0.0,
    origin_y: float = 0.0
) -> None:
    """
    Convert image pixel coordinates into local map coordinates.

    For the prototype:
    X = pixel_x * scale + origin_x
    Y = pixel_y * scale + origin_y
    """

    input_file = Path(input_path)
    output_file = Path(output_path)

    if not input_file.exists():
        raise FileNotFoundError(
            f"Parcel file not found: {input_file}"
        )

    with open(input_file, "r", encoding="utf-8") as file:
        parcels = json.load(file)

    for parcel in parcels:
        coordinates = parcel["geometry"]["coordinates"][0]

        converted = []

        for x, y in coordinates:
            real_x = x * scale + origin_x
            real_y = y * scale + origin_y
            converted.append([real_x, real_y])

        parcel["geometry"]["coordinates"] = [converted]

    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(parcels, file, indent=2)

    print(f"Georeferenced {len(parcels)} parcels.")
    print(f"Saved to: {output_file}")


if __name__ == "__main__":
    georeference_parcels(
        "data/processed/test_parcels.json",
        "data/processed/test_parcels_georeferenced.json",
        scale=1.0
    )