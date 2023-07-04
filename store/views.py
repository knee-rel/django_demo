from django.shortcuts import render

# Create your views here.

def starting_page(request):
  return render(request, "store/index.html")

def products(request):
  pass

def product_detail(request):
  pass