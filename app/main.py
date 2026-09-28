from fastapi import FastAPI, UploadFile, File, Form
from PIL import Image
from io import BytesIO

app = FastAPI(title='Multimodal AI Assistant')

def inspect_image(data: bytes) -> dict[str, int | str]:
    image = Image.open(BytesIO(data))
    return {'format': image.format or 'unknown', 'width': image.width, 'height': image.height}

@app.get('/health')
def health(): return {'status': 'ok'}

@app.post('/analyze')
async def analyze(instruction: str = Form(...), image: UploadFile = File(...)):
    metadata = inspect_image(await image.read())
    return {'instruction': instruction, 'image': metadata, 'answer': f"Image received for instruction: {instruction}"}
