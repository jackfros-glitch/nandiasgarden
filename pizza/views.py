from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import PizzaForm, MultiplePizzaForm
from django.forms import formset_factory
from .models import Pizza

def home(request):
    return render(request, 'pizza/home.html')

def order(request):
    multiple_form = MultiplePizzaForm()
    if request.method == 'POST':
        created_pizza_pk = None
        filled_form = PizzaForm(request.POST)
        if filled_form.is_valid():
            created_pizza = filled_form.save()
            created_pizza_pk = created_pizza.id
            request.session['order_id'] = created_pizza.id
            print(request.session.get('order_id'))
            filled_form = PizzaForm()
        else:
            note = 'Order was not created, please try again'
            return render(request, 'pizza/order.html', {'multiple_form':multiple_form, 'pizzaform':filled_form, 'note': note})
        new_form = PizzaForm(initial={'price': 0.00})
        return redirect(reverse('payment:process'))
    else:
        form = PizzaForm(initial={'price': 0.00})
        return render(request, 'pizza/order.html', {'multiple_form':multiple_form, 'pizzaform':form})

def edit_order(request,pk):
    pizza = Pizza.objects.get(pk=pk)
    form = PizzaForm(instance=pizza)
    if request.method == 'POST':
        filled_form = PizzaForm(request.POST, instance=pizza)
        if filled_form.is_valid():
            filled_form.save()
            form = filled_form
            note = 'Your order has been processed.'
            return render(request, 'pizza/edit_order.html', {'pizzaform':form, 'pizza':pizza, 'note':note})
    return render(request, 'pizza/edit_order.html', {'pizzaform':form, 'pizza':pizza})


def pizzas(request):
    number_of_pizzas = 2
    filled_multiple_pizza_form = MultiplePizzaForm(request.GET)
    if filled_multiple_pizza_form.is_valid():
        number_of_pizzas = filled_multiple_pizza_form.cleaned_data['number']
    PizzaFormSet = formset_factory(PizzaForm, extra=number_of_pizzas)
    formset = PizzaFormSet()
    if request.method == "POST":
        filled_formset = PizzaFormSet(request.POST)
        if(filled_formset.is_valid()):
            for form in filled_formset:
                print(form.cleaned_data['topping1'])
            note = 'Pizzas have been ordered!'
        else:
            note = 'Order was not created, please try again'


        return render(request, 'pizza/pizzas.html', {'note':note, 'formset':formset})
    else:
        return render(request, 'pizza/pizzas.html', {'formset':formset})
