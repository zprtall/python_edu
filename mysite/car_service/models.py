from django.db import models
from phone_field import PhoneField
from django.core.validators import MaxValueValidator
from .validation_service import WorkerValidations, OrderValidations


class Company(models.Model):
    name = models.CharField(max_length=50,
                            verbose_name="Название")
    legal_address = models.CharField(max_length=100,
                                    verbose_name="юр Адрес")
    unp = models.CharField(max_length=9,
                           unique=True,
                           verbose_name="УНП")
    def __str__(self):
        return f"{self.name}: {self.legal_address}"

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
    occupied_workshop_spaces = models.PositiveSmallIntegerField(default= 0,verbose_name="занятые места в мастерской")
    occupied_parking_spaces = models.PositiveSmallIntegerField(verbose_name="занятые места на парковке")

    def __str__(self):
        return f"Мастерская {self.company}: {self.address}"

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
        WorkerValidations.valid_worker_clean(self)

    def __str__(self):
        return f"{self.get_position_display()} {self.first_name} {self.last_name}"

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
    arrival_time = models.DateTimeField(verbose_name="Время поступления авто", )
    work_start_time = models.DateTimeField(default= None, verbose_name="Время начала работы", null=True, blank=True)
    work_end_time = models.DateTimeField(default= None,verbose_name="Время окончания работ", null=True, blank=True)
    delivery_acceptance_time = models.DateTimeField(default= None,verbose_name="Время принятия работ", null=True, blank=True)
    price = models.FloatField(verbose_name="Цена работ")
    car_number = models.CharField(max_length= 8,
                                  verbose_name="Номер авто")
    car_name = models.CharField(max_length=50,
                                verbose_name=" Марка и модель авто")
    comments = models.CharField(max_length=200,
                                blank=True,
                                verbose_name="Коментарии")
    finding = models.CharField(default=Spaces.PARKING,
                                max_length=20,
                               choices = Spaces.choices,
                               verbose_name="Местонахождение")

    def save(self, *args, **kwargs):
        workshop = self.worker.workshop
        if not self.pk:
            workshop.occupied_parking_spaces += 1
        self.full_clean()
        super().save(*args, **kwargs)
        workshop.save()

    def clean(self):
        workshop = self.worker.workshop
        OrderValidations.valid_order_clean(self,workshop)




