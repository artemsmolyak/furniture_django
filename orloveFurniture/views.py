from django.shortcuts import render
from django.http import HttpResponse

from orloveFurniture.models import OperationProjectCatalog
from .models import Order,  RequiredMaterial, Storage, DillerCatalog, RequiredOperationProject, RequiredOperationManufactory,RequiredOperationContractor
from .models import WorkerCatalog

from django.contrib.auth.decorators import login_required


import csv
from django.http import JsonResponse



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

#выполненная работа
def createReportCompletedApplication(request):

    if request.method == "POST":

        worker_id = request.POST['worker_id']

        worker_info = WorkerCatalog.objects.all().filter(id = worker_id)

       # date1 = request.POST['date1']

       # date2 = request.POST['date2']

        month = request.POST['month']

        year =  request.POST['year']


        reportProject = RequiredOperationProject.objects.all().filter(idWorker=worker_id).filter(isDoneDate__month = month).filter(isDoneDate__year = year)

        reportManufactory = RequiredOperationManufactory.objects.all().filter(idWorker=worker_id).filter(isDoneDate__month=month).filter(isDoneDate__year=year)

        reportContractor = RequiredOperationContractor.objects.all().filter(idWorker=worker_id).filter(isDoneDate__month=month).filter(isDoneDate__year=year)


        sum = 0
        for cost_ in reportProject:
            sum = sum + cost_.cost

        for cost_ in reportManufactory:
            sum = sum + cost_.cost

        for cost_ in reportContractor:
            sum = sum + cost_.cost


        return render(request, "report_completed_application.html", { "worker_info" : worker_info.first(),
                                                                      "period" : month,

                                                                      "reportProject" : reportProject,
                                                                      "reportManufactory": reportManufactory,
                                                                      "reportContractor": reportContractor,

                                                                      "sum" : sum } )


    workers = WorkerCatalog.objects.all()

    months =  {0:"January",
               1:"February",
               2:"March",
               3:"April",
               4:"May",
               5:"June",
               6:"July",
               7:"August",
               8:"September",
               9:"October",
               10:"November",
               11:"December" }


    years = {
        '2020'
    }

    return render(request, "report_application_choose_worker.html", {"workers" : workers, "months" : months, "years" : years} )


#невыполненная работа
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




def request_orders_in_work(request, worker_id):

    # список orders_id в которых есть заказы на конкретного worker
    orders_queryset = RequiredOperationProject.objects.filter(idWorker = worker_id).order_by('idOrder_id').distinct().values('idOrder_id')

    # Хотя бы однаоперация не выполнена
    order_array_ready = []
    order_array_to_work = []

    for val in orders_queryset:

        if val['isDone'] == True:
            order_array_ready.append(val['idOrder_id'])
        else:
            order_array_to_work.append(val['idOrder_id'])


    return JsonResponse(list(Order.objects.all().filter(id__in=order_array_to_work).values()), safe=False)


def request_orders_ready(request, worker_id):
    # список orders_id в которых есть заказы на конкретного worker
    orders_queryset = RequiredOperationProject.objects.filter(idWorker = worker_id).order_by('idOrder_id').distinct().values()


    #ТОЛЬКО полностью ВЫПОЛНЕННЫЕ
    order_array_ready = []
    order_array_to_work = []

    for val in orders_queryset:

        if val['isDone'] == True:
            order_array_ready.append(val['idOrder_id'])
        else:
            order_array_to_work.append(val['idOrder_id'])

    order_array_ready_set = set(order_array_ready)
    order_array_to_work_set = set(order_array_to_work)

    res_orders_id = order_array_ready_set.difference(order_array_to_work_set)

    return JsonResponse(list(Order.objects.all().filter(id__in=res_orders_id).values()), safe=False)



def request_order(request, order_id):

    #проверка, что дял этого заказа есть операции дял этого работника
    #orders_queryset = RequiredOperationProject.objects.filter(idOrder=order_id).filter(idWorker = worker_id).values()

    #if orders_queryset is None:
    #    return None
    # else:
    return JsonResponse(list(Order.objects.filter(id=order_id).values()), safe=False)



def request_operations(request, order_id, worker_id):
    return JsonResponse(list(RequiredOperationProject.objects.filter(idOrder=order_id).filter(idWorker=worker_id).values()), safe=False)




def request_dict_operations(request):
    return JsonResponse(list(OperationProjectCatalog.objects.all().values()), safe=False)



def request_auth(request, user_string, hash_string):
    return JsonResponse(list(WorkerCatalog.objects.all().filter(id = 1).values()), safe = False)
