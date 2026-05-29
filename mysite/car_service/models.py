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

class Order(models.Model):
    class TypeWork(models.TextChoices):
        WHEELS = "wheels", "колёса"
        PAINTWORK = "paintwork", "покраска"
        ENGINE = "engine", "двигатель"
        ELECTRICAL_SYSTEM = "electrical_system", "электросистема"
        SUSPENSION = "suspension", "подвеска"
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
    work_start_time = models.DateTimeField(verbose_name="Время начала работы")
    work_end_time = models.DateTimeField(verbose_name="Время окончания работ")
    delivery_acceptance_time = models.DateTimeField(verbose_name="Время принятия работ")
    price = models.FloatField(verbose_name="Цена работ")
    car_number = models.CharField(max_length= 8,
                                  verbose_name="Номер авто")
    car_name = models.CharField(max_length=50,
                                verbose_name=" Марка и модель авто")
    comments = models.CharField(max_length=200,
                                blank=True,
                                verbose_name="Коментарии")

    def clean(self):
        if not self.worker.is_mechanic:
            raise ValidationError("Выполнителем работ может быть только механик")
        if not self.admin.is_admin:
            raise ValidationError("Проверяющим может быть только администратор")
        if self.arrival_time > self.work_start_time:
            raise ValidationError("Принятие авто не может быть позже начала работ")
        if self.work_start_time > self.work_end_time:
            raise ValidationError("Начало работ не может быть позже окончания")
        if self.work_end_time > self.delivery_acceptance_time:
            raise ValidationError("Окончание работ не может быть позже сдачи авто")
