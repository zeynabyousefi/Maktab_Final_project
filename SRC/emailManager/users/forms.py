from django import forms
from django.core.exceptions import ValidationError
from django.forms import EmailInput

from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm


class DateInput(forms.DateInput):
    input_type = 'date'


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username',
                  'first_name',
                  'last_name',
                  'birthdate',
                  'gender',
                  'country',
                  'recovery_email',
                  'phone_number',
                  'password1',
                  'password2'
                  ]
        widgets = {
            'birthdate': DateInput(),
        }


class VerifyCodeForm(forms.Form):
    code = forms.IntegerField()


class UserLoginForm(forms.Form):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'zeynabyousefi1380@zyo.com'}))
    password = forms.CharField(label='password',
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '******'}))


class ResetPasswordForm(forms.Form):
    recovery_email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'zeynabyousefi1380@zyo.com'}),
        required=False)
    phone_number = forms.CharField(label='phone_number',
                                   widget=forms.TextInput(
                                       attrs={'class': 'form-control', 'placeholder': '0930********'}),
                                   required=False)


class ResetPasswordConfirmForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['password1', 'password2']

    password1 = forms.CharField(label='password',
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': '******'}))
    password2 = forms.CharField(label='password',
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': '******'}))
