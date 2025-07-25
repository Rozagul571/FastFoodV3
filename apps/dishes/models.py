from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from apps.restaurants.models import Restaurant, Promotion

class SubCategory(MPTTModel):
    name = models.CharField(max_length=255)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True, blank=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.parent and not self.restaurant:
            self.restaurant = self.parent.restaurant
        super().save(*args, **kwargs)

class Dish(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    promotion = models.ForeignKey(Promotion, on_delete=models.SET_NULL, null=True, blank=True, related_name='dishes')
    category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='dishes')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def adjusted_quantity(self):
        if self.promotion and self.promotion.name == '1+1_aksiya':
            return self.quantity + 1  # Har bir uchun 1 ta bonus
        elif self.promotion and self.promotion.name == '2+1_aksiya':
            return self.quantity + (self.quantity // 2)  # Har 2 taga 1 ta bonus
        return self.quantity

    @property
    def promotion_price(self):
        return self.price  # Aksiya narxni o'zgartirmaydi, faqat miqdor oshadi

    def save(self, *args, **kwargs):
        if self.category and not self.restaurant:
            self.restaurant = self.category.restaurant
        # Promotion ni restoran promtionlaridan olish
        if self.restaurant and self.restaurant.promotions.exists() and not self.promotion:
            # Birinchi promotionni tanlaymiz
            self.promotion = self.restaurant.promotions.first()
        super().save(*args, **kwargs)