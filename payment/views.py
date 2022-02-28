from django.shortcuts import render, get_object_or_404
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm
from pizza.models import Pizza
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse


# Create your views here.

@csrf_exempt
def payment_process(request):
    return render(request, "payment/process.html")

@csrf_exempt
def payment_done(request):
    return render(request, "payment/done.html")

@csrf_exempt
def payment_canceled(request):
    return render(request, "payment/canceled.html")
    

def payment_process(request):
    order_id = request.session.get('order_id')
    print(order_id)
    order = get_object_or_404(Pizza, id = order_id)
    host = request.get_host()

    paypal_dict = {
        'business' : settings.PAYPAL_RECIEVER_EMAIL,
        'amount' : order.price,
        'item_name' : "Pizza {}".format(order_id),
        'invoice' : str(order_id),
        'currency_code' : "USD",
        'notify_url' : 'http://{}{}'.format(host, reverse('paypal-ipn')),
        'return_url' : 'http://{}{}'.format(host, reverse('payment:done')),
        'cancel_return' : 'http://{}{}'.format(host, reverse('payment:canceled'))
    }
    print(paypal_dict)

    form = PayPalPaymentsForm(initial= paypal_dict)
    return render(request, 'payment/process.html', {'form': form, "order": order}) 