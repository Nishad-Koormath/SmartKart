from django.shortcuts import render,redirect
from django.contrib.auth import login, logout, authenticate
from .forms import UserRegistrationForm ,AuthenticationForm

# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user after registration
            return redirect('home')  # Redirect to home page or any other page
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to the home page or another page
            else:
                # Invalid login
                form.add_error(None, 'Invalid username or password')
    else:
        form = AuthenticationForm()
        
    return render(request, 'accounts/login.html', {'form': form})
