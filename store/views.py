from django.shortcuts import render

# Create your views here.

def starting_page(request):
  return render(request, "store/index.html")

def products(request):
  return render(request, "store/all_products.html")

def product_detail(request, slug):
  return render(request, "store/product_detail.html")