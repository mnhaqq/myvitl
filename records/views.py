from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Record
from django.contrib import messages


# Create your views here.
@login_required
def patient_dashboard(request):
    user_profile = request.user.profile

    if not user_profile.is_complete:
        messages.error(request, "Complete your profile")
        return redirect('profile')
    
    user_records = Record.objects.filter(user=request.user)[:4:-1]
    no_records = len(user_records) == 0
    date_query = request.GET.get('date')
    if date_query:
        user_records = Record.objects.filter(user=request.user, date__date=date_query)[:4:-1]

    context = {
        'user_profile': user_profile,
        'user_records': user_records,
        'no_records': no_records,
    }
    return render(request, 'records/patient_dashboard.html', context)



