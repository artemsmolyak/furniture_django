from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import Order, StatusCatalog


class AllOrdersShow(LoginRequiredMixin, TemplateView):

    template_name = "ordersAll.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        ordersArray = []
        statusNameArray = []

        statuses = StatusCatalog.objects.all().order_by("orderliness")
        for stat in statuses:
            order = Order.objects.filter(status=stat.id)
            ordersArray.append(order)
            statusNameArray.append(stat.name)


        context["ordersArray"] = ordersArray
        context["statusNameArray"] = statusNameArray

        return context


