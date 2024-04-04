from django.db import models
from authentication.models import CustomUser

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Product(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='product_images/')
    bid_price = models.DecimalField(max_digits=10, decimal_places=2)
    min_bid_price = models.DecimalField(max_digits=10, decimal_places=2)

class Bid(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)

class ApprovedBid(BaseModel):
    bid = models.OneToOneField(Bid, on_delete=models.CASCADE)
    closed = models.BooleanField(default=False)
