
import io
import json
import torch
import torch.nn as nn

from torchvision import models
from torchvision import transforms
from PIL import Image


imagenet_class_index = json.load(open('static/imagenet_class_index.json'))
monumentmonitor_class_index = json.load(open('static/mm_sites.json'))
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# Make sure to pass `pretrained` as `True` to use the pretrained weights:
model = models.densenet121(pretrained=True)
model.to(device)
# Since we are using our model only for inference, switch to `eval` mode:
model.eval()


model_conv = models.resnet18(pretrained=True)
num_ftrs = model_conv.fc.in_features
model_conv.fc = nn.Linear(num_ftrs, 20)
model_conv = model_conv.to(device)
model_conv.load_state_dict(torch.load("https://monument-monitor-reports.s3.eu-west-2.amazonaws.com/model_6_30e_conv.pt", map_location=torch.device(device)))
model_conv.eval()


def transform_image(image_bytes):
    my_transforms = transforms.Compose([transforms.Resize(256),
                                        transforms.CenterCrop(224),
                                        transforms.ToTensor(),
                                        transforms.Normalize(
                                            [0.485, 0.456, 0.406],
                                            [0.229, 0.224, 0.225])])
    image = Image.open(io.BytesIO(image_bytes))
    return my_transforms(image).unsqueeze(0)


def get_prediction(image_bytes):
    tensor = transform_image(image_bytes=image_bytes).to(device)
    outputs = model.forward(tensor)
    _, y_hat = outputs.max(1)
    predicted_idx = str(y_hat.item())
    return imagenet_class_index[predicted_idx]


def batch_prediction(image_bytes_batch):
    image_tensors = [transform_image(image_bytes=image_bytes) for image_bytes in image_bytes_batch]
    tensor = torch.cat(image_tensors).to(device)
    outputs = model_conv.forward(tensor)
    _, y_hat = outputs.max(1)
    predicted_ids = y_hat.tolist()
    print(predicted_ids)
    return [monumentmonitor_class_index[str(i)] for i in predicted_ids]


if __name__ == "__main__":
    with open(r"static/animage.jpg", 'rb') as f:
        image_bytes = f.read()

    result = get_prediction(image_bytes)
    print(result)
    batch_result = batch_prediction([image_bytes] * 64)
    assert batch_result == [result] * 64