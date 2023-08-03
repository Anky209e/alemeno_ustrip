from django.db import models

class UStrip(models.Model):
    image = models.FileField(upload_to='images')
    colors =  models.JSONField()

    