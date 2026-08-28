from pathlib import Path
import cv2


def preprocess_map(input_path: str, output_path: str) -> None:
    """
    Preprocess a scanned land map for later boundary/OCR processing.

    Steps:
    1. Read the input map.
    2. Convert it to grayscale.
    3. Reduce small scanning noise.
    4. Improve local contrast.
    5. Save the processed map.
    """

    input_file = Path(input_path)
    output_file = Path(output_path)

    if not input_file.exists():
        raise FileNotFoundError(f"Input map not found: {input_file}")

    image = cv2.imread(str(input_file))

    if image is None:
        raise ValueError(f"Could not read image: {input_file}")

    # Convert scanned map to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Reduce small scanning noise while preserving boundaries
    denoised = cv2.GaussianBlur(gray, (5, 5), 0)

    # Improve contrast for old/stained maps
    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )

    enhanced = clahe.apply(denoised)

    # Create output directory if it does not exist
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Save processed map
    success = cv2.imwrite(str(output_file), enhanced)

    if not success:
        raise IOError(f"Could not save processed map: {output_file}")

    print(f"Preprocessed map saved to: {output_file}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Preprocess a scanned land map."
    )

    parser.add_argument(
        "input",
        help="Path to the scanned map"
    )

    parser.add_argument(
        "output",
        help="Path for the processed map"
    )

    args = parser.parse_args()

    preprocess_map(args.input, args.output)