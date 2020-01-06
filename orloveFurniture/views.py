from django.shortcuts import render
from django.http import HttpResponse
from orloveFurniture.models import Order
from .forms import OrderForm

def orders(request):
    orders = Order.objects.all()
    return render(request, "ordersAll.html", {"orders" : orders})



def order(request, good_id):
    order = Order.objects.get(pk = good_id)
    return render(request, "order.html", {"order": order})




def order_create(request):
    return render(request, "order_create.html", {})




def order_create_(request):
    if request.method == "POST":
        return HttpResponse("Thanks")

    form = OrderForm()
    return render(request, "order_create_.html", {'form' : form})