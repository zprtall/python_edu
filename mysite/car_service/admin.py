from django.contrib import admin
from .models import Company, Workshop, Worker, Order


class WorkshopInline(admin.TabularInline):
    model = Workshop
    extra = 1

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "legal_address", "unp")
    inlines = [WorkshopInline]


class WorkerInline(admin.TabularInline):
    model = Worker
    extra = 1

@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    list_display = ("company", "address", "capacity")
    inlines = [WorkerInline]
    list_filter = ("company",)


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "position", "workshop")
    list_filter = ("position", "workshop")
    search_fields = ("last_name", "first_name")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("type_work", "worker", "admin", "price")
    list_filter = ("worker__workshop__company", "worker__workshop")