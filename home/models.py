from django.db import models

# Create your models here.
class template(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    photo = models.ImageField(upload_to='templates_images')