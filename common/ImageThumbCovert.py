from PIL import Image
import io
from django.core.files.base import ContentFile


def image_to_thumb(obj, image_name, thumbSize=[300, 320]):
    image_file = getattr(obj, image_name)
    if image_file.name == "":
        return
    name, typ = image_file.name.split(".")
    image = Image.open(image_file)
    image.thumbnail(thumbSize)
    # img.save("te.jpg")
    dst_bytes = io.BytesIO()
    image.save(dst_bytes, typ)
    dst_bytes.seek(0)
    obj.thumb.save(name, ContentFile(dst_bytes.read()), save=False)
    dst_bytes.close()
    obj.save()
    return None
