import os

gitignore_content = """
venv/
__pycache__/
data/raw_data/
models/gan_checkpoints/
models/yolo_weights/
*.pt
.env
"""

with open(".gitignore", "w") as file:
    file.write(gitignore_content.strip())

req_content = """
torch
torchvision
torchaudio
ultralytics
"""

with open("requirements.txt", "w") as file:
    file.write(req_content.strip())

print("Professional Git guardrails and requirements established.")