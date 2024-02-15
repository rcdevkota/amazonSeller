# your_app_name/views/category_views.py

from django.shortcuts import render, get_object_or_404
from ..models import Category


def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    return render(request, 'your_app_name/category_detail.html', {'category': category})


