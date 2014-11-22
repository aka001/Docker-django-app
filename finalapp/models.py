from django.db import models
from django.contrib.auth.models import User

class Container(models.Model):
    uid=models.CharField(max_length=200)
    name_image=models.CharField(max_length=200)
    id_container=models.CharField(max_length=200)

class Image(models.Model):
    uid=models.CharField(max_length=200)
    name=models.CharField(max_length=200)
    id_images=models.CharField(max_length=200)

# Create your models here.
