from django.shortcuts import render
from .forms import CustomUserCreationForm, SignUpForm, ExpenseForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.shortcuts import redirect
from .models import Employee, Expense


# homepage ->
def home(request):
    if request.user.is_anonymous:
        return render(request, 'home.html')
    else:
        t = int(request.user.id)
        user = Employee.objects.get(id=t)
        return render(request, 'home.html', {'name': user.name})


# singup ->
def signup(request):
    if request.method == 'POST':
        data = request.POST
        managerid = data['managerid']
        if (managerid):
            managerpk = Employee.objects.get(username=managerid).id
            _mutable = data._mutable
            data._mutable = True
            data['managerid'] = managerpk
            data._mutable = _mutable
        form = SignUpForm(data)
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
    t = int(request.user.id)
    expenses = Expense.objects.filter(username=t).order_by('date')
    return render(request, 'dashboard.html', {'expenses': expenses})


#expense form ->
def expenseform(request):
    if (request.method == 'POST'):
        data = request.POST
        user = request.user.id
        _mutable = data._mutable
        data._mutable = True
        data['username'] = user
        data._mutable = _mutable
        print(data)
        form = ExpenseForm(data)
        print(form)

        if form.is_valid():
            expense = form.save(commit=False)
            expense.save()
            return redirect('dashboard')
        else:
            return render(request, 'expenseform.html')
    else:
        return render(request, 'expenseform.html')
