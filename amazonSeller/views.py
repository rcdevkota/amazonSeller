# myapp/views.py
from django.shortcuts import render
from django.http import JsonResponse
from .models import Category
from django.core import serializers

from django.shortcuts import render, redirect
from .forms import PasswordForm

def home(request):
    return render(request, 'amazonseller/home.html')

def main_category(request):
    #data = fetch_amazon_best_sellers_main_category()
    data = Category.objects.all()
    # for item in data:
    #     category = Category(name=item['name'], link=item['url'])
    #     category.save()

    return JsonResponse({'message': 'Data added to the database', 'data': data})

#return all the main categories name and url as json response 
def get_main_category(request):
    categories = Category.objects.all()
    data = [{'name': category.name, 'link': category.link} for category in categories]
    return JsonResponse(data, safe=False)
