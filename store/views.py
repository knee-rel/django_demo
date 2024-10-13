from datetime import date

from django.shortcuts import render

# Create your views here.

all_products = [
  {
    "slug": "jeans-for-sale",
    "title": "Jeans",
    "image": "jeans.png",
    "price": 1000,
    "description": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Officiis nobis aperiam est praesentium, quos iste consequuntur omnis exercitationem quam velit labore vero culpa ad mollitia? Quis architecto ipsam nemo. Odio.",
    "availability": True,
    "date": date(2023, 6, 21),
    "categories": "Clothing"
  },
  {
    "slug": "eyewear",
    "title": "Eyewear",
    "image": "eyewear.jpeg",
    "price": 2000,
    "description": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Officiis nobis aperiam est praesentium, quos iste consequuntur omnis exercitationem quam velit labore vero culpa ad mollitia? Quis architecto ipsam nemo. Odio.",
    "availability": True,
    "date": date(2023, 6, 10),
    "categories": "Eyewear"
  },
  {
    "slug": "shirt",
    "title": "Shirt",
    "image": "shirt.png",
    "price": 500,
    "description": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Officiis nobis aperiam est praesentium, quos iste consequuntur omnis exercitationem quam velit labore vero culpa ad mollitia? Quis architecto ipsam nemo. Odio.",
    "availability": True,
    "date": date(2023, 6, 22),
    "categories": "Clothing",
  },
  {
    "slug": "shop_img",
    "title": "Shop",
    "image": "shop_img.jpg",
    "price": 500,
    "description": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Officiis nobis aperiam est praesentium, quos iste consequuntur omnis exercitationem quam velit labore vero culpa ad mollitia? Quis architecto ipsam nemo. Odio.",
    "availability": False,
    "date": date(2023, 6, 2),
    "categories": "Shop",
  },
]

def get_date(product):
  return product['date']

def starting_page(request):
  sorted_products = sorted(all_products, key=get_date)
  latest_products = sorted_products[-3:]
  return render(request, "store/index.html", {
    "products": latest_products
  })

def products(request):
  return render(request, "store/all_products.html", {
    "all_products": all_products
  })

def product_detail(request, slug):
  identified_product = next(product for product in all_products if product['slug'] == slug)
  return render(request, "store/product_detail.html", {
    "product": identified_product
  })