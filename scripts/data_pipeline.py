import os
import shutil
import random

source_dir = "data/raw_data"
train_img_dir = "data/processed/train/images"
val_img_dir = "data/processed/val/images"

os.makedirs(train_img_dir, exist_ok=True)
os.makedirs(val_img_dir, exist_ok=True)

def distribute_data():
    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp')
    all_files = []
    
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.lower().endswith(valid_extensions):
                all_files.append(os.path.join(root, file))
    
    if not all_files:
        print("Error: No images found. Make sure dataset is extracted inside data/raw_data folder.")
        return

    random.shuffle(all_files)
    split_idx = int(len(all_files) * 0.8)
    
    train_files = all_files[:split_idx]
    val_files = all_files[split_idx:]

    for f in train_files:
        shutil.copy(f, os.path.join(train_img_dir, os.path.basename(f)))
    for f in val_files:
        shutil.copy(f, os.path.join(val_img_dir, os.path.basename(f)))

    print(f"Data Pipeline Ready: {len(train_files)} Train images, {len(val_files)} Validation images structured.")

if __name__ == '__main__':
    distribute_data()