import json
import math
from pathlib import Path


MAX_DISTANCE = 150


def polygon_center(coordinates):
    xs = [point[0] for point in coordinates]
    ys = [point[1] for point in coordinates]

    return sum(xs) / len(xs), sum(ys) / len(ys)


def distance(point1, point2):
    return math.sqrt(
        (point1[0] - point2[0]) ** 2 +
        (point1[1] - point2[1]) ** 2
    )


def match_plot_parcels(
    parcels_path: str,
    numbers_path: str,
    output_path: str
) -> None:

    with open(parcels_path, "r", encoding="utf-8") as file:
        parcels = json.load(file)

    with open(numbers_path, "r", encoding="utf-8") as file:
        numbers = json.load(file)

    for parcel in parcels:
        coordinates = parcel["geometry"]["coordinates"][0]

        parcel["center"] = polygon_center(coordinates)
        parcel["plot_number"] = None

    assigned_parcels = set()

    for number in numbers:
        location = number["location"]

        text_center = (
            location["x"] + location["width"] / 2,
            location["y"] + location["height"] / 2
        )

        nearest_parcel = None
        nearest_distance = float("inf")

        for index, parcel in enumerate(parcels):

            if index in assigned_parcels:
                continue

            current_distance = distance(
                text_center,
                parcel["center"]
            )

            if current_distance < nearest_distance:
                nearest_distance = current_distance
                nearest_parcel = parcel
                nearest_index = index

        if (
            nearest_parcel is not None
            and nearest_distance <= MAX_DISTANCE
        ):
            nearest_parcel["plot_number"] = number["plot_number"]
            nearest_parcel["ocr_confidence"] = number["confidence"]
            nearest_parcel["ocr_distance"] = round(
                nearest_distance,
                2
            )

            assigned_parcels.add(nearest_index)

    for parcel in parcels:
        parcel.pop("center", None)

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(parcels, file, indent=2)

    matched = sum(
        1
        for parcel in parcels
        if parcel.get("plot_number") is not None
    )

    print(f"Parcels matched with plot numbers: {matched}")
    print(f"Total parcels: {len(parcels)}")
    print(f"Unmatched parcels: {len(parcels) - matched}")
    print(f"Saved to: {output_file}")


if __name__ == "__main__":
    match_plot_parcels(
        "data/processed/test_parcels_validated.json",
        "data/processed/plot_numbers_filtered.json",
        "data/processed/parcels_with_plot_numbers.json"
    )