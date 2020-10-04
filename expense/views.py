from django.shortcuts import render
from .forms import CustomUserCreationForm, SignUpForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone


# homepage ->
def home(request):
    return render(request, 'home.html')


# singup ->
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        print(form)
        if form.is_valid():
            user = form.save(commit=False)
            if request.user.is_anonymous:
                user.is_active = True
                user.save()
                login(request, user)
                message = "Logged In !"
                return render(request, 'home.html', {'message': message})
            else:
                message = "You are logged in already"
                return render(request, 'home.html', {'message': message})
        else:
            message = "Invalid employee ID."
            return render(request, 'signup.html', {'message': message})
    else:
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})
