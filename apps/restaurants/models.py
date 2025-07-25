from django.contrib.gis.db.models import PointField
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

class Category(MPTTModel):
    name = models.CharField(max_length=255)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', default=None)
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE, null=False, related_name='categories')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name

class Promotion(models.Model):
    class PromotionType(models.TextChoices):
        AKSIYA = '1+1_aksiya', '1+1 Aksiyasi'
        FREE_DELIVERY = 'free_delivery', 'Bepul yetkazib berish'
        AKSIYA2 = '2+1_aksiya', '2+1 Aksiyasi'

    name = models.CharField(max_length=255, choices=PromotionType.choices)

    def __str__(self):
        return self.name

class Restaurant(MPTTModel):
    name = models.CharField(max_length=255)
    location = PointField(srid=4326, null=True, blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='branches')
    promotions = models.ManyToManyField(Promotion, related_name='restaurants', blank=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name