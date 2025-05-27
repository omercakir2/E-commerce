# models.py
from django.db import models
from django.conf import settings 

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,  # allow existing products to have no user for now
        blank=True,
        related_name='products'
    )
    
    def __str__(self):
        return self.name