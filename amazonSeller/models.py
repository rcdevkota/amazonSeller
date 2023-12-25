from django.db import models

class Category(models.Model):
    categoryID = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)

class SellerInfo(models.Model):
    sellerID = models.BigAutoField(primary_key=True)
    sellerName = models.CharField(max_length=255)
    amazonID = models.CharField(max_length=255)
    email = models.EmailField()
    nummer = models.IntegerField()
    adresse = models.CharField(max_length=255)
    productsType = models.CharField(max_length=255)
    contacted = models.BooleanField()

class Subcategory(models.Model):
    categoryID = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    link = models.CharField(max_length=255)

class Products(models.Model):
    productID = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    amazonID = models.CharField(max_length=255)
    sellerID = models.ForeignKey(SellerInfo, on_delete=models.CASCADE)
    subCategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
