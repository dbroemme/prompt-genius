# Create your views here.
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.shortcuts import render, redirect


def display_session_keys(request):
    for a_key in request.session.keys():
        print("Session " + a_key + ": " + str(request.session[a_key]))

def main_menu(request):
    return render(request, 'menu.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to the desired page after successful login
            return redirect('main_menu')
        else:
            # Authentication failed
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to the desired page after successful registration
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def logout_view(request):
    logout(request)
    # Redirect to the desired page after logout
    return redirect('login')


