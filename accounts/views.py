from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.contrib.auth.decorators import login_required
from .models import History

@login_required
def settings(request):
    return render(request, 'profile/settings.html')

@login_required
def history(request):
    history = History.objects.filter(user=request.user)
    context = {'history': history}
    return render(request, 'profile/history.html', context)