from django.contrib import admin
from .models import Company, Workshop, Worker, Order

admin.site.register(Company)
admin.site.register(Workshop)
admin.site.register(Worker)
admin.site.register(Order)

# Register your models here.
