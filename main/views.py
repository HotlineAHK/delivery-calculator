from decimal import Decimal, ROUND_HALF_UP

from django.shortcuts import render

from .forms import DeliveryForm
from .models import Order

DELIVERY_MULTIPLIERS = {
    'standard': Decimal('1.0'),
    'express': Decimal('1.5'),
    'same_day': Decimal('2.0'),
}


def calculate_cost(weight, delivery_type):
    base = Decimal('300') + Decimal('30') * weight
    cost = base * DELIVERY_MULTIPLIERS[delivery_type]
    return cost.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def delivery_view(request):
    result = None
    form = DeliveryForm()

    if request.method == 'POST':
        form = DeliveryForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.cost = calculate_cost(order.weight, order.delivery_type)
            order.save()
            result = order
            form = DeliveryForm()

    last_orders = Order.objects.all()[:5]
    return render(request, 'demo/delivery.html', {'form': form, 'result': result, 'last_orders': last_orders})
