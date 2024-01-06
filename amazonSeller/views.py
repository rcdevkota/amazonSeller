# myapp/views.py
from django.shortcuts import render
# from .categoryScrape import fetch_amazon_best_sellers_main_category
from django.http import JsonResponse
from .models import Category

def home(request):
    return render(request, 'amazonseller/home.html')

def main_category(request):
    #data = fetch_amazon_best_sellers_main_category()
    data = Category.objects.all()
    # for item in data:
    #     category = Category(name=item['name'], link=item['url'])
    #     category.save()

    return JsonResponse({'message': 'Data added to the database', 'data': data})
