import json
from pathlib import Path

import cv2


def create_overlay(
    image_path: str,
    parcels_path: str,
    numbers_path: str,
    output_path: str
) -> None:

    image = cv2.imread(image_path)

    if image is None:
        raise FileNotFoundError(f"Could not read image: {image_path}")

    with open(parcels_path, "r", encoding="utf-8") as file:
        parcels = json.load(file)

    with open(numbers_path, "r", encoding="utf-8") as file:
        numbers = json.load(file)

    # Draw parcel boundaries
    for parcel in parcels:
        coordinates = parcel["geometry"]["coordinates"][0]

        points = [
            [int(x), int(y)]
            for x, y in coordinates
        ]

        points = __import__("numpy").array(
            points,
            dtype="int32"
        )

        cv2.polylines(
            image,
            [points],
            True,
            (255, 0, 0),
            2
        )

    # Draw OCR number locations
    for number in numbers:
        location = number["location"]

        x = location["x"]
        y = location["y"]
        w = location["width"]
        h = location["height"]

        cv2.rectangle(
            image,
            (x, y),
            (x + w, y + h),
            (0, 0, 255),
            2
        )

        cv2.putText(
            image,
            number["plot_number"],
            (x, y - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 0, 255),
            2
        )

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    cv2.imwrite(str(output_file), image)

    print(f"Overlay saved to: {output_file}")


if __name__ == "__main__":
    create_overlay(
        "data/raw/test_map.png",
        "data/processed/test_parcels.json",
        "data/processed/plot_numbers_filtered.json",
        "data/processed/parcel_overlay.png"
    )