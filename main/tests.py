from decimal import Decimal

from django.test import TestCase

from .models import Order
from .views import calculate_cost


class CalculateCostTests(TestCase):
    def test_standard(self):
        self.assertEqual(calculate_cost(Decimal('10'), 'standard'), Decimal('600.00'))

    def test_express(self):
        self.assertEqual(calculate_cost(Decimal('10'), 'express'), Decimal('900.00'))

    def test_same_day(self):
        self.assertEqual(calculate_cost(Decimal('10'), 'same_day'), Decimal('1200.00'))


class DeliveryViewTests(TestCase):
    def valid_data(self, **overrides):
        data = {
            'sender_name': 'Иванов Иван Иванович',
            'phone': '+79991234567',
            'city_from': 'Москва',
            'city_to': 'Казань',
            'weight': '10',
            'delivery_type': 'standard',
            'agree': 'on',
        }
        data.update(overrides)
        return data

    def test_page_opens(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Калькулятор доставки')

    def test_valid_post_creates_order_and_shows_cost(self):
        response = self.client.post('/', self.valid_data())
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.get().cost, Decimal('600.00'))
        self.assertContains(response, 'Итоговая стоимость')

    def test_weight_out_of_range(self):
        response = self.client.post('/', self.valid_data(weight='150'))
        self.assertEqual(Order.objects.count(), 0)
        self.assertContains(response, 'от 0.1 до 100')

    def test_same_cities(self):
        response = self.client.post('/', self.valid_data(city_to='Москва'))
        self.assertEqual(Order.objects.count(), 0)
        self.assertContains(response, 'совпадают')

    def test_express_too_heavy(self):
        response = self.client.post('/', self.valid_data(weight='25', delivery_type='express'))
        self.assertEqual(Order.objects.count(), 0)
        self.assertContains(response, '20 кг')

    def test_agreement_required(self):
        data = self.valid_data()
        del data['agree']
        response = self.client.post('/', data)
        self.assertEqual(Order.objects.count(), 0)

    def test_entered_data_kept_after_error(self):
        response = self.client.post('/', self.valid_data(weight='150'))
        self.assertContains(response, 'value="Иванов Иван Иванович"')

    def test_history_shows_last_five(self):
        for i in range(7):
            self.client.post('/', self.valid_data(city_to=f'Город{i}'))
        response = self.client.get('/')
        self.assertEqual(Order.objects.count(), 7)
        self.assertContains(response, 'Город6')
        self.assertNotContains(response, 'Город0')
