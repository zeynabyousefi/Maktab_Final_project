from django import forms
from django.core.exceptions import ValidationError
from django.forms import EmailInput

from .models import *
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
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'sarboland@email.com'}))
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


class AddContact(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'zeynabyousefi1380@zyo.com'}))
    name = forms.CharField(label='name',
                           widget=forms.TextInput(
                               attrs={'class': 'form-control', 'placeholder': 'zeynab_yousefi'}))
    phone = forms.CharField(label='phone number',
                            widget=forms.TextInput(
                                attrs={'class': 'form-control', 'placeholder': '+9999999'}))
    birthdate = forms.DateField(label="birthdate", widget=forms.DateInput(
        attrs={'class': 'form-control', 'placeholder': '2022/03/12'})
                                )


class CreationEmail(forms.Form):
    subject = forms.CharField(label='Subject',
                              widget=forms.TextInput(
                                  attrs={'class': 'form-control', 'placeholder': 'subject'}))
    body = forms.CharField(label='Body',
                           widget=forms.TextInput(
                               attrs={'class': 'form-control', 'placeholder': 'body'}))
    attachment = forms.FileField(label='file',
                                 widget=forms.FileInput(
                                     attrs={'class': 'form-control', 'placeholder': 'fileupload'}))
    cc = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'zeynabyousefi1380@zyo.com'}),
        required=False)
    bcc = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'zeynabyousefi1380@zyo.com'}),
        required=False)


class AddContact(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name',
                  'email',
                  'phone',
                  'birthdate',

                  ]
        widgets = {
            'birthdate': DateInput(),
        }


class AddSignatureForm(forms.ModelForm):
    class Meta:
        model = Signature
        fields = ['name',
                  'content',
                  ]