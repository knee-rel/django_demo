from datetime import date
from .models import Product, QuotationForm, Customer, Checkout
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib import messages
from .filters import ProductFilter
import json

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
    latest_products = Product.objects.order_by('-date')[:3]
    return render(request, "store/index.html", {
        "products": latest_products,
        "messages": messages.get_messages(request)  
    })


def products(request):
    all_products = Product.objects.all()
    product_filter = ProductFilter(request.GET, queryset=all_products)
    
    return render(request, "store/all_products.html", {
        # "all_products": all_products
        "all_products": product_filter.qs,
        "filter": product_filter
    })


def product_detail(request, slug):
    identified_product = get_object_or_404(Product, slug=slug)
    return render(request, "store/product_detail.html", {
        "product": identified_product
    })


def add_to_quotation(request, slug):
    # Get the product by its slug
    product = get_object_or_404(Product, slug=slug)

    # Initialize the quotation form in session if not already there
    quotation_form = request.session.get('quotation_form', {})

    # Check if the product is already in the quotation form
    if slug in quotation_form:
        # If it already exists in the quotation, increase the quantity
        quotation_form[slug]['quantity'] += 1
    else:
        # Add the product to the quotation form
        quotation_form[slug] = {
            'title': product.title,
            # Convert to string for session storage
            'price': str(product.price),
            'quantity': 1,
            'image': product.image_name  # Add image URL for displaying later
        }

    # Save the updated quotation form back into the session
    request.session['quotation_form'] = quotation_form
    print("Updated Quotation Form: ", request.session['quotation_form'])

    return redirect('quotation-page')  # Redirect to the quotation form page

@csrf_exempt  # Use this for testing, but be cautious with security!
def update_quantity(request, slug):
    if request.method == "POST":
        data = json.loads(request.body)
        quantity = data.get('quantity', 0)

        # Get the current quotation form from the session
        quotation_form = request.session.get('quotation_form', {})

        if slug in quotation_form:
            if quantity > 0:
                quotation_form[slug]['quantity'] = quantity
            else:
                # Remove the item if quantity is 0
                del quotation_form[slug]

        request.session['quotation_form'] = quotation_form
        total_price = sum(float(item['price']) * item['quantity'] for item in quotation_form.values())

        return JsonResponse({'total_price': total_price})

    return JsonResponse({'error': 'Invalid request'}, status=400)



def quotation_page(request):
    # Get the quotation form from session
    quotation_form = request.session.get('quotation_form', {})
    print("Quotation Form:", quotation_form)

    # Calculate the total price
    total_price = sum(float(item['price']) * item['quantity']
                      for item in quotation_form.values())

    return render(request, "store/quotation.html", {
        "quotation_items": quotation_form,
        "total_price": total_price
    })

def checkout_page(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')

        # Here, you can save the customer information to the database
        customer = Customer(first_name=first_name, last_name=last_name, email_address=email)
        customer.save()
        
        # Create a Checkout record
        checkout = Checkout(customer=customer)
        checkout.save()

        # Optionally, you could create a QuotationForm entry here as well
        quotation_form = request.session.get('quotation_form', {})
        for slug, item in quotation_form.items():
            product = get_object_or_404(Product, slug=slug)
            quotation_entry = QuotationForm(customer=customer, product=product, quantity=item['quantity'])
            quotation_entry.save()

        # Clear the quotation form from the session
        del request.session['quotation_form']
        
        messages.success(request, "Checkout completed successfully!")

        return redirect('starting-page')  # Redirect after successful checkout

    return render(request, "store/checkout.html")
