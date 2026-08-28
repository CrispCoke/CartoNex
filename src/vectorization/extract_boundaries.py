from pathlib import Path
import cv2


def extract_boundaries(input_path: str, output_path: str) -> None:
    """Detect boundary lines from a preprocessed land map."""

    input_file = Path(input_path)
    output_file = Path(output_path)

    if not input_file.exists():
        raise FileNotFoundError(f"Input map not found: {input_file}")

    image = cv2.imread(str(input_file), cv2.IMREAD_GRAYSCALE)

    if image is None:
        raise ValueError(f"Could not read image: {input_file}")

    # Detect edges
    edges = cv2.Canny(image, 50, 150)

    # Connect broken boundary segments
    kernel = cv2.getStructuringElement(
        cv2.MORPH_RECT, (3, 3)
    )

    boundaries = cv2.morphologyEx(
        edges,
        cv2.MORPH_CLOSE,
        kernel,
        iterations=2
    )

    output_file.parent.mkdir(parents=True, exist_ok=True)

    if not cv2.imwrite(str(output_file), boundaries):
        raise IOError(f"Could not save boundaries: {output_file}")

    print(f"Boundary image saved to: {output_file}")


if __name__ == "__main__":
    extract_boundaries(
        "data/processed/test_map_processed.png",
        "data/processed/test_map_boundaries.png"
    )