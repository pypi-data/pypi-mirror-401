# Object Detection on Aerial Imagery

Coconut tree detection from drone imagery using YOLOv8 with OpenStreetMap labels and OpenAerialMap imagery.

## Overview

- OpenStreetMap point data : bounding boxes with buffer zones
- Tile large aerial imagery (256×256 at 5cm/pixel)
- Convert geographic coordinates to YOLO format
- Train YOLOv8 on coconut trees from Kolovai, Tonga

**Source**: World Bank - Automated Feature Detection of Aerial Imagery from South Pacific

## Data

**Statistics**:
- **Original**: 10,631 trees (Coconut: 10,092 | Mango: 261 | Banana: 181 | Papaya: 97)
- **Target**: Coconut trees only
- **Tiles**: 256×256px at zoom 19, EPSG:4326
- **Train/Val**: 441 / 167 tiles (80/20 stratified split)

## Structure

```
data/
├── raw/                # OAM imagery + OSM points
├── chips/              # 256×256 tiles (.tif)
├── labels/             # Per-tile annotations (.geojson)
└── yolo/
    ├── train/          # Training data (.png + .txt)
    ├── val/            # Validation data
    └── config.yaml     # YOLO config

notebooks/
├── 01_cleanup.ipynb         # OSM filtering + bbox generation
├── 02_tiles.ipynb           # Imagery tiling
├── 03_yolo_format.ipynb     # GeoJSON : YOLO conversion
└── 04_train.ipynb           # YOLOv8 training
```

## Setup

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
git clone https://github.com/kshitijrajsharma/dl4cv-object-detection-on-aerial-imagery
cd dl4cv-object-detection-on-aerial-imagery
uv sync
```

## Workflow

**1. Clean OSM Data** : Filter coconut trees, generate buffered bounding boxes

**2. Tile Imagery** : Create 256×256 tiles, clip labels to tile extents

**3. YOLO Conversion** : Transform coordinates (EPSG:4326 : pixels : normalized [0,1])

```python
row, col = src.index(lon, lat)  # rasterio
x_norm = col / img_width
y_norm = row / img_height
```

**4. Train** : YOLOv8n, 100 epochs, batch 16

```python
from ultralytics import YOLO
model = YOLO('yolov8n.pt')
model.train(data='data/yolo/config.yaml', epochs=100, imgsz=256, batch=16)
```

## References

- [OpenAerialMap](https://openaerialmap.org/)
- [OpenStreetMap](https://www.openstreetmap.org/)
- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)
- [uv Package Manager](https://github.com/astral-sh/uv)
