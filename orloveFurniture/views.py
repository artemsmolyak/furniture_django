from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Order, StatusCatalog, RequiredMaterial, Storage, DillerCatalog, RequiredOperationProject, RequiredOperationManufactory,RequiredOperationContractor
from .models import WorkerCatalog
from .forms import RequiredOperationProjectForm, RequiredOperationManufactoryForm, RequiredOperationContractorForm
from .forms import OrderForm, DillerForm
from django.forms.models import inlineformset_factory
from django.contrib.auth.decorators import login_required
import csv



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


    RequiredOperationProjectFormset = inlineformset_factory(Order, RequiredOperationProject, RequiredOperationProjectForm, can_delete=True, extra=1)
    RequiredOperationManufactoryFormset = inlineformset_factory(Order, RequiredOperationManufactory, RequiredOperationManufactoryForm, can_delete=True, extra=1)
    RequiredOperationContractorFormset = inlineformset_factory(Order, RequiredOperationContractor,  RequiredOperationContractorForm, can_delete=True, extra=1)


    if request.method == "POST":

        instance = get_object_or_404(Order, id=good_id)
        orderForm = OrderForm(request.POST, instance=instance)

        formMaterials = RequiredMaterialFormset(request.POST, instance=obj)

        formProjectOperations = RequiredOperationProjectFormset(request.POST, instance=obj)
        formManufactoryOperations = RequiredOperationManufactoryFormset(request.POST, instance=obj)
        formContractorOperations = RequiredOperationContractorFormset(request.POST, instance=obj)

        if orderForm.is_valid() and formMaterials.is_valid() and formProjectOperations.is_valid() and formManufactoryOperations.is_valid() and formContractorOperations.is_valid():

            obj = orderForm.save()

            instance = RequiredMaterial.objects.filter(idOrder=obj)
            instance.delete()



            #materials
            formMaterials.save(commit=False)

            for form in formMaterials:
                if form['count'].value():
                    choice = form.save(commit=False)
                    choice.idOrder = obj
                    choice.save()


            #project operation
            instance = RequiredOperationProject.objects.filter(idOrder=obj)
            instance.delete()

            formProjectOperations.save(commit=False)

            for form in formProjectOperations.deleted_objects:
                form.delete()

            for form in formProjectOperations:
                if form['cost'].value() != 0 and form['cost'].value():
                    choice = form.save(commit=False)
                    choice.idOrder = obj
                    choice.save()


            # manufactory operation
            instance = RequiredOperationManufactory.objects.filter(idOrder=obj)
            instance.delete()

            formManufactoryOperations.save(commit=False)

            for form in formManufactoryOperations.deleted_objects:
                form.delete()

            for form in formManufactoryOperations:
                if form['cost'].value() != 0 and form['cost'].value():
                    choice = form.save(commit=False)
                    choice.idOrder = obj
                    choice.save()


            # constractor operation
            instance = RequiredOperationContractor.objects.filter(idOrder=obj)
            instance.delete()

            formContractorOperations.save(commit=False)

            for form in formContractorOperations.deleted_objects:
                form.delete()

            for form in formContractorOperations:
                if form['cost'].value() != 0 and form['cost'].value():
                    choice = form.save(commit=False)
                    choice.idOrder = obj
                    choice.save()

            return orders(request)

        return render(request, "order_create.html", {"objOrder": instance, "form": form,
                                                     "formMaterials": formMaterials,
                                                     "formProjectOperations" : formProjectOperations,
                                                     "formManufactoryOperations" : formManufactoryOperations,
                                                     "formContractorOperations" : formContractorOperations
                                                     })


    else:

        formMaterials = RequiredMaterialFormset(instance=obj)

        #formOperations = RequiredOperationFormset(instance=obj)

        formProjectOperations = RequiredOperationProjectFormset(instance=obj)
        formManufactoryOperations = RequiredOperationManufactoryFormset(instance=obj)
        formContractorOperations = RequiredOperationContractorFormset(instance=obj)



        forms = RequiredOperationProject.objects.all().filter(idOrder=good_id).filter(isDone=True)
        sumProjectOperation = 0
        for form_ in forms:
            sumProjectOperation = sumProjectOperation + form_.cost



        forms = RequiredOperationManufactory.objects.all().filter(idOrder=good_id).filter(isDone=True)
        sumManufactoryOperation = 0
        for form_ in forms:
            sumManufactoryOperation = sumManufactoryOperation + form_.cost




        forms = RequiredOperationContractor.objects.all().filter(idOrder=good_id).filter(isDone=True)
        sumContractorOperation = 0
        for form_ in forms:
            sumContractorOperation = sumContractorOperation + form_.cost


    # objOrder для номера заказа
    return render(request, "order_create.html", { "objOrder" : obj,
                                                  "form": form,

                                                  "formMaterials" : formMaterials,
                                                  "formProjectOperations" : formProjectOperations,
                                                  "formManufactoryOperations" : formManufactoryOperations,
                                                  "formContractorOperations" : formContractorOperations,

                                                  "sumProjectOperation": sumProjectOperation,
                                                  "sumManufactoryOperation": sumManufactoryOperation,
                                                  "sumContractorOperation": sumContractorOperation,
                                                  "sumTotal": sumProjectOperation + sumManufactoryOperation + sumContractorOperation
                                                  })




@login_required
def order_create(request):

    RequiredMaterialFormset = inlineformset_factory(Order, RequiredMaterial, fields=('idMaterial', 'count',), can_delete=True, extra=1)

    RequiredOperationProjectFormset = inlineformset_factory(Order, RequiredOperationProject,  RequiredOperationProjectForm,  can_delete=True, extra=1)
    RequiredOperationManufactoryFormset = inlineformset_factory(Order,  RequiredOperationManufactory, RequiredOperationManufactoryForm, can_delete=True, extra=1)
    RequiredOperationContractorFormset = inlineformset_factory(Order, RequiredOperationContractor, RequiredOperationContractorForm, can_delete=True, extra=1)

    if request.method == "POST":

        orderform = OrderForm(request.POST)

        formMaterials = RequiredMaterialFormset(request.POST)

        formProjectOperations = RequiredOperationProjectFormset(request.POST)
        formManufactoryOperations = RequiredOperationManufactoryFormset(request.POST)
        formContractorOperations = RequiredOperationContractorFormset(request.POST)

        if orderform.is_valid() and formMaterials.is_valid() and  formProjectOperations.is_valid() and  formManufactoryOperations.is_valid() and  formContractorOperations.is_valid():

            orderObj = orderform.save()

            #materials
            formMaterials.save(commit=False)
            for form in formMaterials:
                if form['count'].value():
                    choice = form.save(commit=False)
                    choice.idOrder = orderObj
                    choice.save()

            #project operation
            formProjectOperations.save(commit=False)
            for form in formProjectOperations:
                if form['cost'].value():
                    choice = form.save(commit=False)
                    choice.idOrder = orderObj
                    choice.save()

            #manufactory
            formManufactoryOperations.save(commit=False)
            for form in formManufactoryOperations:
                if form['cost'].value():
                    choice = form.save(commit=False)
                    choice.idOrder = orderObj
                    choice.save()

            # contractor
            formContractorOperations.save(commit=False)
            for form in formContractorOperations:
                if form['cost'].value():
                    choice = form.save(commit=False)
                    choice.idOrder = orderObj
                    choice.save()

            return orders(request)


        return render(request, "order_create.html", {"form": orderform,
                                                     "formMaterials": formMaterials,
                                                     "formProjectOperations" : formProjectOperations,
                                                     "formManufactureOperations": formManufactoryOperations,
                                                     "formContractorOperations" : formContractorOperations})



    form = OrderForm(None)

    formMaterials = RequiredMaterialFormset(queryset=RequiredMaterial.objects.none())


    formProjectOperations = RequiredOperationProjectFormset(queryset=RequiredOperationProject.objects.none())
    formManufactoryOperations = RequiredOperationManufactoryFormset(queryset=RequiredOperationManufactory.objects.none())
    formContractorOperations = RequiredOperationContractorFormset(queryset=RequiredOperationContractor.objects.none())

    return render(request, "order_create.html", {"form": form,
                                                 "formMaterials" : formMaterials,
                                                 "formProjectOperations" : formProjectOperations,
                                                 "formManufactoryOperations" : formManufactoryOperations,
                                                 "formContractorOperations" : formContractorOperations})





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




################      REPORTS

def createReportCompletedApplication(request):

    if request.method == "POST":

        worker_id = request.POST['worker_id']

        worker_info = WorkerCatalog.objects.all().filter(id = worker_id)

       # date1 = request.POST['date1']

       # date2 = request.POST['date2']

        month = request.POST['month']

        report = RequiredOperationProject.objects.all().filter(idWorker=worker_id).filter(isDoneDate__month = month)

        sum = 0
        for cost_ in report:
            sum = sum + cost_.cost


        return render(request, "report_completed_application.html", { "worker_info" : worker_info.first(),
                                                                      "period" : month,
                                                                      "report" : report, "sum" : sum } )



    workers = WorkerCatalog.objects.all()

    months =  {"January":0, "February":1, "March":2, "April":3, "May":4, "June":5, "July":6, "August":7, "September":8, "October":9, "November":10, "December":11 }
    # {
    #      1 : 'January',
    #      2 : 'February',
    #      3 : 'March',
    #      4 : 'April',
    #      5 : 'May',
    #      6 : 'June',
    #      7 : 'July',
    #      8 : 'August',
    #     9 : 'September',
    #     10 : 'October',
    #     11 : 'November',
    #     12 : 'December'
    # }

    years = {
        '2019',
        '2020'
    }

    return render(request, "report_application_choose_worker.html", {"workers" : workers, "months" : months, "years" : years} )



def createReportOutstandingApplication(request):

    if request.method == "POST":
        return HttpResponse("в разработке")




    Operations = []
    for needOperation in RequiredOperationProject.objects.all().filter(isDone=False).order_by('idWorker'):
        Operation = {}
        Operation["workerName"] = needOperation.idWorker
        Operation["order"] = needOperation.idOrder
        Operation["operation"] = needOperation.idOperation

        Operations.append(Operation)


    workers =  WorkerCatalog.objects.all()

    return render(request, "report_outstanding_applications.html", {"workers" : workers, "Operations" : Operations})



def xls(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

    writer = csv.writer(response)

    period = request.POST['period']
    worker_info = request.POST['worker_info']
    sum =  request.POST['sum']

    writer.writerow([])
    writer.writerow(['ФИО',worker_info])
    writer.writerow(['месяц',period ])
    writer.writerow([])


    #table
    writer.writerow(['Договор','Операция', 'Дата выполнения', 'Стоимость' ])

    count = request.POST['count_']
    for val in range(0, int(count)):
        idOrder = request.POST['idOrder' + str(val)]
        idOperation = request.POST['idOperation'+ str(val)]
        isDoneDate = request.POST['isDoneDate'+ str(val)]
        cost = request.POST['cost'+ str(val)]
        writer.writerow([idOrder, idOperation, isDoneDate, cost])

    writer.writerow([])
    writer.writerow(['', '', 'итоговая сумма', sum])

    return response