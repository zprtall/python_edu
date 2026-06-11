from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Count, Avg, Q
from datetime import datetime
from .models import Order
from .validation_service import AdminButtonLogic
from .serializers import OrderSerializer


class Pagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_query_param = 'page'


def order_change_status(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    workshop = order.worker.workshop
    try:
        AdminButtonLogic.order_change_status_logic(order, workshop)
        order.save()
        messages.success(request, "Статус заказа обновлен")
    except Exception as e:
        messages.error(request, f"Ошибка: {str(e)}")
    return redirect(request.META.get('HTTP_REFERER', '/admin/'))


class MonthlyStatistics(GenericViewSet):
    @action(detail=True, methods=["get"], url_path="company")
    def company_stats(self,request, pk=None):
        start_date, end_date = self.date_processing(request)
        orders = Order.objects.filter(
            worker__workshop__company_id=pk,
            arrival_time__gte=start_date,
            arrival_time__lt=end_date
        )
        data = orders.aggregate(
            total_orders=Count("id"),
            total_revenue=Sum("price"),
            avg_price=Avg("price")
        )
        return Response(data)

    @action(detail=True, methods=["get"], url_path="workshop")
    def workshop_stats(self, request, pk=None):
        start_date, end_date = self.date_processing(request)
        orders = Order.objects.filter(
            worker__workshop_id=pk,
            arrival_time__gte=start_date,
            arrival_time__lt=end_date
        )
        data = orders.aggregate(
            total_orders=Count("id"),
            total_revenue=Sum("price"),
            avg_price=Avg("price")
        )
        return Response(data)

    @action(detail=True, methods=["get"], url_path="worker")
    def worker_stats(self, request, pk=None):
        start_date, end_date = self.date_processing(request)

        orders = Order.objects.filter(
            worker_id=pk,
            arrival_time__gte=start_date,
            arrival_time__lt=end_date
        )
        data = orders.aggregate(
            total_orders=Count("id"),
            total_revenue=Sum("price"),
            avg_price=Avg("price")
        )
        return Response(data)

    def date_processing(self, request):
        try:
            year = int(request.GET.get("year", datetime.now().year))
            month = int(request.GET.get("month", datetime.now().month))
        except (TypeError, ValueError):
            year = datetime.now().year
            month = datetime.now().month
        year = int(request.GET.get("year"))
        month = int(request.GET.get("month"))
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)
        return start_date, end_date


class MonthlyOrders(GenericViewSet):
    pagination_class = Pagination
    @action(detail=True, methods=["get"], url_path="company")
    def company_order_list(self,request, pk = None):
        start_date, end_date = self.date_processing(request)
        filters = Q(worker__workshop__company_id=pk,arrival_time__gte=start_date, arrival_time__lt=end_date)
        filters &= self.get_filter(request)
        orders = Order.objects.filter(filters).select_related('worker', 'admin')
        page = self.paginate_queryset(orders)
        if page is not None:
            serializer = OrderSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path="workshop")
    def workshop_order_list(self,request, pk = None):
        start_date, end_date = self.date_processing(request)
        filters = Q(worker__workshop_id=pk, arrival_time__gte=start_date, arrival_time__lt=end_date)
        filters &= self.get_filter(request)
        orders = Order.objects.filter(filters).select_related('worker', 'admin')
        page = self.paginate_queryset(orders)
        if page is not None:
            serializer = OrderSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)



    def date_processing(self, request):
        try:
            year = int(request.GET.get("year", datetime.now().year))
            month = int(request.GET.get("month", datetime.now().month))
        except (TypeError, ValueError):
            year = datetime.now().year
            month = datetime.now().month
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)
        return start_date, end_date

    def get_filter(self,request):
        type_work = request.GET.get("type_work")
        worker_id = request.GET.get("worker")
        admin_id = request.GET.get("admin")
        min_price = request.GET.get("min_price")
        max_price = request.GET.get("max_price")
        if min_price is not None:
            try:
                min_price = float(min_price)
            except ValueError:
                min_price = None
        if max_price is not None:
            try:
                max_price = float(max_price)
            except ValueError:
                max_price = None
        if worker_id:
            try:
                worker_id = int(worker_id)
            except ValueError:
                worker_id = None
        if admin_id:
            try:
                admin_id = int(admin_id)
            except ValueError:
                admin_id = None

        filters = Q()

        if type_work:
            filters &= Q(type_work=type_work)
        if worker_id:
            filters &= Q(worker_id=worker_id)
        if admin_id:
            filters &= Q(admin_id=admin_id)
        if min_price is not None:
            filters &= Q(price__gte=min_price)
        if max_price is not None:
            filters &= Q(price__lte=max_price)

        return filters


