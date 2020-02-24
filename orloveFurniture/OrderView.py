from django.views import View
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin

from django.forms import inlineformset_factory

from .forms import OrderForm, RequiredOperationProjectForm, RequiredOperationManufactoryForm, RequiredOperationContractorForm
from .models import Order, RequiredMaterial, RequiredOperationProject, RequiredOperationManufactory, RequiredOperationContractor

from django.shortcuts import redirect



class OrderView(LoginRequiredMixin, View):

    requiredMaterialFormset = inlineformset_factory(Order, RequiredMaterial, fields=('idMaterial', 'count',), can_delete=True, extra=1)
    requiredOperationProjectFormset = inlineformset_factory(Order, RequiredOperationProject, RequiredOperationProjectForm, can_delete=True, extra=1)
    requiredOperationManufactoryFormset = inlineformset_factory(Order, RequiredOperationManufactory, RequiredOperationManufactoryForm, can_delete=True, extra=1)
    requiredOperationContractorFormset = inlineformset_factory(Order, RequiredOperationContractor, RequiredOperationContractorForm, can_delete=True, extra=1)

    def get(self, request, *args, **kwargs):

        order_id = self.kwargs['order_id']

        obj = get_object_or_404(Order, id=order_id)
        form = OrderForm(instance=obj)

        #Форма требуемых материалов
        formMaterials = self.requiredMaterialFormset(instance=obj)

        #Форма Операций - Проект
        formProjectOperations = self.requiredOperationProjectFormset(instance=obj)

        #Форма Операций - Цех
        formManufactoryOperations = self.requiredOperationManufactoryFormset(instance=obj)

        # Форма Операций - Подрядчик
        formContractorOperations = self.requiredOperationContractorFormset(instance=obj)


        #Подсчет суммм для операций
        forms = RequiredOperationProject.objects.all().filter(idOrder=order_id).filter(isDone=True)
        sumProjectOperation = 0
        for form_ in forms:
            sumProjectOperation = sumProjectOperation + form_.cost

        forms = RequiredOperationManufactory.objects.all().filter(idOrder=order_id).filter(isDone=True)
        sumManufactoryOperation = 0
        for form_ in forms:
            sumManufactoryOperation = sumManufactoryOperation + form_.cost

        forms = RequiredOperationContractor.objects.all().filter(idOrder=order_id).filter(isDone=True)
        sumContractorOperation = 0
        for form_ in forms:
            sumContractorOperation = sumContractorOperation + form_.cost


        # objOrder нужен для получения номера заказа

        return render(request, "order.html", {"objOrder": obj,
                                              "form": form,

                                              "formMaterials": formMaterials,
                                              "formProjectOperations": formProjectOperations,
                                              "formManufactoryOperations": formManufactoryOperations,
                                              "formContractorOperations": formContractorOperations,

                                              "sumProjectOperation": sumProjectOperation,
                                              "sumManufactoryOperation": sumManufactoryOperation,
                                              "sumContractorOperation": sumContractorOperation,
                                              "sumTotal": sumProjectOperation + sumManufactoryOperation + sumContractorOperation
                                              })




    def post(self, request, *args, **kwargs):

        order_id = self.kwargs['order_id']

        if request.POST.get("RemoveBtn"):
            return redirect('/delete/' + order_id)

        obj = get_object_or_404(Order, id=order_id)
        orderForm = OrderForm(request.POST, instance=obj)


        #Форма требуемых материалов
        formMaterials = self.requiredMaterialFormset(request.POST, instance=obj)

        #Форма Операций  -Проект
        formProjectOperations = self.requiredOperationProjectFormset(request.POST, instance=obj)

        # Форма Операций  - Цех
        formManufactoryOperations = self.requiredOperationManufactoryFormset(request.POST, instance=obj)

        # Форма Операций - Подрядчик
        formContractorOperations = self.requiredOperationContractorFormset(request.POST, instance=obj)


        #Проверка валидности присланной формы
        errorString = ""
        if orderForm.is_valid() and formMaterials.is_valid() and \
                formProjectOperations.is_valid() and formManufactoryOperations.is_valid() and formContractorOperations.is_valid():

            obj = orderForm.save()

            instance = RequiredMaterial.objects.filter(idOrder=obj)
            instance.delete()

            # materials
            formMaterials.save(commit=False)

            for form in formMaterials:
                if form['count'].value():
                    choice = form.save(commit=False)
                    choice.idOrder = obj
                    choice.save()


            # project operation
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

            if request.POST.get("SaveBtn"):
                return redirect('/index')

        else:
            errorString = "Ошибка заполнения формы"




         #считаем суммы дял Апдейта или если форма не заполнена до конца
        forms = RequiredOperationProject.objects.all().filter(idOrder=order_id).filter(isDone=True)
        sumProjectOperation = 0
        for form_ in forms:
            sumProjectOperation = sumProjectOperation + form_.cost

        forms = RequiredOperationManufactory.objects.all().filter(idOrder=order_id).filter(isDone=True)
        sumManufactoryOperation = 0
        for form_ in forms:
            sumManufactoryOperation = sumManufactoryOperation + form_.cost

        forms = RequiredOperationContractor.objects.all().filter(idOrder=order_id).filter(isDone=True)
        sumContractorOperation = 0
        for form_ in forms:
            sumContractorOperation = sumContractorOperation + form_.cost


         #не смогли сохранить или нажата Update
        return render(request, "order.html", {"objOrder": obj,
                                              "form": orderForm,

                                              "formMaterials": formMaterials,
                                              "formProjectOperations": formProjectOperations,
                                              "formManufactoryOperations": formManufactoryOperations,
                                              "formContractorOperations": formContractorOperations,

                                              "sumProjectOperation": sumProjectOperation,
                                              "sumManufactoryOperation": sumManufactoryOperation,
                                              "sumContractorOperation": sumContractorOperation,
                                              "sumTotal": sumProjectOperation + sumManufactoryOperation + sumContractorOperation,

                                              "errorString" : errorString

                                              })