from random import choices

from django.db import models
from django.core.exceptions import ValidationError
from phone_field import PhoneField
from django.core.validators import MaxValueValidator


class Company(models.Model):
    name = models.CharField(max_length=50,
                            verbose_name="Название")
    legal_address = models.CharField(max_length=100,
                                    verbose_name="юр Адрес")
    unp = models.CharField(max_length=9,
                           unique=True,
                           verbose_name="УНП")

    def __str__(self):
        return f"{self.name} {self.legal_address}"

class Workshop(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="workshops",
        verbose_name="Компания"

    )
    address = models.CharField(max_length=100,
                               verbose_name="Адрес мастерской")
    capacity = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(5)],
        verbose_name="Вмещаемость мастерской"
    )
    parking_space = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(60)],
        verbose_name="Количество места на стоянке"
    )
    occupied_workshop_spaces = models.SmallIntegerField(verbose_name="занятые места в мастерской")
    occupied_parking_spaces = models.SmallIntegerField(verbose_name="занятые места на парковке")

class Worker(models.Model):

    class Position(models.TextChoices):
        MECHANIC = "mechanic", "Автомеханик"
        ADMIN = "admin", "Админ"

    workshop =models.ForeignKey(
        Workshop,
        on_delete=models.CASCADE,
        related_name="workers",
        verbose_name="Мастерская"
    )
    first_name = models.CharField(max_length=50,
                                  verbose_name="Имя")
    last_name = models.CharField(max_length=50,
                            verbose_name="Фамилия")
    dad_name = models.CharField(max_length=50,
                                verbose_name="Отчество")
    position = models.CharField(max_length=8,
                            choices=Position.choices,
                            verbose_name="Должность")
    hourly_rate = models.FloatField(null=True,
                                    blank=True,
                                    verbose_name="часовая ставка")
    phone = PhoneField(verbose_name="номер телефона")

    @property
    def is_mechanic(self):
        return self.position == self.Position.MECHANIC

    @property
    def is_admin(self):
        return self.position == self.Position.ADMIN

    def clean(self):
        if self.position == self.Position.MECHANIC and not self.hourly_rate:
            raise ValidationError("У механика должна быть указана ставка")
        if self.position == self.Position.ADMIN and self.hourly_rate:
            raise ValidationError("Администратору ставка не нужна")
        if self.position == self.Position.ADMIN and self.hourly_rate:
            raise ValidationError("У администратора нет почасовой ставки")

class Order(models.Model):
    class TypeWork(models.TextChoices):
        WHEELS = "wheels", "колёса"
        PAINTWORK = "paintwork", "покраска"
        ENGINE = "engine", "двигатель"
        ELECTRICAL_SYSTEM = "electrical_system", "электросистема"
        SUSPENSION = "suspension", "подвеска"
        OTHER = "other", "прочее"
    class Spaces(models.TextChoices):
        PARKING = "parking", "стоянка"
        BOX = "box", "рабочее пространство"
        OWNER = "owner", "уехала к владельцу"
    type_work = models.CharField(max_length=18,
                                choices = TypeWork.choices,
                                verbose_name="Тип работы")
    worker = models.ForeignKey(Worker,
                                    on_delete=models.CASCADE,
                                    related_name="order_as_worker",
                                    verbose_name="Работник")
    admin = models.ForeignKey(Worker,
                                   on_delete=models.CASCADE,
                                   related_name="order_as_admin",
                                   verbose_name="Админ")
    arrival_time = models.DateTimeField(verbose_name="Время поступления авто")
    work_start_time = models.DateTimeField(verbose_name="Время начала работы", null=True)
    work_end_time = models.DateTimeField(verbose_name="Время окончания работ", null=True)
    delivery_acceptance_time = models.DateTimeField(verbose_name="Время принятия работ", null=True)
    price = models.FloatField(verbose_name="Цена работ")
    car_number = models.CharField(max_length= 8,
                                  verbose_name="Номер авто")
    car_name = models.CharField(max_length=50,
                                verbose_name=" Марка и модель авто")
    comments = models.CharField(max_length=200,
                                blank=True,
                                verbose_name="Коментарии")
    finding = models.CharField(max_length=20,
                               choices = Spaces.choices,
                               verbose_name="Местонахождение")

    def save(self, *args, **kwargs):
        workshop = self.worker.workshop
        if self.pk:
            old = Order.objects.get(pk=self.pk)
            old_finding = old.finding
        else:
            old_finding = None
        if self.delivery_acceptance_time is not None:
            new_finding = self.Spaces.OWNER
        elif self.work_start_time is None:
            new_finding = self.Spaces.PARKING
        elif self.work_end_time is None:
            new_finding = self.Spaces.BOX
        else:
            new_finding = self.Spaces.PARKING
        self.finding = new_finding

        if old_finding == self.Spaces.BOX:
            workshop.occupied_workshop_spaces -= 1
        elif old_finding == self.Spaces.PARKING:
            workshop.occupied_parking_spaces -= 1

        if new_finding == self.Spaces.BOX:
            workshop.occupied_workshop_spaces += 1
        elif new_finding == self.Spaces.PARKING:
            workshop.occupied_parking_spaces += 1

        workshop.occupied_workshop_spaces = max(0, workshop.occupied_workshop_spaces)
        workshop.occupied_parking_spaces = max(0, workshop.occupied_parking_spaces)

        self.full_clean()
        super().save(*args, **kwargs)

    def clean(self):
        workshop = self.worker.workshop
        if self.worker and not self.worker.is_mechanic:
            raise ValidationError("Выполнителем работ может быть только механик")
        if self.admin and not self.admin.is_admin:
            raise ValidationError("Проверяющим может быть только администратор")
        if self.work_start_time and self.arrival_time > self.work_start_time:
            raise ValidationError("Начало работ не может быть раньше поступления авто")
        if self.work_start_time and self.work_end_time:
            if self.work_start_time > self.work_end_time:
                raise ValidationError("Окончание не может быть раньше начала")
        if self.work_end_time and self.delivery_acceptance_time:
            if self.work_end_time > self.delivery_acceptance_time:
                raise ValidationError("Сдача не может быть раньше окончания работ")
        if self.work_end_time and not self.work_start_time:
            raise ValidationError("Нельзя закончить работу, не начав её")
        if self.delivery_acceptance_time and (
                not self.work_start_time or not self.work_end_time
        ):
            raise ValidationError("Сдача невозможна без начала и окончания работ")
        if self.type_work.lower() == self.TypeWork.OTHER and not self.comments:
            raise ValidationError("Для типа 'Прочее' необходимо указать комментарий")
        if workshop.occupied_workshop_spaces > workshop.capacity:
            raise ValidationError("В мастерской нет места")
        if workshop.occupied_parking_spaces > workshop.parking_space:
            raise ValidationError("На парковске нет места")



