from django.shortcuts import get_object_or_404, redirect
from .validation_service import AdminButtonLogic
from django.contrib import messages
from .models import Order

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