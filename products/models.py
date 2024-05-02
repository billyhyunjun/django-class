from django.db import models
from django.conf import settings


class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    context = models.TextField()
    image = models.ImageField(blank=True, null=True)
