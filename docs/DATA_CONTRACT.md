# Group 1 Data Contract

## Purpose

Group 1 converts legacy land-survey material into georeferenced digital land parcels and building footprints for downstream processing.

## Group 1 Inputs

- Scanned Mouza/Tippan maps
- Existing survey coordinates
- Drone or satellite imagery
- Municipal building information
- Available parcel or plot records

## Group 1 Processing

1. Map preprocessing
2. Boundary-line detection
3. Plot-number OCR
4. Parcel polygon extraction
5. Georeferencing
6. Rubber-sheet transformation when required
7. Parcel topology validation
8. Building-footprint extraction
9. Building-height estimation when available
10. Confidence and provenance recording

## Group 1 Outputs

Each processed parcel should provide:

- Plot/parcel identifier
- Valid 2D parcel polygon
- Coordinate reference system (CRS)
- Building footprint when present
- Estimated building height when available
- Accuracy/confidence information
- Source/provenance information
- Georeferencing/transformation information

## Parcel Geometry

Parcel boundaries are represented as valid 2D polygons.

A parcel must:

- Have a closed boundary
- Use a declared CRS
- Avoid self-intersections
- Avoid unintended gaps or overlaps
- Preserve the original plot identifier where available

## Building Footprint

The building footprint represents the 2D portion of a building associated with the parcel.

It may contain:

- Footprint geometry
- Detection source
- Detection confidence
- Estimated height

Group 1 does **not** create apartments, floors, or internal 3D spaces. Those are handled by Group 2.

## Coordinate Information

Spatial outputs should record:

- CRS
- Coordinate units
- Coordinate epoch when applicable
- Georeferencing method
- Transformation information when used
- Positional tolerance when available

## Accuracy and Confidence

Estimated geometry must not be presented as surveyed geometry.

The output should record:

- Boundary confidence
- OCR confidence
- Georeferencing confidence
- Building-detection confidence
- Estimated positional error when available

## Provenance

Each result should retain its source information.

Recommended fields:

- Source document
- Source map identifier
- Source image
- Processing method
- Processing timestamp
- Pipeline version
- Transformation method

## Group 1 → Group 2 Handoff

Group 2 is responsible for reading IFC building models and extracting the internal cadastral hierarchy:

**Parcel → Building → Storey → Space**

Group 1 therefore provides the parent land context and building footprint rather than generating internal building spaces.

The current StrataForge Group 2 API accepts an IFC file and supports:

- `parent_ulpin`
- `valid_from_unix_s`
- `valid_to_unix_s`
- `coordinate_epoch_milliyear`
- `tolerance_m`
- `explicit_transform_json`

Therefore, Group 1 must preserve the parcel identity and spatial-reference information needed to associate a building with its parent parcel.

## Downstream Compatibility

Group 1 output should be capable of supplying:

- Parent parcel identifier
- Parcel geometry
- CRS
- Coordinate epoch when available
- Georeferencing transformation
- Positional tolerance
- Valid-from timestamp
- Valid-to timestamp when applicable

## Validation Requirements

Before downstream handoff:

- Geometry must be valid
- Polygon must be closed
- CRS must be present
- Parcel identifier must be present
- Coordinates must be finite
- Self-intersections must be checked
- Confidence information should be present
- Provenance information should be present

## Versioning

A new processing result must not silently overwrite an earlier result.

Each output should include:

- Schema version
- Pipeline version
- Processing timestamp
- Source reference

## Responsibility Boundary

### Group 1

Responsible for:

- Legacy map processing
- Parcel extraction
- Georeferencing
- Parcel validation
- Building-footprint extraction
- Approximate building-height estimation
- Spatial provenance

### Group 2

Responsible for:

- IFC processing
- Building hierarchy
- Storey extraction
- Apartment/unit extraction
- Common-area extraction
- Closed 3D space generation

### Group 3

Responsible for:

- 3D-ULPIN generation
- Spatial indexing
- 3D collision detection
- Geometry registration
- Spatial versioning