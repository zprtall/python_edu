from django.core.exceptions import ValidationError
from django.utils import timezone

class WorkerValidations:
    @staticmethod
    def valid_worker_clean(worker):
        if worker.position == worker.Position.MECHANIC and not worker.hourly_rate:
            raise ValidationError("У механика должна быть указана ставка")
        if worker.position == worker.Position.ADMIN and worker.hourly_rate:
            raise ValidationError("У администратора нет почасовой ставки")

class OrderValidations:
    @staticmethod
    def valid_order_clean(order,workshop):
        if order.worker and not order.worker.is_mechanic:
            raise ValidationError("Выполнителем работ может быть только механик")
        if order.admin and not order.admin.is_admin:
            raise ValidationError("Проверяющим может быть только администратор")
        if order.type_work.lower() == order.TypeWork.OTHER and not order.comments:
            raise ValidationError("Для типа 'Прочее' необходимо указать комментарий")

        if workshop.occupied_workshop_spaces > workshop.capacity:
            raise ValidationError("В мастерской нет места")
        if workshop.occupied_parking_spaces > workshop.parking_space:
            raise ValidationError("На парковке нет места")


class AdminButtonLogic:
    @staticmethod
    def order_change_status_logic(order,workshop):
        if not order.work_start_time:
            order.work_start_time = timezone.now()
            order.finding = order.Spaces.BOX
            workshop.occupied_parking_spaces -= 1
            workshop.occupied_workshop_spaces += 1
        elif not order.work_end_time and order.work_start_time:
            order.work_end_time = timezone.now()
            order.finding = order.Spaces.PARKING
            workshop.occupied_workshop_spaces -= 1
            workshop.occupied_parking_spaces += 1
        elif not order.delivery_acceptance_time and order.work_end_time and order.work_start_time:
            order.delivery_acceptance_time = timezone.now()
            order.finding = order.Spaces.OWNER
            workshop.occupied_parking_spaces -= 1





