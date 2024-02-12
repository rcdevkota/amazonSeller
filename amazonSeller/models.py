from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=2, unique=True)
    def __str__(self):
        return self.name
    

class Category(models.Model):
    name = models.CharField(max_length=255, null=True)  # Assuming category names are unique
    link = models.URLField(max_length=255, null=True)
    country = models.ForeignKey(Country,on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.name
    class Meta:
        unique_together = ('name', 'country')

class Subcategory(models.Model):
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=255, null=True)
    link = models.URLField(max_length=255, null=True)
    country = models.ForeignKey(Country,on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

class Us_productInfo(models.Model):
    asin = models.CharField(max_length=255)
    main_category = models.ForeignKey(Category,  on_delete=models.CASCADE, default=None, null=True)
    sub_category = models.ForeignKey(Subcategory,  on_delete=models.CASCADE, default=None, null=True)
    product_name = models.CharField(max_length=500, null=True)
    store_name = models.CharField(max_length=255, null=True)
    seller_name = models.CharField(max_length=255, null=True)
    seller_id = models.CharField(max_length=255, null=True)
    company_name = models.CharField(max_length=255, null=True)
    email = models.EmailField(null=True)
    phone_number = models.CharField(max_length=255, null=True)
    address = models.TextField(null=True)
    about_seller = models.TextField(null=True)
    seller_detailed_info = models.TextField(null=True)
    scraped = models.BooleanField(default=False)
    contacted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product_name} by {self.store_name}"


class De_productInfo(models.Model):
    asin = models.CharField(max_length=255)
    main_category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None, null=True)
    sub_category = models.ForeignKey(Subcategory, on_delete=models.CASCADE, default=None, null=True)
    product_name = models.CharField(max_length=500, null=True)
    store_name = models.CharField(max_length=255, null=True)
    seller_name = models.CharField(max_length=255, null=True)
    seller_id = models.CharField(max_length=255, null=True)
    company_name = models.CharField(max_length=255, null=True)
    email = models.EmailField(null=True)
    phone_number = models.CharField(max_length=255, null=True)
    address = models.TextField(null=True)
    about_seller = models.TextField(null=True)
    seller_detailed_info = models.TextField(null=True)
    scraped = models.BooleanField(default=False)
    contacted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product_name} by {self.store_name}"
    
class CategoryUS(Category):
    class Meta:
        proxy = True
        verbose_name = 'US Category'
        verbose_name_plural = 'US Categories'

class CategoryDE(Category):
    class Meta:
        proxy = True
        verbose_name = 'DE Category'
        verbose_name_plural = 'DE Categories'