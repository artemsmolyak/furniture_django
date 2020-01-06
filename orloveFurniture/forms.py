from django import forms


class OrderForm(forms.Form):
    surname = forms.CharField(max_length=255)
    name = forms.CharField(max_length=255)
    patronymic = forms.CharField(max_length=255)