from django import forms
from .models import Thing, List, Profile
from django.core.exceptions import ValidationError

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['username', 'image']
        error_messages = {
            'username': {
                'required': "Please enter a valid username.",
                'max_length': "The username must be under 20 characters.",
                'unique': "That username has already been taken. Please choose another name.",
                'invalid': "Usernames can only contain letters, numbers, underscores and dashes"
            },
            'image': {
                'invalid': "The list image file is not valid.",
                'invalid_image': "The list image file must be a valid image format (JPEG, PNG, etc.).",
            },
        }

class ListForm(forms.ModelForm):
    class Meta:
        model = List
        fields = ['name', 'image', 'description', 'permission', 'comparison_method']
        error_messages = {
            'name': {
                'required': "Please enter a name for the list.",
                'max_length': "The list name must be under 100 characters.",
                'unique': "That list name has already been taken. Please choose another name.",
            },
            'image': {
                'invalid': "The list image file is not valid.",
                'invalid_image': "The list image file must be a valid image format (JPEG, PNG, etc.).",
            },
            'description': {
                'max_length': "The list description must be under 1000 characters.",
            },
        }

class ThingForm(forms.ModelForm):
    class Meta:
        model = Thing
        fields = ["name", "image"]
        error_messages = {
            'name': {
                'max_length': "The name must be under 100 characters.",
            },
            'image': {
                'invalid': "The image file is not valid.",
                'invalid_image': "The image file must be a valid image format (JPEG, PNG, etc.).",
            },
        }
    # Ensures that:
    # 1) Lists of type "text" (Text+Image) have a unique name (case-insensitve)
    # 2) Lists of type "image" (Images Only) have a unique image
    def clean(self):
        cleaned_data = super().clean()
        list = self.instance.list
        name = cleaned_data.get("name")
        image = cleaned_data.get("image")

        # Due to the different list types, this cannot be done at the model level
        if list.type == "text":
            if not name:
                self.add_error("name", "Please enter a name for this thing.")
            if Thing.objects.filter(list=list, name__iexact=name).exclude(pk=self.instance.pk).exists():
                self.add_error("name", "A Thing with this name already exists.")
        if list.type == "image":
            if not image:
                self.add_error("image", "Please add an image for this thing.")
            if self.image and Thing.objects.filter(list=list, image=image).exclude(pk=self.instance.pk).exists():
                self.add_error("image", "A Thing with this image already exists.")
        return cleaned_data

NUM_THINGS_REQUIRED = 4
class BaseThingFormSet(forms.BaseModelFormSet):
    def clean(self):
        super().clean()
        if any(self.errors):
            return  # Don’t re-check if individual forms already invalid

        # Count non-deleted, non-empty forms
        valid_forms = [form for form in self.forms
            if form.cleaned_data and not form.cleaned_data.get("DELETE")]
        if len(valid_forms) < NUM_THINGS_REQUIRED:
            raise ValidationError(f"You must include at least {NUM_THINGS_REQUIRED} things.")
