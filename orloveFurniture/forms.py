from django import forms
from .models import Order, RequiredMaterial
from djangoformsetjs.utils import formset_media_js

class OrderForm(forms.ModelForm):

    surname = forms.CharField(max_length=255)
    name = forms.CharField(max_length=255)
    patronymic = forms.CharField(max_length=255)
    details = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Order
        fields = ('__all__')

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.initial['status'] = '1'




class RequiredMaterialForm(forms.ModelForm):

    count = forms.IntegerField()

    class Meta:
        model = RequiredMaterial
        fields = [ 'idMaterial', 'count']








