from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)  # Champ email par exemple

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = UserProfile
        fields = ['email','location', 'birth_date', 'gender', 'phone_number']  # Liste des champs supplémentaires
