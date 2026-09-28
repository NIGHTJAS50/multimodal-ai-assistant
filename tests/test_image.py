from PIL import Image
from io import BytesIO
from app.main import inspect_image

def test_image_metadata_is_read():
    buffer = BytesIO()
    Image.new('RGB', (3, 4), 'red').save(buffer, format='PNG')
    result = inspect_image(buffer.getvalue())
    assert result == {'format': 'PNG', 'width': 3, 'height': 4}
