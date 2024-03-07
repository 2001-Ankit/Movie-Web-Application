from typing import Any
from django.db import models

# Create your models here.

class Movie(models.Model):
    name = models.CharField(max_length=400)
    image_src = models.URLField()
    image_alt = models.CharField(max_length=400)
    duration= models.CharField(max_length=400)	
    rate = models.CharField(max_length=400)
    votes = models.CharField(max_length=600)
    alt_image = models.CharField(max_length=255,null=True)
    src_image = models.URLField(null=True)
    def __init__(self):
        return self.name
    

        
