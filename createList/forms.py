from django import forms
from .models import Thing, List

class ListForm(forms.ModelForm):
    class Meta:
        model = List
        fields = ['name', 'image', 'description']

class ThingForm(forms.ModelForm):
    class Meta:
        model = Thing
        fields = ['name', 'image']
