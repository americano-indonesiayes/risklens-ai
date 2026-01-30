from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .forms import RegisterForm
from .models import Profile
from .models import User

def register_view(request):
    if request.method == 'POST':
        u_name = request.POST.get('username')
        p_word = request.POST.get('password')
        cp_word = request.POST.get('confirm_password')
        u_role = request.POST.get('role') 
        
        if p_word != cp_word:
            messages.error(request, "Password tidak cocok!")
            return redirect('register')
        
        if User.objects.filter(username=u_name).exists():
            messages.error(request, "Username sudah digunakan.")
            return redirect('register')

        user = User.objects.create_user(username=u_name, password=p_word)
        
        if u_role not in ['admin', 'employee']:
            u_role = 'employee' 
            
        Profile.objects.create(user=user, role=u_role) 

        messages.success(request, "Akun berhasil dibuat! Silakan login.")
        return redirect('login')
    
    return render(request, 'register.html')

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            selected_role = request.POST.get('role') 

            user = authenticate(username=username, password=password)

            if user is not None:
                if hasattr(user, 'profile') and user.profile.role == selected_role:
                    login(request, user)
                    if user.profile.role == "admin":
                        return redirect("dashboard")
                    else:
                        return redirect("dashboard_employee")
                else:
                    messages.error(request, f"Akun ini bukan terdaftar sebagai {selected_role}.")
            else:
                messages.error(request, "Username atau password salah.")
        else:
            messages.error(request, "Form tidak valid.")
    else:
        form = AuthenticationForm()
    
    return render(request, "login.html", {"form": form})

def logout_view(request):
    logout(request)
    messages.info(request, "Anda telah logout.")
    return redirect("login")