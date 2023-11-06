from django.db import models

class ProductCategory(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(blank=False)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=256, unique=True)
    # image = models.ImageField(upload_to='', blank=False)
    description = models.TextField(blank=False)
    price = models.PositiveBigIntegerField()
    quantity = models.PositiveBigIntegerField(default=0)
    category = models.ForeignKey('ProductCategory', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


