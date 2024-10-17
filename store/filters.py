from django_filters import FilterSet, CharFilter
from .models import Product

class ProductFilter(FilterSet):
    title = CharFilter(field_name='title', lookup_expr='icontains', label='Search Product')
    # min_price = CharFilter(field_name='price', lookup_expr='gte', label='Min price')
    # max_price = CharFilter(field_name='price', lookup_expr='lte', label='Max price')
    
    class Meta:
        model = Product
        fields = ['title', 'categories']