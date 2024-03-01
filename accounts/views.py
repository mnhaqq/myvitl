from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import Profile
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm


def signup(request):
    if request.user.is_authenticated:
        return redirect('profile')
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        instance = form.save()
        Profile.objects.create(user=instance)
        return redirect('login')
    
    context={'form':form}
    return render(request, 'accounts/signup.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('profile')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            messages.warning(request, 'Invalid username or password')
            return redirect('login')
    return render(request, 'accounts/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile(request):
    profile = Profile.objects.get(user=request.user)
    
    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)

    if form.is_valid():
        form.save()
        redirect('profile')

    context = {
        'profile': profile,
        'form': form
    }
    return render(request, 'accounts/profile_update.html', context)
    