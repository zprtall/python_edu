from django.db import models
from pydantic.v1 import ValidationError


class Company(models.Model):
    name = models.CharField(max_length=50,
                            verbose_name="Название")
    legal_address = models.CharField(max_length=100,
                                    verbose_name="юр Адрес")
    UNP = models.CharField(max_length=9,
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
                               verbose_name="Адресс мастерской")
    capacity = models.IntegerField(verbose_name="Вмещаемость мастерской")
    parking_space = models.IntegerField(verbose_name="Количество места на стоянке")

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
    full_name = models.CharField(max_length=50,
                                verbose_name="ФИО")
    position = models.CharField(max_length=20,
                            choices=Position.choices,
                            verbose_name="Должность")
    hourly_rate = models.FloatField(null=True,
                                    blank=True,
                                    verbose_name="часовая ставка")
    phone = models.CharField(max_length=20,
                             verbose_name="номер телефона")

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
    type_work = models.CharField(max_length=200,
                                 verbose_name="Тип работы")
    worker_name = models.ForeignKey(Worker,
                                    on_delete=models.CASCADE,
                                    related_name="order_as_worker",
                                    verbose_name="Работник")
    admin_name = models.ForeignKey(Worker,
                                   on_delete=models.CASCADE,
                                   related_name="order_as_admin",
                                   verbose_name="Админ")
    receipt_time = models.DateTimeField(verbose_name="Время поступления авто")
    start_time = models.DateTimeField(verbose_name="Время начала работы")
    end_time = models.DateTimeField(verbose_name="Время окончания работ")
    time_of_delivery = models.DateTimeField(verbose_name="Время принятия работ")
    price = models.FloatField(verbose_name="Цена работ")
    car_number = models.CharField(max_length= 8,
                                  verbose_name="Номер авто")
    name_car = models.CharField(max_length=50,
                                verbose_name=" Марка и модель авто")
    comments = models.CharField(max_length=200,
                                blank=True,
                                verbose_name="Коментарии")

    def clean(self):
        if not self.worker_name.is_mechanic:
            raise ValidationError("Выполнителем работ может быть только механик")

        if not self.admin_name.is_admin:
            raise ValidationError("Проверяющим может быть только администратор")

            # время
        if self.receipt_time > self.start_time:
            raise ValidationError("Принятие авто не может быть позже начала работ")

        if self.start_time > self.end_time:
            raise ValidationError("Начало работ не может быть позже окончания")

        if self.end_time > self.time_of_delivery:
            raise ValidationError("Окончание работ не может быть позже сдачи авто")
