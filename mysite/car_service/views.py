from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import mixins, viewsets
from django.db.models import Sum, Count, Avg
from datetime import datetime
from .models import Order, Company, Workshop, Worker
from .validation_service import AdminButtonLogic
from .serializers import OrderSerializer, CompanyViewSerializer, WorkshopViewSerializer, WorkerViewSerializer
from .serializers import DateQuerySerializer
from .filters import OrderListFilter


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


def date_processing(request):
    serializer = DateQuerySerializer(data=request.GET)
    serializer.is_valid(raise_exception=True)
    year = serializer.validated_data["year"]
    month = serializer.validated_data["month"]
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1)
    else:
        end_date = datetime(year, month + 1, 1)
    return start_date, end_date


class CompanyViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanyViewSerializer
    pagination_class = Pagination

    @action(detail=True, methods=["get"], url_path="orders")
    def company_order_list(self, request, pk=None):
        start_date, end_date = date_processing(request)
        queryset = Order.objects.filter(
            worker__workshop__company_id=pk,
            arrival_time__gte=start_date,
            arrival_time__lt=end_date
        ).select_related('worker', 'admin')
        filterset = OrderListFilter(request.GET, queryset=queryset)
        if filterset.is_valid():
            queryset = filterset.qs
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = OrderSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"], url_path="stats")
    def company_stats(self, request, pk=None):
        start_date, end_date = date_processing(request)
        queryset = Order.objects.filter(
            worker__workshop__company_id=pk,
            arrival_time__gte=start_date,
            arrival_time__lt=end_date
        )
        data = queryset.aggregate(
            total_orders=Count("id"),
            total_revenue=Sum("price"),
            avg_price=Avg("price")
        )
        return Response(data)

class WorkshopViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    queryset = Workshop.objects.all()
    serializer_class = WorkshopViewSerializer
    pagination_class = Pagination

    @action(detail=True, methods=['get'], url_path="orders")
    def workshop_order_list(self, request, pk=None):
        start_date, end_date = date_processing(request)
        queryset = Order.objects.filter(
            worker__workshop_id=pk,
            arrival_time__gte=start_date,
            arrival_time__lt=end_date
        ).select_related('worker', 'admin')
        filterset = OrderListFilter(request.GET, queryset=queryset)
        if filterset.is_valid():
            queryset = filterset.qs
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = OrderSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"], url_path="stats")
    def workshop_stats(self, request, pk=None):
        start_date, end_date = date_processing(request)
        queryset = Order.objects.filter(
            worker__workshop_id=pk,
            arrival_time__gte=start_date,
            arrival_time__lt=end_date
        )
        data = queryset.aggregate(
            total_orders=Count("id"),
            total_revenue=Sum("price"),
            avg_price=Avg("price")
        )
        return Response(data)

class WorkerViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    queryset = Worker.objects.all()
    serializer_class = WorkerViewSerializer
    pagination_class = Pagination
    @action(detail=True, methods=["get"], url_path="stats")
    def worker_stats(self, request, pk=None):
        start_date, end_date = date_processing(request)

        queryset = Order.objects.filter(
            worker_id=pk,
            arrival_time__gte=start_date,
            arrival_time__lt=end_date
        )
        data = queryset.aggregate(
            total_orders=Count("id"),
            total_revenue=Sum("price"),
            avg_price=Avg("price")
        )
        return Response(data)
