from django.contrib import admin
from .models import Country, Category, CategoryUS, CategoryDE, Subcategory, ProductInfo


# Admin for Country
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')

# Admin for Category
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'link', 'country')
    list_filter = ('country',)
    search_fields = ('name', 'country__name')

# Admin for Subcategory
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'link', 'category', 'country')
    list_filter = ('category', 'country')
    search_fields = ('name', 'category__name', 'country__name')

# Admin for ProductInfo
class ProductInfoAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'store_name', 'seller_name', 'company_name', 'country', 'scraped', 'contacted')
    list_filter = ('main_category', 'sub_category', 'country', 'scraped', 'contacted')
    search_fields = ('product_name', 'store_name', 'seller_name', 'asin')
    raw_id_fields = ('main_category', 'sub_category', 'country')

# Admin for CategoryUS
class CategoryUSAdmin(admin.ModelAdmin):
    list_display = ('name', 'link', 'country')
    list_filter = ('country',)
    search_fields = ('name', 'country__name')

# Admin for CategoryDE
class CategoryDEAdmin(admin.ModelAdmin):
    list_display = ('name', 'link', 'country')
    list_filter = ('country',)
    search_fields = ('name', 'country__name')


admin.site.register(Country, CountryAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register(ProductInfo, ProductInfoAdmin)
admin.site.register(CategoryUS, CategoryUSAdmin)
admin.site.register(CategoryDE, CategoryDEAdmin)