from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator

# Create your models here.


class Category(models.Model):
    caption = models.CharField(max_length=20)

    def __str__(self):
        return self.caption


class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email_address = models.EmailField()

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name


class Product(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, db_index=True)
    image_name = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField(auto_now=True)
    description = models.TextField(validators=[MinLengthValidator(10)])
    categories = models.ManyToManyField(Category)
    inventory_count = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(0)]
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.title

    @property
    def availability(self):
        return self.inventory_count > 0


class QuotationForm(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.title} (x{self.quantity})"
