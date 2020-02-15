from django import forms
from .models import Order, RequiredMaterial, DillerCatalog
from .models import RequiredOperationProject, RequiredOperationManufactory, RequiredOperationContractor



class OrderForm(forms.ModelForm):

    cost = forms.IntegerField(required=False)
    prepayment = forms.IntegerField(required=False)

    class Meta:
        model = Order
        exclude = ['date_created', 'idOrder']
        widgets = {
                   'fio': forms.TextInput(attrs={'size': 40, "class" : "ajsdfjasdfj"}),

                   'nameOrder': forms.TextInput(attrs={'size': 40}),
                   'nameContract': forms.TextInput(attrs={'size': 40}),

                   'address': forms.TextInput(attrs={'size': 40}),
                   'phone': forms.TextInput(attrs={'size': 11}),

                   'trelloLink': forms.TextInput(attrs={'size': 40}),

                   'details': forms.Textarea(attrs={'cols': 40, 'rows': 4})
                   }

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)





class RequiredMaterialForm(forms.ModelForm):


    class Meta:
        model = RequiredMaterial
        fields = [ 'idMaterial', 'count', 'idOrder']




class DillerForm(forms.ModelForm):

    class Meta:
        model = DillerCatalog
        fields = ['name']



class RequiredOperationProjectForm(forms.ModelForm):

    class Meta:
        model = RequiredOperationProject
        fields = ['idOrder', 'idOperation', 'idWorker', 'cost', 'isDone', 'isDoneDate']
        widgets = {
            'isDoneDate': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
        }


    def __init__(self, *args, **kwargs):
        super(RequiredOperationProjectForm, self).__init__(*args, **kwargs)




class RequiredOperationManufactoryForm(forms.ModelForm):

    class Meta:
        model = RequiredOperationManufactory
        fields = ['idOrder', 'idOperation', 'idWorker', 'cost', 'isDone', 'isDoneDate']
        widgets = {
            'isDoneDate': forms.widgets.DateInput(attrs={'type': 'date'})
        }


class RequiredOperationContractorForm(forms.ModelForm):

    class Meta:
        model = RequiredOperationContractor
        fields = ['idOrder', 'idOperation', 'idWorker', 'cost', 'isDone', 'isDoneDate']
        widgets = {
            'isDoneDate': forms.widgets.DateInput(attrs={'type': 'date'}, format='%m/%d/%y')
        }