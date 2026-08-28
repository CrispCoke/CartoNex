# CartoNex

CartoNex is the Group 1 engine of the 3D/4D cadastral platform. It converts legacy scanned land-survey maps into structured digital parcel data using image processing, boundary detection, OCR, parcel matching, validation, georeferencing, and GeoJSON export.

> **Prototype status:** The current pipeline is functional on the provided test map. OCR accuracy, parcel matching, and survey-grade georeferencing require further refinement for production deployment.

## Pipeline

```text
Scanned Land Map
       ↓
Image Preprocessing
       ↓
Boundary Detection & Filtering
       ↓
Parcel Polygon Generation
       ↓
Plot Number OCR
       ↓
Plot ↔ Parcel Matching
       ↓
Parcel Validation
       ↓
Georeferencing
````
# Key Features
Scanned cadastral / Tippan map processing
Automatic parcel boundary detection
Parcel polygon generation
OCR-based plot-number extraction using Tesseract
Plot-number to parcel matching
Parcel geometry validation
Pixel-to-map coordinate transformation
GeoJSON export
Visualization and intermediate processing outputs
       ↓
GeoJSON Export

# Current Prototype Results
| Metric                  | Result |
| ----------------------- | -----: |
| Total parcels generated |    112 |
| Plot numbers matched    |     33 |
| Unmatched parcels       |     79 |
| Invalid parcels         |      0 |
Unmatched parcels are retained as WARNING rather than discarded, allowing them to be reviewed or processed further.

# Project Structure
CartoNex/
├── data/
│   ├── raw/
│   ├── processed/
│   ├── output/
│   └── control_points.json
│
├── src/
│   ├── vectorization/
│   ├── validation/
│   ├── georeferencing/
│   ├── buildings/
│   ├── visualization/
│   └── output/
│
├── requirements.txt
└── README.md

# Installation
# Requirements
Python 3.10+
Tesseract OCR
Git

Install dependencies:

pip install -r requirements.txt

Verify Tesseract:

tesseract --version
Running the Pipeline

Generate parcels:

python src/vectorization/generate_parcels.py

Extract plot numbers:

python src/vectorization/ocr_plot_numbers.py

Filter OCR results:

python src/vectorization/filter_plot_numbers.py

Match plot numbers with parcels:

python src/vectorization/match_plot_parcels.py

Validate parcels:

python src/validation/validate_parcel.py

Georeference parcels:

python src/georeferencing/georeference.py

Export GeoJSON:

python src/output/export_parcel.py

Final output:

data/output/parcels.geojson
Integration

CartoNex provides the digital parcel layer for the downstream cadastral pipeline:

CartoNex
Group 1
   │
   │ Digital Parcels
   ▼
StrataForge
Group 2
   │
   │ 3D Cadastral Spaces
   ▼
BhuSOT-4D
Group 3

# Validation
CartoNex currently uses three validation states:
| Status    | Meaning                          |
| --------- | -------------------------------- |
| `VALID`   | Geometry passed validation       |
| `WARNING` | Requires additional verification |
| `INVALID` | Geometry failed validation       |

Current test result:
VALID    : 33
WARNING  : 79
INVALID  : 0

# Limitations
OCR accuracy can vary with map quality.
Some plot numbers may remain unmatched.
Complex or noisy boundaries may require refinement.
Current georeferencing is a prototype transformation.
Production deployment requires authoritative survey control points and cadastral data.
