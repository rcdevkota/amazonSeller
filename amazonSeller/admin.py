from django.contrib import admin
from .models import Category, SellerInfo, Subcategory, Products

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('categoryID', 'name','link')
    search_fields = ['name']
    link = ['link']

class SellerInfoAdmin(admin.ModelAdmin):
    list_display = ('sellerID', 'sellerName', 'email', 'nummer', 'contacted')
    search_fields = ['sellerName', 'email']

# Define Admin classes for Subcategory and Products similarly...

# Register your models here with their respective ModelAdmin classes
admin.site.register(Category, CategoryAdmin)
admin.site.register(SellerInfo, SellerInfoAdmin)
# ...similarly for Subcategory and Products
