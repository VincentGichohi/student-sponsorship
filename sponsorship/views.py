import sponsorship
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import login as django_login, logout as django_logout, authenticate as django_authenticate
from django.contrib.auth.decorators import login_required
from .forms import AuthenticationForm, RegistrationForm, BioForm, SchoolForm, RecommendationForm
# from .models import user_type, User

# Create your views here.


def dashboard(request):
    return render(request, 'sponsorship/dashboard.html')


def register_request(request):
	if request.method == "POST":
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("login")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = RegistrationForm()
	return render (request,"sponsorship/register.html",{"register_form":form})


def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("dashboard")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request,"sponsorship/login.html",{"login_form":form})

def bio(request):

    return render(request, 'sponsorship/bio.html')

def index(request):
    return render(request, 'sponsorship/index.html')

def sponsor(request):
	return render(request, 'sonsorship/sponsor.html')