from django.db import models
from product_configuration.models import ColorCategory, BrandCategory, Storage, Condition, ProductModelCategory, LockStatus, Category, Location

class MobilePhones(models.Model):
    title = models.CharField(max_length=255)
    sold_price = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2)
    ebay_item_id = models.IntegerField()
    product_url = models.TextField()
    image = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    product_model = models.ForeignKey(ProductModelCategory, on_delete=models.SET_NULL, null=True)
    brand = models.ForeignKey(BrandCategory, on_delete=models.SET_NULL, null=True)
    color = models.ForeignKey(ColorCategory, on_delete=models.SET_NULL, null=True)
    storage = models.ForeignKey(Storage, on_delete=models.SET_NULL, null=True)
    lock_status = models.ForeignKey(LockStatus, on_delete=models.SET_NULL, null=True)
    condition = models.ForeignKey(Condition, on_delete=models.SET_NULL, null=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    sold_date = models.DateField()
    created_ad = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('title', 'sold_date', 'product_url')

