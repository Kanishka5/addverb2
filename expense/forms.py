from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Employee

# signup form


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Employee
        fields = ('username', 'name', 'mobile')

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        print(cleaned_data)
        name = cleaned_data.get('name')
        username = cleaned_data.get('username')
        mobile = cleaned_data.get('mobile')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Employee
        fields = ('name', 'username', 'mobile')


class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = Employee
        #fields = ('username', 'email','college','score','name',)
        fields = UserChangeForm.Meta.fields
