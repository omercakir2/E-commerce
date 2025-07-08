from django.db import models
from users.models import CustomUser
from products.models import Product
# Create your models here.
class Card(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)

    def __str__(self):
        return f"product_id = {self.product.id} user_id = {self.user.id} "