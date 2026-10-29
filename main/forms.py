from decimal import Decimal

from django import forms
from django.core.exceptions import ValidationError

from .models import Order

MIN_WEIGHT = Decimal('0.1')
MAX_WEIGHT = Decimal('100')
MAX_EXPRESS_WEIGHT = Decimal('20')


class DeliveryForm(forms.ModelForm):
    agree = forms.BooleanField(label='Согласен с условиями доставки')

    class Meta:
        model = Order
        fields = ['sender_name', 'phone', 'city_from', 'city_to', 'weight', 'delivery_type']

    def clean_weight(self):
        weight = self.cleaned_data.get('weight')
        if weight is not None and not MIN_WEIGHT <= weight <= MAX_WEIGHT:
            raise ValidationError(f'Вес должен быть от {MIN_WEIGHT} до {MAX_WEIGHT} кг.')
        return weight

    def clean(self):
        cleaned_data = super().clean()
        weight = cleaned_data.get('weight')
        delivery_type = cleaned_data.get('delivery_type')
        city_from = cleaned_data.get('city_from')
        city_to = cleaned_data.get('city_to')

        if city_from and city_to and city_from.strip().lower() == city_to.strip().lower():
            self.add_error('city_to', 'Город отправки и город получения совпадают.')
        if delivery_type == 'express' and weight is not None and weight > MAX_EXPRESS_WEIGHT:
            self.add_error('weight', 'Для экспресс-доставки вес не может превышать 20 кг.')
        return cleaned_data
