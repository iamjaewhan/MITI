from django.db import models

# Create your models here.
class PlaceTypeChoices(models.TextChoices):
    INDOOR = 'IN', 'indoor'
    OUTDOOR = 'OUT', 'outdoor'


class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=255, unique=True)
    address_detail = models.CharField(max_length=50, null=True)
    contact = models.CharField(max_length=50)
    info = models.CharField(max_length=255, null=True)
    type = models.CharField(max_length=20, choices=PlaceTypeChoices.choices)

    def __str__(self):
        return self.name