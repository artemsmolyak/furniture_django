from django import forms
from .models import Order, RequiredMaterial
from djangoformsetjs.utils import formset_media_js

class OrderForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__( *args, **kwargs )
        self.initial['status'] = '1'

    class Meta:
        model = Order
        exclude = ['date_created']




class RequiredMaterialForm(forms.ModelForm):

    class Meta:
        model = RequiredMaterial
        fields = [ 'idMaterial', 'count']





