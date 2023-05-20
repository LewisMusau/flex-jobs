 # Create your views here.
from django.shortcuts import render, redirect
from .forms import RegistrationForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('register_success')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def register_success(request):
    return render(request, 'register_success.html')

def myprofile(request):
    return render(request, 'profile.html')


from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)  # Use auth_login instead of login
            # Redirect to a success page or the desired URL
            return redirect('home')  # Replace 'home' with your desired URL name
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

