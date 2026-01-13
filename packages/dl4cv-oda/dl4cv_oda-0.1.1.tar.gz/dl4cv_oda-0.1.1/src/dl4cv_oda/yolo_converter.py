import shutil
from pathlib import Path

import geopandas as gpd
import pandas as pd
import rasterio
import yaml
from PIL import Image


def geojson_to_yolo(geojson_path, image_path, class_mapping):
    trees = gpd.read_file(geojson_path)
    yolo_lines = []

    with rasterio.open(image_path) as src:
        for _, tree in trees.iterrows():
            species = tree.get("species_mapped", "Unknown")
            class_id = class_mapping.get(species, 0)

            minx, miny, maxx, maxy = tree.geometry.bounds
            top_py, top_px = src.index(minx, miny)
            bottom_py, bottom_px = src.index(maxx, maxy)

            center_x = (top_px + bottom_px) / 2 / src.width
            center_y = (top_py + bottom_py) / 2 / src.height
            width = abs(top_px - bottom_px) / src.width
            height = abs(top_py - bottom_py) / src.height

            yolo_lines.append(
                f"{class_id} {center_x:.6f} {center_y:.6f} {width:.6f} {height:.6f}"
            )

    return yolo_lines


def convert_to_yolo_format(
    trees_path, chips_dir, labels_dir, output_dir, target_species="Coconut"
):
    trees = gpd.read_file(trees_path)
    trees = trees[trees["species_mapped"] == target_species]

    chips_dir = Path(chips_dir)
    labels_dir = Path(labels_dir)
    output_dir = Path(output_dir)

    output_dir.mkdir(exist_ok=True)
    yolo_labels_dir = output_dir / "labels"
    yolo_labels_dir.mkdir(exist_ok=True)

    classes = sorted(trees["species_mapped"].unique())
    class_to_id = {cls: idx for idx, cls in enumerate(classes)}

    label_files = sorted(labels_dir.glob("*.geojson"))

    for label_file in label_files:
        stem = label_file.stem
        image_file = chips_dir / f"{stem}.tif"

        if not image_file.exists():
            continue

        yolo_lines = geojson_to_yolo(label_file, image_file, class_to_id)
        yolo_file = yolo_labels_dir / f"{stem}.txt"

        with open(yolo_file, "w") as f:
            f.write("\n".join(yolo_lines))

    return class_to_id


def create_train_val_split(
    labels_dir, chips_dir, yolo_dir, train_ratio=0.7, val_ratio=0.2, test_ratio=0.1
):
    labels_dir = Path(labels_dir)
    chips_dir = Path(chips_dir)
    yolo_dir = Path(yolo_dir)
    yolo_labels_dir = yolo_dir / "labels"

    train_dir = yolo_dir / "train"
    val_dir = yolo_dir / "val"
    test_dir = yolo_dir / "test"
    train_dir.mkdir(exist_ok=True)
    val_dir.mkdir(exist_ok=True)
    test_dir.mkdir(exist_ok=True)

    data = []
    for label_file in labels_dir.glob("*.geojson"):
        trees = gpd.read_file(label_file)
        if not trees.empty:
            dominant_species = trees["species_mapped"].value_counts().idxmax()
            data.append({"file": label_file.stem, "species": dominant_species})

    df = pd.DataFrame(data)
    train_df = df.groupby("species", group_keys=False).apply(
        lambda x: x.sample(frac=train_ratio, random_state=42)
    )
    remaining_df = df.drop(train_df.index)

    # Split remaining data into val and test based on adjusted ratio
    val_frac = val_ratio / (val_ratio + test_ratio)
    val_df = remaining_df.groupby("species", group_keys=False).apply(
        lambda x: x.sample(frac=val_frac, random_state=42)
    )
    test_df = remaining_df.drop(val_df.index)

    for split_df, target_dir in [
        (train_df, train_dir),
        (val_df, val_dir),
        (test_df, test_dir),
    ]:
        for stem in split_df["file"]:
            with rasterio.open(chips_dir / f"{stem}.tif") as src:
                Image.fromarray(src.read([1, 2, 3]).transpose(1, 2, 0)).save(
                    target_dir / f"{stem}.png"
                )
            shutil.copy(yolo_labels_dir / f"{stem}.txt", target_dir / f"{stem}.txt")

    return len(train_df), len(val_df), len(test_df)


def create_yolo_config(yolo_dir, class_mapping):
    yolo_dir = Path(yolo_dir)

    config = {
        "path": str(yolo_dir.absolute()),
        "train": "train",
        "val": "val",
        "test": "test",
        "names": {idx: name for name, idx in class_mapping.items()},
    }

    config_file = yolo_dir / "config.yaml"
    with open(config_file, "w") as f:
        yaml.dump(config, f, sort_keys=False)

    return config_file
