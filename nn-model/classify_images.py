from torchvision import transforms, models
from torchvision.datasets.utils import download_url
from torch.utils.data import DataLoader, Dataset
import subprocess
from PIL import Image
from pillow_heif import register_heif_opener
import torch
import os
import glob
import json
import sqlite3
import os


windows_image_paths = os.environ.get('FILE_PATH')
download_url("https://s3.amazonaws.com/deep-learning-models/image-models/imagenet_class_index.json", ".", "imagenet_class_index.json")

wsl_path = subprocess.check_output(['wslpath', windows_image_paths]).decode().strip()

image_extensions = ["*.HEIC", "*.heic"]
img_paths = []
for ext in image_extensions:
    img_paths.extend(glob.glob(os.path.join(wsl_path, ext)))

with open("imagenet_class_index.json") as f:
    class_idx = json.load(f)

# Invert the dictionary to map indices to class names
idx_to_class = {int(key): value[1] for key, value in class_idx.items()}

register_heif_opener()

def store_predictions(predictions):
    conn = sqlite3.connect('../database/pictures.db')
    cursor = conn.cursor()

    cursor.execute("BEGIN TRANSACTION;")
    for prediction in predictions:
        cursor.execute("INSERT INTO images (keywords) VALUES (?)", (idx_to_class[prediction.item()], ))
    conn.commit()
    conn.close()


# Example transform
transform = transforms.Compose([
    transforms.Resize((224, 224)), # ResNet input size
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Custom dataset to apply transformations
class ImageDataset(Dataset):
    def __init__(self, image_paths, transform=None):
        self.image_paths = image_paths
        self.transform = transform
    
    def __len__(self):
        return len(self.image_paths)
    
    def __getitem__(self, idx):
        image = Image.open(self.image_paths[idx])
        if self.transform:
            image = self.transform(image)
        return image

# Example usage
dataset = ImageDataset(img_paths, transform=transform)
dataloader = DataLoader(dataset, batch_size=32, shuffle=False, num_workers=4)

model = models.resnet101(weights='DEFAULT')
model.eval()  # Set the model to evaluation mode

with torch.no_grad():  # Disable gradient computation
    for batch in dataloader:
        outputs = model(batch)  # Perform inference
        _, preds = torch.max(outputs, 1)  # Get the predicted class
        print(preds)
        store_predictions(preds)

