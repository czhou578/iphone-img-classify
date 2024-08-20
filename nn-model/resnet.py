from torchvision import models, transforms
from PIL import Image
from pillow_heif import register_heif_opener
import torch

resnet = models.resnet101(pretrained=True)
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

register_heif_opener()

img = Image.open('./test_images/IMG_1855.HEIC')

img_t = transform(img)

batch_t = torch.unsqueeze(img_t, 0)

resnet.eval()

out = resnet(batch_t)

with open('basic_labels.txt') as f:
    classes = [line.strip() for line in f.readlines()]


_, indices = torch.sort(out, descending=True)
percentage = torch.nn.functional.softmax(out, dim=1)[0] * 100

print([(classes[idx], percentage[idx].item()) for idx in indices[0][:5]])
