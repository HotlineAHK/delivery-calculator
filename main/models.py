from django.core.validators import RegexValidator
from django.db import models

PHONE_VALIDATOR = RegexValidator(r'^\+?\d{10,15}$', 'Введите номер в формате +79991234567 (10-15 цифр).')


class Order(models.Model):
    DELIVERY_TYPES = [
        ('standard', 'Стандарт'),
        ('express', 'Экспресс'),
        ('same_day', 'День в день'),
    ]

    sender_name = models.CharField('ФИО отправителя', max_length=100)
    phone = models.CharField('Телефон', max_length=20, validators=[PHONE_VALIDATOR])
    city_from = models.CharField('Город отправки', max_length=100)
    city_to = models.CharField('Город получения', max_length=100)
    weight = models.DecimalField('Вес, кг', max_digits=6, decimal_places=2)
    delivery_type = models.CharField('Тип доставки', max_length=20, choices=DELIVERY_TYPES, default='standard')
    cost = models.DecimalField('Стоимость, руб.', max_digits=10, decimal_places=2)
    created_at = models.DateTimeField('Дата расчёта', auto_now_add=True)

    class Meta:
        ordering = ['-created_at', '-pk']

    def __str__(self):
        return f'{self.sender_name}: {self.city_from} → {self.city_to}'
