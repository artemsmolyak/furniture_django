from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Order, StatusCatalog, RequiredMaterial, Storage, DillerCatalog
from .forms import OrderForm, DillerForm
from django.forms.models import modelformset_factory, inlineformset_factory





def orders(request):

    ordersArray = []
    statusNameArray = []

    statuses = StatusCatalog.objects.all().order_by("orderliness")

    for stat in statuses:
        order = Order.objects.filter(status = stat.id)
        ordersArray.append( order )
        statusNameArray.append(stat.name)

    return render(request, "ordersAll.html", {"ordersArray" : ordersArray, "statusNameArray" : statusNameArray })






def order(request, good_id):

    obj = get_object_or_404(Order, id=good_id)
    form = OrderForm(instance=obj)

    RequiredMaterialFormset = inlineformset_factory(Order, RequiredMaterial, fields=('idMaterial', 'count',), can_delete=True, extra=1)

    if request.method == "POST":

        instance = get_object_or_404(Order, id=good_id)
        orderForm = OrderForm(request.POST, instance=instance)

        if orderForm.is_valid():

            obj = orderForm.save()

            formMaterials = RequiredMaterialFormset(request.POST, instance=obj)

            if formMaterials.is_valid():

                instance = RequiredMaterial.objects.filter(idOrder=obj)
                instance .delete()

                formMaterials.save(commit=False)

                for form in formMaterials:
                    if form['count'].value():
                        choice = form.save(commit=False)
                        choice.idOrder = obj
                        choice.save()


                return orders(request)

            return render(request, "order_create.html", {"objOrder": instance, "form": form, "formMaterials": formMaterials})


    else:

        formMaterials = RequiredMaterialFormset(instance=obj)

    return render(request, "order_create.html", {"form": form, "formMaterials" : formMaterials})





def order_create(request):

    RequiredMaterialFormset = inlineformset_factory(Order, RequiredMaterial, fields=('idMaterial', 'count',), can_delete=True, extra=1)


    if request.method == "POST":

        orderform = OrderForm(request.POST)

        formMaterials = RequiredMaterialFormset(request.POST)

        if orderform.is_valid():
            orderObj = orderform.save()

            if formMaterials.is_valid():
                formMaterials.save(commit=False)
                for form in formMaterials:

                    if form['count'].value():
                        choice = form.save(commit=False)
                        choice.idOrder = orderObj
                        choice.save()

                return orders(request)

        return render(request, "order_create.html", {"form": orderform, "formMaterials": formMaterials})



    form = OrderForm(None)

    formMaterials = RequiredMaterialFormset(queryset=RequiredMaterial.objects.none())

    return render(request, "order_create.html", {"form": form, "formMaterials" : formMaterials})






def store(request):

    materialsInStore = Storage.objects.all()


    return render(request, "store.html", {'materialsInStore' : materialsInStore})





def createRequestMaterials(request):

    Definitions = []

    for needMaterial in RequiredMaterial.objects.all().order_by('idMaterial'):
        for havematerial in  Storage.objects.all().order_by('idMaterial'):
            if needMaterial.idMaterial == havematerial.idMaterial:

                Definition = {}
                Definition["name"] = needMaterial.idMaterial.name
                Definition["needMaterial"] = needMaterial.count
                Definition["havematerial"] = havematerial.count
                diff = (needMaterial.count - havematerial.count)
                if diff < 0:
                    Definition["toOrder"] = 0
                else:
                    Definition["toOrder"] = needMaterial.count - havematerial.count

                Definitions.append(Definition)

    dillers = DillerCatalog.objects.all()

    return render(request, "materialsRequest.html", { "Definitions" : Definitions, 'dillers' : dillers })