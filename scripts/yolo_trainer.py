import os
from ultralytics import YOLO

def train_yolo():
    yaml_path = os.path.abspath("data/dataset.yaml")
    project_root = os.path.abspath(".")
    processed_data_path = os.path.join(project_root, "data", "processed").replace("\\", "/")
    
    # Auto-updating YAML with your exact computer path
    yaml_content = f"""
path: {processed_data_path}
train: train/images
val: val/images

names:
  0: Grade_A_Perfect
  1: Grade_B_Minor
  2: Grade_C_Reject
"""
    with open(yaml_path, "w") as f:
        f.write(yaml_content.strip())

    print(f"Dataset YAML successfully locked to absolute path: {processed_data_path}")

    model = YOLO("yolov8n.pt")
    
    print("Igniting YOLOv8 Vision Engine Custom Training...")
    
    model.train(
        data=yaml_path,
        epochs=1,
        imgsz=224,
        batch=4,
        project="models",
        name="yolo_vision_weights"
    )
    
    print("YOLO Training Test Epoch Complete. Engine is now ready for deployment.")

if __name__ == '__main__':
    train_yolo()