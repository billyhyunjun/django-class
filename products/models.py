from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    context = models.TextField()
    image = models.ImageField(blank=True, null=True)
