from django.db import models

# Create your models here.


class Recipe (models.Model):
    name = models.CharField(max_length=50)
    cooking_time = models.FloatField(help_text='In minutes')
    ingredients = models.CharField(max_length=225)
    description = models.TextField()

def __str__(self):
    return str(self.name)