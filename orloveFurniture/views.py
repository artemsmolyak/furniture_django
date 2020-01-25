from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Order, StatusCatalog, RequiredMaterial, Storage, DillerCatalog, RequiredOperation
from .forms import OrderForm, DillerForm
from django.forms.models import modelformset_factory, inlineformset_factory
from django.contrib.auth.decorators import login_required



@login_required
def orders(request):

    ordersArray = []
    statusNameArray = []

    statuses = StatusCatalog.objects.all().order_by("orderliness")

    for stat in statuses:
        order = Order.objects.filter(status = stat.id)
        ordersArray.append( order )
        statusNameArray.append(stat.name)

    return render(request, "ordersAll.html", {"ordersArray" : ordersArray, "statusNameArray" : statusNameArray })





@login_required
def order(request, good_id):

    obj = get_object_or_404(Order, id=good_id)
    form = OrderForm(instance=obj)

    RequiredMaterialFormset = inlineformset_factory(Order, RequiredMaterial, fields=('idMaterial', 'count',), can_delete=True, extra=1)

    RequiredOperationFormset = inlineformset_factory(Order, RequiredOperation, fields=('idOrder', 'idOperation', 'idWorker', 'cost',), can_delete=True, extra=1)

    if request.method == "POST":

        instance = get_object_or_404(Order, id=good_id)
        orderForm = OrderForm(request.POST, instance=instance)

        formMaterials = RequiredMaterialFormset(request.POST, instance=obj)
        formOperations = RequiredOperationFormset(request.POST, instance=obj)

        if orderForm.is_valid() and formMaterials.is_valid() and formOperations.is_valid():

            obj = orderForm.save()

            instance = RequiredMaterial.objects.filter(idOrder=obj)
            instance.delete()

            formMaterials.save(commit=False)

            for form in formMaterials:
                if form['count'].value():
                    choice = form.save(commit=False)
                    choice.idOrder = obj
                    choice.save()


            #instance = RequiredOperation.objects.filter(idOrder=obj)
            #instance.delete()

            formOperations.save(commit=False)

            for form in formOperations.deleted_objects:
                form.delete()

            for form in formOperations:
                if form['cost'].value() != 0 and form['cost'].value():
                    choice = form.save(commit=False)
                    choice.idOrder = obj
                    choice.save()

            return orders(request)

        return render(request, "order_create.html", {"objOrder": instance, "form": form, "formMaterials": formMaterials, "formOperations" : formOperations})


    else:

        formMaterials = RequiredMaterialFormset(instance=obj)

        formOperations = RequiredOperationFormset(instance=obj)


    # objOrder для номера заказа
    return render(request, "order_create.html", { "objOrder" : obj, "form": form, "formMaterials" : formMaterials, "formOperations" : formOperations})




@login_required
def order_create(request):

    RequiredMaterialFormset = inlineformset_factory(Order, RequiredMaterial, fields=('idMaterial', 'count',), can_delete=True, extra=1)

    RequiredOperationFormset = inlineformset_factory(Order, RequiredOperation, fields=('idOrder', 'idOperation', 'idWorker', 'cost',), can_delete=True, extra=1)


    if request.method == "POST":

        orderform = OrderForm(request.POST)

        formMaterials = RequiredMaterialFormset(request.POST)

        formOperations = RequiredOperationFormset(request.POST)

        if orderform.is_valid() and formMaterials.is_valid() and  formOperations.is_valid():

            orderObj = orderform.save()


            formMaterials.save(commit=False)
            for form in formMaterials:
                if form['count'].value():
                    choice = form.save(commit=False)
                    choice.idOrder = orderObj
                    choice.save()

            formOperations.save(commit=False)
            for form in formOperations:
                if form['cost'].value():
                    choice = form.save(commit=False)
                    choice.idOrder = orderObj
                    choice.save()

            return orders(request)


        return render(request, "order_create.html", {"form": orderform, "formMaterials": formMaterials, "formOperations" : formOperations})



    form = OrderForm(None)

    formMaterials = RequiredMaterialFormset(queryset=RequiredMaterial.objects.none())

    formOperations = RequiredOperationFormset(queryset=RequiredOperation.objects.none())

    return render(request, "order_create.html", {"form": form, "formMaterials" : formMaterials, "formOperations" : formOperations})





@login_required
def store(request):

    materialsInStore = Storage.objects.all()


    return render(request, "store.html", {'materialsInStore' : materialsInStore})




@login_required
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