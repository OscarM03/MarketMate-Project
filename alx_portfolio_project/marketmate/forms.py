from django.forms import ModelForm
from django import forms
from .models import Business, Product

class businessForm(ModelForm):
    # category = forms.CharField(required=True)

    class Meta:
        model = Business
        fields = '__all__'
        exclude = ['b_id', 'votes', 'owner']
