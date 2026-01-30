from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def show_dashboard(request):
    return render(request, "dashboard.html")

@login_required(login_url='login')
def show_dashboard_employee(request):
    return render(request, "dashboard_employee.html")