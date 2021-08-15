from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Kasutaja nimi'
        self.fields['password'].label = 'Parool'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = User.objects.filter(username=username).first()
        if not user:
            raise forms.ValidationError(f'Kasutaja {username} ei ole leitud')
        if not user.check_password(password):
            raise forms.ValidationError('Vale parool')
        return self.cleaned_data


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    phone = forms.CharField(required=False)
    address = forms.CharField(required=False)
    email = forms.EmailField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Kasutaja nimi'
        self.fields['confirm_password'].label = 'Kinnitage parool'
        self.fields['phone'].label = 'Telefoni number'
        self.fields['address'].label = 'Aadres'
        self.fields['email'].label = 'Email'
        self.fields['first_name'].label = 'Eesnimi'
        self.fields['last_name'].label = 'Perekonnanimi'

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'{username} on juba kasutuses')
        return username

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('Sisesta sama paroolid')
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'first_name', 'last_name', 'email', 'phone', 'address']
