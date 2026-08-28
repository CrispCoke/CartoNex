import re
import json
from pathlib import Path

import cv2
import pytesseract


pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def extract_plot_numbers(image_path: str, output_path: str) -> None:
    """Detect likely numeric plot numbers and their image locations."""

    input_file = Path(image_path)
    output_file = Path(output_path)

    image = cv2.imread(str(input_file), cv2.IMREAD_GRAYSCALE)

    if image is None:
        raise FileNotFoundError(f"Could not read: {input_file}")

    # Improve text visibility
    blurred = cv2.GaussianBlur(image, (3, 3), 0)

    threshold = cv2.threshold(
        blurred,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]

    # Ask Tesseract for individual text boxes
    data = pytesseract.image_to_data(
        threshold,
        config="--psm 11",
        output_type=pytesseract.Output.DICT
    )

    detected_numbers = []

    for i, text in enumerate(data["text"]):
        text = text.strip()

        # Keep only 1-4 digit values
        if not re.fullmatch(r"\d{1,4}", text):
            continue

        confidence = float(data["conf"][i])

        # Ignore very uncertain OCR results
        if confidence < 50:
            continue

        x = data["left"][i]
        y = data["top"][i]
        width = data["width"][i]
        height = data["height"][i]

        detected_numbers.append({
            "plot_number": text,
            "confidence": round(confidence, 2),
            "location": {
                "x": x,
                "y": y,
                "width": width,
                "height": height
            }
        })

    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(detected_numbers, file, indent=2)

    print(f"Detected {len(detected_numbers)} numeric labels.")

    for number in detected_numbers:
        print(
            f"Plot {number['plot_number']} "
            f"(confidence: {number['confidence']}%) "
            f"at {number['location']}"
        )

    print(f"Saved to: {output_file}")


if __name__ == "__main__":
    extract_plot_numbers(
        "data/raw/test_map.png",
        "data/processed/plot_numbers.json"
    )