from django.shortcuts import render
from .forms import CustomUserCreationForm, SignUpForm, ExpenseForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.shortcuts import redirect
from .models import Employee, Expense


# homepage ->
def home(request):
    return render(request, 'home.html', {})


# singup ->
def signup(request):
    if request.user.is_anonymous: 
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
                    return redirect('dashboard') 
                else:
                    message = "You are logged in already"
                    return redirect('dashboard')
            else: 
                message = "Invalid employee ID."
                return render(request, 'signup.html', {'message': message}) 
        else: 
            form = SignUpForm()
            return render(request, 'signup.html', {'form': form}) 
    else:
        return redirect('home')


#signin ->
def signin(request):
    if request.user.is_anonymous: 
        if request.method == 'POST': 
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password) 
            if user:
                if user.is_active:
                    login(request, user) 
                    return redirect('dashboard') 
                else:
                    return HttpResponse(
                        "Your account was inactive. Contact Admin")
            else:
                print("Someone tried to login and failed.")
                message = "Invalid login details!"
                return render(request, 'signin.html', {'message': message})
        else:
            return render(request, 'signin.html', {})
    else:
        return redirect('home')



#logout ->
def logoutReq(request):
    logout(request)
    return redirect('home')


#dashboard ->
def dashboard(request):
    if request.user.is_anonymous:
        return redirect('signin')
    else:
        empid = int(request.user.id)
        user = Employee.objects.get(pk=empid)
        approvereq = {}
        team = {}
        payreq = {}
        teamexpense = 0
        yourexpense = 0
        if (user.profile == '1'):
            underman = Employee.objects.filter(managerid_id=empid)
            approvereq = Expense.objects.filter(username_id__in=underman,
                                          approvalstatus=False)
            own_team = Employee.objects.filter(
                managerid_id=empid) | Employee.objects.filter(id=empid)
            team = Expense.objects.filter(username_id__in=own_team)

            for t in team:
                teamexpense += t.amount
            # approvereq = Expense.objects.raw(
            #     'SELECT * FROM expense_expense WHERE username_id in (SELECT id from expense_employee WHERE managerid_id = %s)',
            #     [empid])
        elif (user.profile == '3'):
            payreq = Expense.objects.filter(approvalstatus=True,paymentstatus=False)

        expenses = Expense.objects.filter(username=empid).order_by('date')
        for expense in expenses:
            yourexpense += expense.amount

        return render(
            request, 'dashboard.html', {
                'expenses': expenses,
                'approvereq': approvereq,
                'payreq': payreq,
                'team': team,
                'teamexpense': round(teamexpense, 2),
                'yourexpense': round(yourexpense, 2)
            })


#expense form ->
def expenseform(request):
    if request.user.is_anonymous:
        return redirect('signin')
    else:
        if (request.method == 'POST'):
            print(request.FILES)
            data = request.POST
            empid = int(request.user.id)
            user = Employee.objects.get(pk=empid)
            _mutable = data._mutable
            data._mutable = True
            data['username'] = empid
            if (user.profile == '1' or user.profile == '3'):
                data['approvalstatus'] = True
            data._mutable = _mutable
            form = ExpenseForm(data, request.FILES)
            print(form)
            if form.is_valid():
                expense = form.save(commit=False)
                expense.save()
                return redirect('dashboard')
            else:
                print('error')
                return render(request, 'expenseform.html')
        else:
            form = ExpenseForm()
            return render(request, 'expenseform.html', {'form': form})


# accept/reject approval request ->
def approve(request):
    if (request.method == 'POST'):
        print(request.POST.get('Approval'))
        if (request.POST.get('Approval') == 'Approve'):
            expenseid = request.POST.get('expenseid')
            Expense.objects.filter(pk=expenseid).update(approvalstatus=True)
        # Expense.objects.raw(
        #     'UPDATE expense_expense SET approvalstatus=True WHERE username_id = %s',
        #     [empid])
    return redirect('dashboard')


# accept/reject payment request ->
def paymentreq(request):
    if (request.method == 'POST'):
        if (request.POST.get('Approval') == 'Approve'):
            expenseid = request.POST.get('expenseid')
            Expense.objects.filter(pk=expenseid).update(paymentstatus=True)
        # Expense.objects.raw(
        #     'UPDATE expense_expense SET approvalstatus=True WHERE username_id = %s',
        #     [empid])
    return redirect('dashboard')
