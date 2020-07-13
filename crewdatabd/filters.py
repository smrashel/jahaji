import django_filters
from .models import *


class ShippingStaffFilter(django_filters.FilterSet):
    class Meta:
        model = ShippingStaff
        fields = ['full_name', 'contact_number']