import clip
import torch
from PIL import Image, ImageOps

device = "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

def preprocess_image(image: Image.Image, size=(224, 224)) -> Image.Image:
    """
    Простая предобработка для скриншотов на белом фоне:
    - конвертация в RGB
    - обрезка полностью белых краёв
    - масштабирование
    """
    image = image.convert("RGB")
    
    # Инвертируем, чтобы белое стало черным
    inverted = ImageOps.invert(image)
    bbox = inverted.getbbox()  # bounding box непустых пикселей
    if bbox:
        image = image.crop(bbox)
    
    # Масштабирование под CLIP
    image = image.resize(size)
    return image

def get_embedding(image: Image.Image) -> torch.Tensor:
    """
    Получение эмбеддинга изображения через CLIP с предобработкой
    """
    image = preprocess_image(image)
    image_tensor = preprocess(image).unsqueeze(0).to(device)
    
    with torch.no_grad():
        emb = model.encode_image(image_tensor)
        emb /= emb.norm(dim=-1, keepdim=True)
    
    return emb

