from django.shortcuts import render, get_object_or_404
from .models import Category, Product


# Create your views here.
def store(request):

    all_products = Product.objects.all()

    context = {"all_products": all_products}

    return render(request, "store/store.html", context)


# context processor is a python function that takes request argument and returns a dictonary that gets added to the template context
def categories(request):

    all_categories = Category.objects.all()

    return {"all_categories": all_categories}


def list_category(request, slug):

    categories = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=categories)
    context = {"categories": categories, "products": products}
    return render(request, "store/list_category.html", context)


def product_info(request, slug):
    
    product = get_object_or_404(Product, slug=slug)
    context = {"product": product}
    return render(request, "store/product_info.html", context)
