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
        login(request, instance)
        return redirect('profile')
    
    context={'form':form}
    return render(request, 'accounts/signup.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('patient_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('patient_dashboard')
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
        instance = form.save(commit=False)

        cleaned_data = form.cleaned_data

        for field_name, value in cleaned_data.items():
            if field_name == 'is_complete' or field_name == 'user':
                continue
            if not value:
                instance.save()
                profile.is_complete = False
                messages.error(request, "Complete your profile")
                return redirect('profile')

        instance.is_complete = True
        instance.save()       

        return redirect('patient_dashboard')

    context = {
        'profile': profile,
        'form': form
    }
    return render(request, 'accounts/profile_update.html', context)
    