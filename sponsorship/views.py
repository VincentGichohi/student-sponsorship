import sponsorship
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth import login as django_login, logout as django_logout, authenticate as django_authenticate
from django.contrib.auth.decorators import login_required
# from .forms import AuthenticationForm, RegistrationForm, BioForm, SchoolForm, RecommendationForm
# from .models import user_type, User

# Create your views here.


def dashboard(request):
    return render(request, 'sponsorship/dashboard.html')

def bio(request):
    return render(request, 'sponsorship/bio.html')

def index(request):
    return render(request, 'sponsorship/index.html')