from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Order, StatusCatalog, RequiredMaterial, Storage, DillerCatalog, RequiredOperationProject, RequiredOperationManufactory,RequiredOperationContractor
from .models import WorkerCatalog
from .forms import RequiredOperationProjectForm, RequiredOperationManufactoryForm, RequiredOperationContractorForm
from .forms import OrderForm, DillerForm
from django.forms.models import inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
import csv



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