from django.urls import path

from . import views

urlpatterns = [
    path("", views.starting_page, name="starting-page"),
    path("products", views.products, name="products-page"),
    path("products/<slug:slug>", views.product_detail,
         name="product-detail-page")  # /products/my-first-product
]
