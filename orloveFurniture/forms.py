from django import forms
from .models import Order, RequiredMaterial, DillerCatalog, RequiredOperation
from djangoformsetjs.utils import formset_media_js

class OrderForm(forms.ModelForm):

    cost = forms.IntegerField(required=False)
    prepayment = forms.IntegerField(required=False)

    class Meta:
        model = Order
        exclude = ['date_created', 'idOrder']
        widgets = {
                   'surname': forms.TextInput(attrs={'size': 40}),
                   'name': forms.TextInput(attrs={'size': 40}),
                   'patronymic': forms.TextInput(attrs={'size': 40}),
                   'address': forms.TextInput(attrs={'size': 40}),
                   'phone': forms.TextInput(attrs={'size': 11}),
                   'details': forms.Textarea(attrs={'cols': 40, 'rows': 5})
                   }

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.initial['status'] = '1'




class RequiredMaterialForm(forms.ModelForm):


    class Meta:
        model = RequiredMaterial
        fields = [ 'idMaterial', 'count', 'idOrder']




class DillerForm(forms.ModelForm):

    class Meta:
        model = DillerCatalog
        fields = ['name']



class RequiredOperationForm(forms.ModelForm):

    class Meta:
        model = RequiredOperation
        fields = ['idOrder', 'idOperation', 'idWorker', 'cost']


