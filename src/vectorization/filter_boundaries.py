from pathlib import Path
import cv2


def filter_boundaries(input_path: str, output_path: str) -> None:
    """Remove small noise and keep significant map boundaries."""

    input_file = Path(input_path)
    output_file = Path(output_path)

    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")

    image = cv2.imread(str(input_file), cv2.IMREAD_GRAYSCALE)

    if image is None:
        raise ValueError(f"Could not read image: {input_file}")

    # Remove tiny isolated components
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(
        image,
        connectivity=8
    )

    filtered = image.copy()
    filtered[:] = 0

    # Keep components large enough to represent meaningful map lines
    min_area = 150

    for label in range(1, num_labels):
        area = stats[label, cv2.CC_STAT_AREA]

        if area >= min_area:
            filtered[labels == label] = 255

    # Connect small gaps in boundary lines
    kernel = cv2.getStructuringElement(
        cv2.MORPH_RECT,
        (5, 5)
    )

    filtered = cv2.morphologyEx(
        filtered,
        cv2.MORPH_CLOSE,
        kernel,
        iterations=1
    )

    output_file.parent.mkdir(parents=True, exist_ok=True)

    if not cv2.imwrite(str(output_file), filtered):
        raise IOError(f"Could not save filtered boundaries: {output_file}")

    print(f"Filtered boundaries saved to: {output_file}")


if __name__ == "__main__":
    filter_boundaries(
        "data/processed/test_map_boundaries.png",
        "data/processed/test_map_boundaries_filtered.png"
    )