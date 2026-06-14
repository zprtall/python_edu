import django_filters
from .models import Order

class OrderListFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    class Meta:
        model = Order
        fields ={
            'type_work' : ['exact'],
            'worker_id' : ['exact'],
            'admin_id' : ['exact']
        }