from django import forms
from django.contrib.auth.models import User
from piramid.models import TempInvoices


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput, min_length=8)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput, min_length=8)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'example@gmail.com',
        })

        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Alex',
        })

        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '********',
            'id': 'password-input',
        })

        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '********',
            'id': 'password-input',
        })

        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Username',
            'id': 'password-input',
        })

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    def clean_email(self):
        cd = self.cleaned_data
        if User.objects.filter(email=cd.get('email')).exists():
            raise forms.ValidationError('Email is taken.')
        return cd


class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    next = forms.CharField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'example@gmail.com',
        })

        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '********',
            'id': 'password-input',
        })


class DepositForm(forms.Form):
    amount = forms.IntegerField(label='Amount')

    def __init__(self, *args, **kwargs):
        super(DepositForm, self).__init__(*args, **kwargs)
        self.fields['amount'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '100',
        })
