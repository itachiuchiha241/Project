from django import forms 
from .models import Pet, CustomUser
from django.contrib.auth.forms import UserCreationForm

class CustomUserRegistrationForm(UserCreationForm):
    city = forms.CharField(max_length=50)
    phone_number = forms.CharField(max_length=20)

    class Meta:
        model = CustomUser
        fields =  ['first_name', 'last_name', 'username', 'email', 'city', 'phone_number']

        def save(self, commit=True):
            user = super().save(commit=False)
            user.city = self.cleaned_data['city']
            user.phone_number = self.cleaned_data['phone_number']

            if commit:
                user.save()
            return user

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields =  ['name', 'breed', 'price', 'image', 'tags']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'breed': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }