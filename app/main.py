from fastapi import FastAPI, UploadFile, File, Form
from PIL import Image
from io import BytesIO
import os
from functools import lru_cache

app = FastAPI(title='Multimodal AI Assistant')

def inspect_image(data: bytes) -> dict[str, int | str]:
    image = Image.open(BytesIO(data))
    return {'format': image.format or 'unknown', 'width': image.width, 'height': image.height}

@lru_cache(maxsize=1)
def get_captioner():
    from transformers import pipeline
    return pipeline('image-to-text', model=os.getenv('VISION_MODEL', 'Salesforce/blip-image-captioning-base'))

@app.get('/health')
def health(): return {'status': 'ok'}

@app.post('/analyze')
async def analyze(instruction: str = Form(...), image: UploadFile = File(...)):
    data = await image.read()
    metadata = inspect_image(data)
    answer = f"Image received for instruction: {instruction}"
    if os.getenv('ENABLE_VISION_MODEL', 'false').lower() == 'true':
        result = get_captioner()(Image.open(BytesIO(data)))
        answer = result[0].get('generated_text', answer)
    return {'instruction': instruction, 'image': metadata, 'answer': answer, 'model_enabled': os.getenv('ENABLE_VISION_MODEL', 'false').lower() == 'true'}
