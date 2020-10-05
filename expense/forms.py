from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Employee, Expense


# signup form
class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Employee
        fields = ('username', 'name', 'mobile', 'email', 'profile',
                  'managerid', 'accountno')

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        print(cleaned_data)
        name = cleaned_data.get('name')
        username = cleaned_data.get('username')
        mobile = cleaned_data.get('mobile')
        email = cleaned_data.get('email')
        profile = cleaned_data.get('profile')
        managerid = cleaned_data.get('managerid')
        accountno = cleaned_data.get('accountno')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')


#expense register form ->
class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ('description', 'amount', 'date', 'attachments', 'username')

    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Employee
        fields = ('name', 'username', 'mobile')


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Employee
        fields = UserChangeForm.Meta.fields
