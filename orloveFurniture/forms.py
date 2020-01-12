from django import forms
from .models import Order, RequiredMaterial
from djangoformsetjs.utils import formset_media_js

class OrderForm(forms.ModelForm):

    details = forms.CharField(widget=forms.Textarea)


    class Meta:
        model = Order
        exclude = ['date_created', 'idOrder']
        widgets = {'surname': forms.TextInput(attrs={'size': 40}),
                   'name': forms.TextInput(attrs={'size': 40}),
                   'patronymic': forms.TextInput(attrs={'size': 40}),
                   'idOrder': forms.TextInput(attrs={'size': 40})}

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.initial['status'] = '1'




class RequiredMaterialForm(forms.ModelForm):

    count = forms.IntegerField()

    class Meta:
        model = RequiredMaterial
        fields = [ 'idMaterial', 'count', 'idOrder']








