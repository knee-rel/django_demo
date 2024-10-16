from django.urls import path

from . import views

urlpatterns = [
    path("", views.starting_page, name="starting-page"),
    path("products", views.products, name="products-page"),
    path("products/<slug:slug>", views.product_detail,
         name="product-detail-page"),  # /products/my-first-product
    path('add-to-quotation/<slug:slug>/',
         views.add_to_quotation, name='add-to-quotation'),
    path('quotation/', views.quotation_page, name='quotation-page'),
    path('update-quantity/<slug>/', views.update_quantity, name='update-quantity'),
    path('checkout/', views.checkout_page, name='checkout-page'),
]
