from django.db import models

class UStrip(models.Model):
    """
    Django Model for saving images and color data for later use
    """
    image = models.FileField(upload_to='images')
    colors =  models.JSONField()

    