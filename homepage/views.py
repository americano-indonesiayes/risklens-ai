from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def show_home(request):
    return render(request, "homepage.html")
