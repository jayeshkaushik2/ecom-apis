from PIL import Image
import io
from django.core.files.base import ContentFile


def image_to_thumb(obj, image_name, thumbSize=[300, 320]):
    image = getattr(obj, image_name)
    name, typ = image.name.split(".")
    img = Image.open(image)
    img.thumbnail(thumbSize)
    img.save("te.jpg")
    thumb = io.BytesIO()
    obj.thumb.save(f"thumb-{obj.id}.{typ}", thumb)
    obj.save()
    return None
