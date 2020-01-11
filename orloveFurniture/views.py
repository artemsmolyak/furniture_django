from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Order, StatusCatalog, RequiredMaterial
from .forms import OrderForm, RequiredMaterialForm
from django.forms.models import modelformset_factory



def orders(request):

    ordersArray = []
    statusNameArray = []

    statuses = StatusCatalog.objects.all()

    for stat in statuses:
        order = Order.objects.filter(status = stat.id)
        ordersArray.append( order )
        statusNameArray.append(stat.name)

    return render(request, "ordersAll.html", {"ordersArray" : ordersArray, "statusNameArray" : statusNameArray })






def order(request, good_id):

    if request.method == "POST":



        orderForm = OrderForm(request.POST or None)

        if orderForm.is_valid():
            orderForm.save()



        ordersArray = []
        statusNameArray = []

        statuses = StatusCatalog.objects.all()

        for stat in statuses:
            order = Order.objects.filter(status=stat.id)
            ordersArray.append(order)
            statusNameArray.append(stat.name)

        return render(request, "ordersAll.html", {"ordersArray": ordersArray, "statusNameArray": statusNameArray})

    else:

        obj = get_object_or_404(Order, id=good_id)
        form = OrderForm(instance=obj)

        RequiredMaterialFormset = modelformset_factory(RequiredMaterial, form=RequiredMaterialForm, extra=1)
        formMaterials = RequiredMaterialFormset(queryset=RequiredMaterial.objects.filter(idOrder=good_id))

    return render(request, "order_create.html", {"form": form, "formMaterials" : formMaterials})





def order_create(request):

    form = OrderForm(request.POST or None )

    formMaterials = RequiredMaterialForm(request.POST or None)



    if request.method == "POST":

        if form.is_valid():
            form.save()

            ordersArray = []
            statusNameArray = []

            statuses = StatusCatalog.objects.all()

            for stat in statuses:
                order = Order.objects.filter(status=stat.id)
                ordersArray.append(order)
                statusNameArray.append(stat.name)

            return render(request, "ordersAll.html", {"ordersArray": ordersArray, "statusNameArray": statusNameArray})
        else:
            return HttpResponse("error")

    return render(request, "order_create.html", {"form": form, "formMaterials" : formMaterials})




def order_edit(request, good_id):
    obj = get_object_or_404(Order, id=good_id)

    form = OrderForm(request.POST or None, instance=obj)
    context = {'form': form}

    if form.is_valid():
        obj = form.save(commit=False)

        obj.save()

        context = {'form': form}

        return HttpResponse("Updated")

    else:
        return HttpResponse("NOT Updated")