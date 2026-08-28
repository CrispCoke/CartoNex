import json
from pathlib import Path


def georeference_parcels(
    input_path: str,
    control_points_path: str,
    output_path: str
) -> None:
    """
    Convert image pixel coordinates into longitude/latitude
    using four corner control points.

    This is a prototype affine transformation.
    """

    input_file = Path(input_path)
    control_file = Path(control_points_path)
    output_file = Path(output_path)

    if not input_file.exists():
        raise FileNotFoundError(
            f"Parcel file not found: {input_file}"
        )

    if not control_file.exists():
        raise FileNotFoundError(
            f"Control points not found: {control_file}"
        )

    with open(input_file, "r", encoding="utf-8") as file:
        parcels = json.load(file)

    with open(control_file, "r", encoding="utf-8") as file:
        control_data = json.load(file)

    points = control_data["points"]

    if len(points) < 4:
        raise ValueError(
            "At least 4 control points are required."
        )

    pixel_x = [p["pixel"][0] for p in points]
    pixel_y = [p["pixel"][1] for p in points]

    world_x = [p["world"][0] for p in points]
    world_y = [p["world"][1] for p in points]

    min_px = min(pixel_x)
    max_px = max(pixel_x)
    min_py = min(pixel_y)
    max_py = max(pixel_y)

    min_wx = min(world_x)
    max_wx = max(world_x)
    min_wy = min(world_y)
    max_wy = max(world_y)

    pixel_width = max_px - min_px
    pixel_height = max_py - min_py

    if pixel_width == 0 or pixel_height == 0:
        raise ValueError(
            "Control points must cover a non-zero area."
        )

    for parcel in parcels:

        coordinates = parcel["geometry"]["coordinates"][0]

        converted = []

        for x, y in coordinates:

            longitude = (
                min_wx
                + ((x - min_px) / pixel_width)
                * (max_wx - min_wx)
            )

            latitude = (
                max_wy
                - ((y - min_py) / pixel_height)
                * (max_wy - min_wy)
            )

            converted.append([
                longitude,
                latitude
            ])

        parcel["geometry"]["coordinates"] = [converted]

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(parcels, file, indent=2)

    print(f"Georeferenced {len(parcels)} parcels.")
    print(f"Saved to: {output_file}")


if __name__ == "__main__":
    georeference_parcels(
        "data/processed/test_parcels_validated.json",
        "data/control_points.json",
        "data/processed/test_parcels_georeferenced.json"
    )