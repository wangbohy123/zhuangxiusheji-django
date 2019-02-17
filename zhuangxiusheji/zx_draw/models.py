from django.db import models

class ImagesForDraw(models.Model):

    image = models.ImageField(upload_to='images_for_draw/', null=False, blank=True)
    class Meta:
        db_table = 'draw_images'