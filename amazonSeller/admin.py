from django.contrib import admin
from .models import Country, Category, CategoryUS, CategoryDE, Subcategory, ProductInfo

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')

# Base admin class to filter by country
class CountrySpecificAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if hasattr(self.model, 'country'):
            country_code = 'US' if 'US' in self.model.__name__ else 'DE'
            country = Country.objects.filter(code=country_code).first()
            if country:
                return qs.filter(country=country)
        return qs

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "country":
            country_code = 'US' if 'US' in self.model.__name__ else 'DE'
            kwargs["queryset"] = Country.objects.filter(code=country_code)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

# Register US and DE Categories
@admin.register(CategoryUS)
class CategoryUSAdmin(CountrySpecificAdmin):
    pass

@admin.register(CategoryDE)
class CategoryDEAdmin(CountrySpecificAdmin):
    pass

# Similar registrations for SubcategoryUS, SubcategoryDE, ProductInfoUS, and ProductInfoDE
