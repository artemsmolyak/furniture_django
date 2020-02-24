from django.views.generic.edit import DeleteView
from .models import Order
from django.http import HttpResponse

from django.shortcuts import get_object_or_404

class OrderDelete(DeleteView):

    template_name = 'order_confirm_delete.html'
    model = Order
    success_url = "/index"
