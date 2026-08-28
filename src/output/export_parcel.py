import json
from pathlib import Path


def export_geojson(input_path: str, output_path: str) -> None:
    input_file = Path(input_path)
    output_file = Path(output_path)

    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")

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

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(geojson, file, indent=2)

    print(f"Exported {len(features)} parcels.")
    print(f"Saved to: {output_file}")


if __name__ == "__main__":
    export_geojson(
        "data/processed/test_parcels_validated.json",
        "data/output/test_parcels.geojson"
    )