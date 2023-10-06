from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
# from profile.models import MyUser


class SignForm(UserCreationForm):
    password1 = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                label='Password')
    password2 = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                label='Confirm password')

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        widgets = {
            'username': forms.TextInput(attrs={'class': "form-control input-lg"}),
            'email': forms.EmailInput(attrs={'class': "form-control input-lg"}),
        }


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ("username", "password")
        widgets = {
            'username': forms.TextInput(attrs={'class': "form-control input-lg"}),
            'email': forms.EmailInput(attrs={'class': "form-control input-lg"}),
        }


class CodeForm(forms.Form):
    verified_fieid = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control input-lg"}))


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get_or_create(name='basic')[0]
        basic_group.user_set.add(user)
        return user


    # def clean_username(self):
    #     username = self.cleaned_data.get('username')
    #     if User.objects.filter(username=username).exists():
    #         raise forms.ValidationError("Пользователь с таким именем уже существует")
    #     return username
    #
    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     if User.objects.filter(email=email).exists():
    #         raise forms.ValidationError("Пользователь с таким email уже существует")
    #     return email

