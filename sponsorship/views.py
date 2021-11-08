import sponsorship
from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required
from .forms import BioForm, ContactForm,SchoolForm,StudentSignUpForm,SponsorSignUpForm,StaffSignUpForm, RecommendationForm, RegistrationForm,AccountAuthenticationForm,AccountUpdateform
from .models import Student, Sponsor, MyUser
from .decorators import anauthenticated_user
from django.views.generic import CreateView
from flask import request
from . import forms
from django.contrib.auth import get_user_model
# Create your views here.

user = get_user_model

@ login_required
def dashboard(request):

    return render(request, 'sponsorship/dashboard.html')

def register_request(request):
	"""
      Renders Registration Form 
    """
	context = {}
	if not request.user.is_authenticated:
		return redirect ('index')
	else:
		if request.method == 'POST':
			form = RegistrationForm(request.POST)
			if form.is_valid():
				form.save()
				email = form.cleaned_data.get('email')
				raw_pass = form.cleaned_data.get('password1')
				user = authenticate(email=email, password=raw_pass)
				login(request, user)
				messages.success(request, "You have been Registered as {}".format(request.user.email))
				return redirect('login')
			else:
				messages.error(request, "Please Correct Below Errors")
				context['registration_form'] = form
		else:
			form = RegistrationForm()
			context['registration_form'] = form
			return render(request, "sponsorship/register.html", context)

# a view for logging in users
def login_request(request):
	"""
    	Renders Login Form
    """
	context={}
	if not request.user.is_authenticated:
		return redirect ('login')
	else:
		if request.method == 'POST':
			form = AccountAuthenticationForm(request.POST)
			email = request.POST.get('email')
			password = request.POST.get('password')
			user = authenticate(email=email, password=password)
			if user is not None:
				login(request, user)
				messages.success(request, 'You have successfully logged in as {}'.format(request.user.email))
				return redirect('dashboard')
			else:
				messages.error(request, 'Please Correct Below Errors')
		else:
			form=AccountAuthenticationForm()
			context['login_form'] = form
		return render(request, 'sponsorship/login.html', context)

#a view for rendering user profile page
def account_view (request):
    """
      Renders userprofile page "
    """
    if not request.user.is_authenticated:
        return redirect("login")
    context = {}
    if request.POST:
        form = AccountUpdateform(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "profile Updated")
        else:
            messages.error(request, "Please Correct Below Errors")
    else:
        form  = AccountUpdateform(
            initial={
            'email':request.user.email,
            }
        )
    context['account_form']=form

    return render(request, "accounts/userprofile.html",context)

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect('index')

# a view for contact
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
      return redirect ("main:homepage")
    messages.error(request, "Error. Message not sent.")
      
  form = ContactForm()
  context = {'form': form}
  return render(request, "sponsorship/contact.html", context)

# a view message for sending email success message
def success(request):
    sub = forms.Success()
    if request.method == 'POST':
        sub = forms.Success(request.POST)
        subject = 'Welcome to Student Sponsorship'
        message = 'Your application was approved successfully'
        recepient = str(sub['Email'].value())
        send_mail(subject, 
            message, EMAIL_HOST_USER, [recepient], fail_silently = False)
        return render(request, 'subscribe/success.html', {'recepient': recepient})
    return render(request, 'subscribe/index.html', {'form':sub})

#a view for uploading bio data
class StudentSignUpView(CreateView):
	model = MyUser
	form_class = StudentSignUpForm
	template_name = 'sponsorship/student_register.html'

	def get_context_data(self, **kwargs):
		kwargs['user_type'] = 'student'
		return super().get_context_data(**kwargs)

	def form_valid(self, form):
		user = form.save()
		login(self.request, user)
		return redirect ('login')

# a class for registering a staff
class StaffSignUpView(CreateView):
	model = MyUser
	form_class = StaffSignUpForm
	template_name = 'sponsorship/staff_register.html'

	def get_context_data(self, **kwargs):
		kwargs['user_type'] = 'staff'
		return super().get_context_data(**kwargs)
	def form_valid(self,form):
		user = form.save()
		login(self.request,user)
		return redirect('login')

# a class for registering a Sponsor
class SponsorSignUpView(CreateView):
	model = MyUser
	form_class = SponsorSignUpForm
	template_name = 'sponsorship/sponsor_register.html'

	def get_context_data(self, **kwargs):
		kwargs['user_type'] = 'sponsor'
		return super().get_context_data(**kwargs)
	def form_valid(self, form):
		user = form.save()
		login(self.request, user)
		return redirect('login')

def home(request):

	return render(request, 'sponsorship/home.html')

#a view for uploading the bio data
@login_required(login_url = 'login')
def bio(request):
	if not request.user.is_authenticated:
		return redirect('index')

	else:
		submitted = False
		if request.method == "POST":
			form = BioForm(request.POST, request.FILES)
			if form.is_valid():
				form.instance.user = request.user
				form.save()
			return HttpResponseRedirect('/school? submitted=True')
		else:
			form = BioForm()
			if 'submitted' in request.GET:
				submitted=True
		form = BioForm()
		context = {
			'form': form,
			'submitted': submitted
		}
		return render(request, 'sponsorship/bio.html', context)

#a view for updating school information
@login_required(login_url = 'login')
def school(request):
	submitted = False
	if request.method == "POST":
		form = SchoolForm(request.POST, request.FILES)
		if form.is_valid():
			form.instance.user = request.user
			form.save()
		return HttpResponseRedirect('/recommendation? submitted=True')
	else:
		form = SchoolForm()
		if 'submitted' in request.GET:
			submitted=True
	form = SchoolForm()
	context = {
		'form': form,
		'submitted': submitted
		}
	return render(request, 'sponsorship/school.html', context)


#a view for updating recommendation details
@login_required(login_url = 'login')
def recommendation(request):
		submitted = False
		if request.method == "POST":
			form = RecommendationForm(request.POST, request.FILES)
			if form.is_valid():
				form.instance.user = request.user
				form.save()
				return HttpResponseRedirect('/reasons? submitted = True')
			else:
				form = RecommendationForm()
				if 'submitted' in request.GET:
					submitted = True
			form = RecommendationForm()
			context = {
				'form':form,
				'submitted':submitted
			}
		return render(request, 'sponsorship/recommendation.html', context)
#the landing page after logging in
def index(request):

    return render(request, 'sponsorship/index.html')

def sponsor(request):

	return render(request, 'sonsorship/sponsor.html')

@login_required(login_url = 'login')
def student_table(request):
	if not request.user.is_authenticated:
		return redirect('login')
	sdetails=Sponsor.objects.all()
	context={
		'sdetails':sdetails
	}
	return render(request, 'sponsorship/student_table.html',context)