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

        # Membuat user baru dengan field role kustom
        user = User.objects.create_user(username=u_name, password=p_word)
        user.role = u_role 
        user.save()
        
        messages.success(request, "Akun berhasil dibuat! Silakan login.")
        return redirect('login')
    
    return render(request, 'register.html')

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("dashboard")
        messages.error(request, "Username atau password salah.")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

def logout_view(request):
    logout(request)
    messages.info(request, "Anda telah logout.")
    return redirect("login")