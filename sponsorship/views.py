import sponsorship
from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required
from .forms import BioForm, SchoolForm, RecommendationForm, ContactForm,RegistrationForm,AccountAuthenticationForm,AccountUpdateform
from .models import Student, Sponsor, CustomUser
from flask import request
from . import forms
# Create your views here.


def dashboard(request):
    return render(request, 'sponsorship/dashboard.html')


def register_request(request):
	"""
      Renders Registration Form 
    """
    	
	context = {}

	if request.method== 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			email    = form.cleaned_data.get('email')
			raw_pass = form.cleaned_data.get('password1')
			user = authenticate(email=email, password = raw_pass)
			login(request, user)
			messages.success(request, "You have been Registered as {}".format(request.user.username))
			return redirect('login')
		else:
			messages.error(request, "Please Correct Below Errors")
			context['registration_form'] = form
	else:
		form = RegistrationForm()
		context['registration_form'] = form
	return render (request,"sponsorship/register.html",context)


def login_request(request):
	"""
    	Renders Login Form
    """
	context={}
	user=request.user
	if user.is_authenticated:
		return redirect('login')
	if request.method=='POST':
		form=AccountAuthenticationForm(request.POST)
		email=request.POST.get('email')
		password=request.POST.get('password')
		user=authenticate(email=email, password=password)
		if user:
			login(request, user)
			messages.success(request, 'Logged In')
			return redirect('dashboard')
		else:
			messages.error('please Correct Below Errors')
	
	else:
		form=AccountAuthenticationForm
	context['login_form']=form
	return render(request, 'sponsorship/login.html', context)




def account_view (request):
    """
      Renders userprofile page "
    """
    if not request.user.is_authenticated:
        return redirect("login")
    context = {}
    if request.POST:
        form = AccountUpdateform(request.POST, instance = request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "profile Updated")
        else:
            messages.error(request, "Please Correct Below Errors")
    else:
        form  = AccountUpdateform(
            initial={
            'email':request.user.email,
            'username':request.user.username,
            }
        )
    context['account_form']=form

    return render(request, "accounts/userprofile.html",context)

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("homepage")

def contact(request):
  if request.method == 'POST':
    form = ContactForm(request.POST)
    if form.is_valid():
      subject = "Website Inquiry" 
      body = {
      'first_name': form.cleaned_data['first_name'], 
      'last_name': form.cleaned_data['last_name'], 
      'email': form.cleaned_data['email_address'], 
      'message':form.cleaned_data['message'], 
      }
      message = "\n".join(body.values())

      try:
        send_mail(subject, message, 'admin@example.com', ['admin@example.com']) 
      except BadHeaderError:
        return HttpResponse('Invalid header found.')
      messages.success(request, "Message sent." )
      return redirect ("sponsorship:homepage")
    messages.error(request, "Error. Message not sent.")
      
  form = ContactForm()
  return render(request, "sponsorship/contact.html", {'form':form})

def success(request):
    sub = forms.Success()
    if request.method == 'POST':
        sub = forms.Success(request.POST)
        subject = 'Welcome to Student Sponsorship'
        message = 'Your application was approved successfuly'
        recepient = str(sub['Email'].value())
        send_mail(subject, 
            message, EMAIL_HOST_USER, [recepient], fail_silently = False)
        return render(request, 'subscribe/success.html', {'recepient': recepient})
    return render(request, 'subscribe/index.html', {'form':sub})

def bio(request):
	submitted=False
	if request.method=="POST":
			form=BioForm(request.POST)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/bio? submitted=True')
	else:
		form=BioForm()
		if 'submitted' in request.GET:
			submitted=True
	form=BioForm
	return render(request, 'sponsorship/bio.html', {"form":form,'submitted':submitted})

def school(request):
	submitted=False
	if request.method=="POST":
			form=SchoolForm(request.POST)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/school? submitted=True')
	else:
		form=SchoolForm
		if 'submitted' in request.GET:
			submitted=True
	form=SchoolForm
	return render(request,'sponsorship/school.html', {"form":form,'submitted':submitted})

def recommendation(request):
		submitted=False
		if request.method=="POST":
				form=RecommendationForm(request.POST)
				if form.is_valid():
					form.save()
					return HttpResponseRedirect('/reasons? submitted=True')
		else:
			form=RecommendationForm
			if 'submitted' in request.GET:
				submitted=True
		form=RecommendationForm
		return render(request,'sponsorship/recommendation.html',{"form":form,'submitted':submitted})

def index(request):
    return render(request, 'sponsorship/index.html')

def sponsor(request):
	return render(request, 'sonsorship/sponsor.html')

def student_table(request):
	sdetails=Sponsor.objects.all()
	context={
		'sdetails':sdetails
	}
	return render(request, 'sponsorship/student_table.html',context)