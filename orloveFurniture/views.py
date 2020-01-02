from django.shortcuts import render
from django.http import HttpResponse
from orloveFurniture.models import Order

# Create your views here.

def orders(request):
    orders = Order.objects.all()
    return render(request, "ordersAll_ex.html", {"orders" : orders})



def order(request, good_id):
    order = Order.objects.get(pk = good_id)
    return render(request, "order_ex.html", {"order": order})




def order_create(request):
    return render(request, "order_create.html", {})