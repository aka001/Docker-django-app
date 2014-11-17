from django.db import models
from django.contrib.auth.models import User

class Containers(models.Model):
	user = models.ManyToManyField(User)
	name=models.CharField(max_length=200)
	id_container=models.CharField(max_length=200)

# Create your models here.
