from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from authentication.decorators import role_required

@login_required(login_url='login')
@role_required("admin")
def show_company(request):
    return render(request, "company.html")
