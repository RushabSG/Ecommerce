from django.db.models import signals
from django.conf import settings
from django.dispatch import receiver
import os

from .models import Product


# To remove the Image if the Model object is deleted from database
@receiver(signals.post_delete, sender=Product)
def delete_static_image_on_object_delete(sender, instance, **kwargs):
    # ensure the image field is not empty
    if instance.images:
        # path for static images
        image_path = os.path.join(settings.MEDIA_ROOT, instance.images.name)
        # delete if the file exists
        if os.path.isfile(image_path):
            os.remove(image_path)
