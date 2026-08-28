from pathlib import Path
import cv2
import json


def generate_parcels(input_path: str, output_path: str) -> None:
    """Convert detected boundaries into parcel polygons."""

    image = cv2.imread(str(input_path), cv2.IMREAD_GRAYSCALE)

    if image is None:
        raise FileNotFoundError(f"Could not read: {input_path}")

    # Close small gaps in boundaries
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    closed = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)

    # Find closed contours
    contours, _ = cv2.findContours(
        closed,
        cv2.RETR_LIST,
        cv2.CHAIN_APPROX_SIMPLE
    )

    parcels = []

    for index, contour in enumerate(contours):
        area = cv2.contourArea(contour)

        # Ignore tiny noise regions
        if area < 500:
            continue

        epsilon = 0.01 * cv2.arcLength(contour, True)
        polygon = cv2.approxPolyDP(contour, epsilon, True)

        coordinates = [
            [int(point[0][0]), int(point[0][1])]
            for point in polygon
        ]

        # Close polygon
        if coordinates and coordinates[0] != coordinates[-1]:
            coordinates.append(coordinates[0])

        parcels.append({
            "parcel_id": f"TEST-{index + 1:04d}",
            "area_pixels": area,
            "geometry": {
                "type": "Polygon",
                "coordinates": [coordinates]
            }
        })

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(parcels, file, indent=2)

    print(f"Generated {len(parcels)} parcel polygons.")
    print(f"Saved to: {output_path}")


if __name__ == "__main__":
    generate_parcels(
        "data/processed/test_map_boundaries_filtered.png",
        "data/processed/test_parcels.json"
    )