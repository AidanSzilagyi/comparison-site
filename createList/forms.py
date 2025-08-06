from django import forms
from .models import Thing, List, Profile

class ListForm(forms.ModelForm):
    class Meta:
        model = List
        fields = ['name', 'image', 'description', 'permission', 'comparison_method']

class ThingForm(forms.ModelForm):
    class Meta:
        model = Thing
        fields = ['name', 'image']
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['username', 'image']
