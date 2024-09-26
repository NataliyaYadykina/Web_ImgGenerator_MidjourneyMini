# pipeline.py
import torch
from diffusers import StableDiffusionPipeline

# Загрузка предобученной модели "midjourney-mini"
model_id = "openskyml/midjourney-mini"
pipeline = StableDiffusionPipeline.from_pretrained(
    model_id, torch_dtype=torch.float32)
pipeline = pipeline.to("cuda" if torch.cuda.is_available() else "cpu")


def generate_image_from_text(description):
    # Генерация изображения на основе текстового описания
    with torch.no_grad():
        image = pipeline(description).images[0]
    return image
