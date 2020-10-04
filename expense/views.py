from django.shortcuts import render
from .forms import CustomUserCreationForm, SignUpForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.shortcuts import redirect
from .models import Employee


# homepage ->
def home(request):
    if request.user.is_anonymous:
        return render(request, 'home.html')
    else:
        t = int(request.user.id)
        user = Employee.objects.get(id=t)
        print(user)
        return render(request, 'home.html', {'name': user})


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


#signin ->
def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('/')
            else:
                return HttpResponse("Your account was inactive. Contact Admin")
        else:
            print("Someone tried to login and failed.")
            message = "Invalid login details!"
            return render(request, 'signin.html', {'message': message})
    else:
        return render(request, 'signin.html', {})


#logout ->
def logoutReq(request):
    logout(request)
    return redirect('/')


#dashboard ->
def dashboard(request):
    return render(request, 'dashboard.html')
