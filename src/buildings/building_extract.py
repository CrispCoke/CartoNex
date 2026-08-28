from pathlib import Path
import cv2
import json


def extract_buildings(input_path: str, output_path: str) -> None:
    """
    Detect building footprints from a map image.

    This prototype uses contours to identify compact rectangular
    structures such as buildings shown on the scanned map.
    """

    input_file = Path(input_path)
    output_file = Path(output_path)

    if not input_file.exists():
        raise FileNotFoundError(f"Input map not found: {input_file}")

    image = cv2.imread(str(input_file), cv2.IMREAD_GRAYSCALE)

    if image is None:
        raise ValueError(f"Could not read image: {input_file}")

    # Threshold darker structures
    _, binary = cv2.threshold(
        image,
        120,
        255,
        cv2.THRESH_BINARY_INV
    )

    # Find connected contours
    contours, _ = cv2.findContours(
        binary,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    buildings = []

    for index, contour in enumerate(contours):
        area = cv2.contourArea(contour)

        # Ignore very small marks and large map regions
        if area < 100 or area > 10000:
            continue

        x, y, width, height = cv2.boundingRect(contour)

        # Buildings are generally compact shapes
        if width < 10 or height < 10:
            continue

        buildings.append({
            "building_id": f"B-{index + 1:04d}",
            "bbox": {
                "x": x,
                "y": y,
                "width": width,
                "height": height
            },
            "area_pixels": area
        })

    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(buildings, file, indent=2)

    print(f"Detected {len(buildings)} building candidates.")
    print(f"Saved to: {output_file}")


if __name__ == "__main__":
    extract_buildings(
        "data/raw/test_map.png",
        "data/processed/buildings.json"
    )