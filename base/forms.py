from customusers.models import CustomUser
from django import forms
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email']

class UserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'password1', 'password2']

class LoginForm(forms.Form):
    username_email = forms.CharField(max_length=254, label='Username or Email')
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        username_email = cleaned_data.get('username_email')
        password = cleaned_data.get('password')

        if not username_email or not password:
            raise forms.ValidationError('Please provide both username/email and password.')

        return cleaned_data