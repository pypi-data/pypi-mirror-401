from pathlib import Path


def train_model(
    config_path,
    epochs=100,
    imgsz=256,
    batch=16,
    name="coconut_tree_detection",
    model_name="yolov8n.pt",
):
    from ultralytics import YOLO

    config_path = Path(config_path)
    model = YOLO(model_name)

    results = model.train(
        data=str(config_path),
        epochs=epochs,
        imgsz=imgsz,
        batch=batch,
        name=name,
    )

    return results