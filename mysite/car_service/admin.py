from django.contrib import admin
from django.urls import path
from .models import Company, Workshop, Worker, Order
from django.utils.html import format_html
from django.urls import reverse
from .views import order_change_status


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
    if not Order.delivery_acceptance_time:
        list_display = ("type_work", "worker", "admin", "price", "finding", "change_status_button")
    else:
        list_display = ("type_work", "worker", "admin", "price", "finding", "change_status_button", "delivery_acceptance_time")

    list_filter = ("worker__workshop__company", "worker__workshop")

    def get_urls(self):
        urls = super().get_urls()

        custom_urls = [
            path(
                "<int:order_id>/change-status/",
                self.admin_site.admin_view(order_change_status),
                name="order-change-status",
            ),
        ]

        return custom_urls + urls

    def change_status_button(self, obj):
        if not obj.finding == obj.Spaces.OWNER:
            url = reverse("admin:order-change-status", args=[obj.id])
            return format_html(
                '<a class="button" href="{}">поменять статус</a>',
                url
            )
        return "—"
    change_status_button.short_description = "Сменить статус"