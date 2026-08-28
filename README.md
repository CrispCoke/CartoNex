# CartoNex

CartoNex is Group 1's parcel digitization and mapping pipeline for converting legacy land survey maps into structured digital parcel data.

## What it does

- Processes scanned land maps and map boundaries
- Detects and generates parcel polygons
- Extracts plot numbers using Tesseract OCR
- Filters and matches plot numbers with detected parcels
- Validates parcel geometries
- Georeferences parcel coordinates
- Exports the final parcel data as GeoJSON

## Pipeline

```text
Input Map
   ↓
Boundary Detection
   ↓
Parcel Generation
   ↓
OCR Plot Number Extraction
   ↓
OCR Filtering
   ↓
Plot ↔ Parcel Matching
   ↓
Parcel Validation
   ↓
Georeferencing
   ↓
GeoJSON Export

```

## Key Features

- Scanned cadastral / Tippan map processing
- Automatic parcel boundary detection
- Parcel polygon generation
- OCR-based plot-number extraction using Tesseract
- Plot-number to parcel matching
- Parcel geometry validation
- Pixel-to-map coordinate transformation
- GeoJSON export
- Visualization and intermediate processing outputs

## Current Prototype Results

| Metric | Result |
|---|---:|
| Total parcels generated | 112 |
| Plot numbers matched | 33 |
| Unmatched parcels | 79 |
| Invalid parcels | 0 |

Unmatched parcels are retained as `WARNING` rather than discarded, allowing them to be reviewed or processed further.

## Project Structure

```text
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
```

## Installation

### Requirements

- Python 3.10+
- Tesseract OCR
- Git

Install dependencies:

```bash
pip install -r requirements.txt
```

Verify Tesseract:

```bash
tesseract --version
```

## Running the Pipeline

### Generate parcels

```bash
python src/vectorization/generate_parcels.py
```

### Extract plot numbers

```bash
python src/vectorization/ocr_plot_numbers.py
```

### Filter OCR results

```bash
python src/vectorization/filter_plot_numbers.py
```

### Match plot numbers with parcels

```bash
python src/vectorization/match_plot_parcels.py
```

### Validate parcels

```bash
python src/validation/validate_parcel.py
```

### Georeference parcels

```bash
python src/georeferencing/georeference.py
```

### Export GeoJSON

```bash
python src/output/export_parcel.py
```

Final output:

```text
data/output/parcels.geojson
```

## Integration

CartoNex provides the digital parcel layer for the downstream cadastral pipeline:

```text
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
```

## Validation

CartoNex currently uses three validation states:

| Status | Meaning |
|---|---|
| `VALID` | Geometry passed validation |
| `WARNING` | Requires additional verification |
| `INVALID` | Geometry failed validation |

Current test result:

```text
VALID    : 33
WARNING  : 79
INVALID  : 0
```

## Limitations

- OCR accuracy can vary with map quality.
- Some plot numbers may remain unmatched.
- Complex or noisy boundaries may require refinement.
- Current georeferencing is a prototype transformation.
- Production deployment requires authoritative survey control points and cadastral data.

## Technical Stack

- **Python** - Processing pipeline
- **OpenCV** - Image processing
- **Tesseract OCR** - Plot-number recognition
- **Shapely / GeoJSON** - Geometric processing
- **JSON** - Intermediate data representation
- **Git / GitHub** - Version control

## Project Status

**CartoNex Group 1 Prototype: Functional**

```text
Map Processing          ✓
Boundary Detection      ✓
Parcel Vectorization    ✓
OCR                     ✓
Plot Matching            ✓
Validation               ✓
Georeferencing           ✓
GeoJSON Export           ✓
```

CartoNex provides the Group 1 foundation for transforming legacy cadastral maps into machine-readable digital parcel data.
