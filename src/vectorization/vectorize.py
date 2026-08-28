import json
from pathlib import Path


def vectorize_parcels(
    input_path: str,
    output_path: str
) -> None:
    """
    Prepare validated parcel polygons as vector features.
    """

    input_file = Path(input_path)
    output_file = Path(output_path)

    if not input_file.exists():
        raise FileNotFoundError(
            f"Validated parcel file not found: {input_file}"
        )

    with open(input_file, "r", encoding="utf-8") as file:
        parcels = json.load(file)

    features = []

    for parcel in parcels:
        features.append({
            "type": "Feature",
            "properties": {
                "parcel_id": parcel["parcel_id"],
                "area_pixels": parcel["area_pixels"]
            },
            "geometry": parcel["geometry"]
        })

    result = {
        "type": "FeatureCollection",
        "features": features
    }

    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(result, file, indent=2)

    print(f"Vectorized {len(features)} parcels.")
    print(f"Saved to: {output_file}")


if __name__ == "__main__":
    vectorize_parcels(
        "data/processed/test_parcels_validated.json",
        "data/output/parcels_vectorized.geojson"
    )