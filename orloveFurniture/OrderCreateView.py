from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.views import View
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin

from django.forms import inlineformset_factory

from .forms import OrderForm, RequiredOperationProjectForm, RequiredOperationManufactoryForm, RequiredOperationContractorForm
from .models import Order, RequiredMaterial, RequiredOperationProject, RequiredOperationManufactory, RequiredOperationContractor

from django.shortcuts import redirect




class OrderCreateView(LoginRequiredMixin, View):

    requiredMaterialFormset = inlineformset_factory(Order, RequiredMaterial, fields=('idMaterial', 'count',), can_delete=True, extra=1)
    requiredOperationProjectFormset = inlineformset_factory(Order, RequiredOperationProject, RequiredOperationProjectForm, can_delete=True, extra=1)
    requiredOperationManufactoryFormset = inlineformset_factory(Order, RequiredOperationManufactory, RequiredOperationManufactoryForm, can_delete=True, extra=1)
    requiredOperationContractorFormset = inlineformset_factory(Order, RequiredOperationContractor, RequiredOperationContractorForm, can_delete=True, extra=1)


    def get(self, request, *args, **kwargs):

        form = OrderForm(None)

        formMaterials = self.requiredMaterialFormset(queryset=RequiredMaterial.objects.none())

        formProjectOperations = self.requiredOperationProjectFormset(queryset=RequiredOperationProject.objects.none())
        formManufactoryOperations = self.requiredOperationManufactoryFormset(queryset=RequiredOperationManufactory.objects.none())
        formContractorOperations = self.requiredOperationContractorFormset(queryset=RequiredOperationContractor.objects.none())

        return render(request, "order.html", {"form": form,
                                              "formMaterials": formMaterials,
                                              "formProjectOperations": formProjectOperations,
                                              "formManufactoryOperations": formManufactoryOperations,
                                              "formContractorOperations": formContractorOperations})




    def post(self, request, *args, **kwargs):

        orderform = OrderForm(request.POST)

        formMaterials = self.requiredMaterialFormset(request.POST)
        formProjectOperations = self.requiredOperationProjectFormset(request.POST)
        formManufactoryOperations = self.requiredOperationManufactoryFormset(request.POST)
        formContractorOperations = self.requiredOperationContractorFormset(request.POST)


        if orderform.is_valid() and formMaterials.is_valid() and formProjectOperations.is_valid() and formManufactoryOperations.is_valid() and formContractorOperations.is_valid():

            orderObj = orderform.save()

            # materials
            formMaterials.save(commit=False)
            for form in formMaterials:
                if form['count'].value():
                    choice = form.save(commit=False)
                    choice.idOrder = orderObj
                    choice.save()

            # project operation
            formProjectOperations.save(commit=False)
            for form in formProjectOperations:
                if form['cost'].value():
                    choice = form.save(commit=False)
                    choice.idOrder = orderObj
                    choice.save()

            # manufactory
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

            if request.POST.get("SaveBtn"):
                return redirect('/index')

            #если нажата обновить то перенаправляем уже как на открытие сохраненного заказа
            return redirect("/order/" + str(orderObj.id))



        return render(request, "order.html", {"form": orderform,
                                              "formMaterials": formMaterials,
                                              "formProjectOperations": formProjectOperations,
                                              "formManufactureOperations": formManufactoryOperations,
                                              "formContractorOperations": formContractorOperations})