from django_filters import FilterSet, NumberFilter, CharFilter
from .models import Product

class ProductFilter(FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')

    price__gt = NumberFilter(field_name='price', lookup_expr='gt')
    price__lt = NumberFilter(field_name='price', lookup_expr='lt')

    vendor = CharFilter(field_name='vendor__username', lookup_expr='iexact')

    class Meta:
        model = Product
        fields = []