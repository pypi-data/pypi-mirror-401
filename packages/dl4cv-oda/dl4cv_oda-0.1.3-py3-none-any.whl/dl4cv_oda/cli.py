import asyncio
from pathlib import Path

import geopandas as gpd
import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from dl4cv_oda import (
    clean_osm_data,
    clip_labels_to_tiles,
    convert_to_yolo_format,
    create_train_val_split,
    create_yolo_config,
    download_tiles,
    train_model,
)

app = typer.Typer(help="Object Detection on Aerial Imagery - Coconut Tree Detection")
console = Console()


@app.command()
def cleanup(
    input_file: Path = typer.Argument(..., help="Input OSM GeoJSON file"),
    output_point: Path = typer.Argument(..., help="Output cleaned point file"),
    output_box: Path = typer.Argument(..., help="Output buffered box file"),
):
    """Clean OSM data and generate bounding boxes"""
    with Progress(
        SpinnerColumn(), TextColumn("[progress.description]{task.description}")
    ) as progress:
        progress.add_task("Cleaning OSM data...", total=None)
        count = clean_osm_data(str(input_file), str(output_point), str(output_box))
    console.print(f"[green]OK[/green] Processed {count} trees")


@app.command()
def tile(
    trees_file: Path = typer.Argument(..., help="Trees GeoJSON file"),
    zoom: int = typer.Option(19, help="Zoom level"),
    tms_url: str = typer.Option(..., help="TMS tile URL template"),
    output_dir: Path = typer.Option("data", help="Output directory"),
    prefix: str = typer.Option("OAM", help="Tile prefix"),
):
    """Download aerial imagery tiles"""
    trees = gpd.read_file(str(trees_file))
    trees.to_crs(epsg=4326, inplace=True)
    bbox = trees.total_bounds.tolist()

    with Progress(
        SpinnerColumn(), TextColumn("[progress.description]{task.description}")
    ) as progress:
        progress.add_task("Downloading tiles...", total=None)
        asyncio.run(download_tiles(bbox, zoom, tms_url, str(output_dir), prefix))
    console.print("[green]OK[/green] Tiles downloaded")


@app.command()
def clip(
    trees_file: Path = typer.Argument(..., help="Trees GeoJSON file"),
    tiles_file: Path = typer.Argument(..., help="Tiles GeoJSON file"),
    output_dir: Path = typer.Argument(..., help="Output labels directory"),
    prefix: str = typer.Option("OAM", help="Tile prefix"),
):
    """Clip tree labels to tiles"""
    with Progress(
        SpinnerColumn(), TextColumn("[progress.description]{task.description}")
    ) as progress:
        progress.add_task("Clipping labels...", total=None)
        stats = clip_labels_to_tiles(str(trees_file), str(tiles_file), str(output_dir), prefix)
    console.print(
        f"[green]OK[/green] Processed {stats['processed']} tiles, {stats['total_trees']} trees"
    )


@app.command()
def convert(
    trees_file: Path = typer.Argument(..., help="Trees GeoJSON file"),
    chips_dir: Path = typer.Argument(..., help="Chips directory"),
    labels_dir: Path = typer.Argument(..., help="Labels directory"),
    output_dir: Path = typer.Argument(..., help="YOLO output directory"),
    species: str = typer.Option("Coconut", help="Target species"),
    train_ratio: float = typer.Option(0.8, help="Train split ratio"),
):
    """Convert to YOLO format and create train/val split"""
    with Progress(
        SpinnerColumn(), TextColumn("[progress.description]{task.description}")
    ) as progress:
        task = progress.add_task("Converting to YOLO format...", total=None)
        class_mapping = convert_to_yolo_format(
            str(trees_file), str(chips_dir), str(labels_dir), str(output_dir), species
        )

        progress.update(task, description="Creating train/val split...")
        train_count, val_count = create_train_val_split(
            str(labels_dir), str(chips_dir), str(output_dir), train_ratio
        )

        progress.update(task, description="Creating YOLO config...")
        create_yolo_config(str(output_dir), class_mapping)

    console.print(f"[green]OK[/green] Train: {train_count} | Val: {val_count}")


@app.command()
def train(
    config_path: Path = typer.Argument(..., help="YOLO config YAML file"),
    epochs: int = typer.Option(100, help="Number of training epochs"),
    imgsz: int = typer.Option(256, help="Image size"),
    batch: int = typer.Option(16, help="Batch size"),
    name: str = typer.Option("coconut_tree_detection", help="Experiment name"),
    model: str = typer.Option("yolov8n.pt", help="Model weights"),
):
    """Train YOLOv8 model"""
    console.print(f"[yellow]Training model with {epochs} epochs...[/yellow]")
    train_model(str(config_path), epochs, imgsz, batch, name, model)
    console.print("[green]OK[/green] Training complete")


@app.command()
def pipeline(
    osm_file: Path = typer.Argument(..., help="Input OSM GeoJSON file"),
    data_dir: Path = typer.Option(Path("data"), help="Data directory"),
    tms_url: str = typer.Option(..., help="TMS tile URL template"),
    zoom: int = typer.Option(19, help="Zoom level"),
    epochs: int = typer.Option(100, help="Training epochs"),
    batch: int = typer.Option(16, help="Batch size"),
):
    """Run complete pipeline from raw data to trained model"""
    console.print("[bold blue]Starting full pipeline...[/bold blue]\n")

    data_dir.mkdir(exist_ok=True)
    raw_dir = data_dir / "raw"
    raw_dir.mkdir(exist_ok=True)

    cleaned_file = raw_dir / "cleaned.geojson"
    trees_box_file = data_dir / "trees_box.geojson"
    tiles_file = data_dir / "tiles.geojson"
    labels_dir = data_dir / "labels"
    chips_dir = data_dir / "chips"
    yolo_dir = data_dir / "yolo"

    console.print("[1/5] Cleaning OSM data...")
    count = clean_osm_data(str(osm_file), str(cleaned_file), str(trees_box_file))
    console.print(f"  [OK] Processed {count} trees\n")

    console.print("[2/5] Downloading tiles...")
    trees = gpd.read_file(str(trees_box_file))
    trees.to_crs(epsg=4326, inplace=True)
    bbox = trees.total_bounds.tolist()
    asyncio.run(download_tiles(bbox, zoom, tms_url, str(data_dir), "OAM"))
    console.print("  [OK] Tiles downloaded\n")

    console.print("[3/5] Clipping labels to tiles...")
    stats = clip_labels_to_tiles(str(trees_box_file), str(tiles_file), str(labels_dir), "OAM")
    console.print(f"  [OK] Processed {stats['processed']} tiles, {stats['total_trees']} trees\n")

    console.print("[4/5] Converting to YOLO format...")
    class_mapping = convert_to_yolo_format(
        str(trees_box_file), str(chips_dir), str(labels_dir), str(yolo_dir), "Coconut"
    )
    train_count, val_count = create_train_val_split(str(labels_dir), str(chips_dir), str(yolo_dir))
    config_file = create_yolo_config(str(yolo_dir), class_mapping)
    console.print(f"  [OK] Train: {train_count} | Val: {val_count}\n")

    console.print("[5/5] Training model...")
    train_model(str(config_file), epochs, 256, batch, "coconut_tree_detection", "yolov8n.pt")
    console.print("  [OK] Training complete\n")

    console.print("[bold green]Pipeline completed successfully![/bold green]")


if __name__ == "__main__":
    app()