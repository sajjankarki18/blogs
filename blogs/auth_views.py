from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import CustomCreationForm

# auth_views

# view for user login
def userLogin(request):
    
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        
        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Invalid credentials! Please try again...')
            return redirect('home')
        
    return render(request, 'auth_routes/userLogin.html')


# view for creating a new account
def userRegistration(request):
    form = CustomCreationForm()
    
    if request.method == 'POST':
        form = CustomCreationForm(request.POST)
        
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            
            if password1 == password2:
                user = auth.authenticate(username=username, email=email, password=password1)
                
                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.info(request, "Invalid credentials! Try again...")
            else:
                messages.info(request, "Password did'nt match! Please try again....")
                return redirect('userRegistration')
    
    context = {"form": form}        
    return render(request, 'auth_routes/userRegistration.html', context)

# logout user view
def userLogout(request):
    logout(request)
    return redirect('userLogin')