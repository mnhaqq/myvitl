from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Record
from django.contrib import messages
from .utils import scan_code
from math import pow


@login_required
def patient_dashboard(request):
    user_profile = request.user.profile

    if not user_profile.is_complete:
        messages.error(request, "Complete your profile")
        return redirect('profile')
    
    user_records = Record.objects.filter(user=request.user).order_by('-date')[:4]
    no_records = len(user_records) == 0
    date_query = request.GET.get('date')
    if date_query:
        user_records = Record.objects.filter(user=request.user, date__date=date_query).order_by('-date')[:4]

    if request.method ==  'POST':
        res = int(scan_code())
        Record.objects.create(
            user=request.user,
            temperature = (res % 1000) / 10,
            heart_rate = int(res / 10 ** 5),
            sugar_level = round((res / 10 ** 4) % 10, 1)
        )
        return redirect("patient_dashboard")

    context = {
        'user_profile': user_profile,
        'user_records': user_records,
        'no_records': no_records,
    }
    return render(request, 'records/patient_dashboard.html', context)



