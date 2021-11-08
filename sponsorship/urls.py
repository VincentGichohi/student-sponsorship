from . import views
from sponsorship.views import StudentSignUpView,StaffSignUpView,SponsorSignUpView
from django.urls import path, include
from django.conf import settings

urlpatterns = [
   path('index/', views.index, name='index'),
   path('dashboard/', views.dashboard, name='dashboard'),
   path('bio/', views.bio, name='bio'),
   path('school/', views.school, name='school'),
   path('recommendation/', views.recommendation, name='recommendation'),
   path('register/', views.register_request, name='register'),
   path('student_register/',StudentSignUpView.as_view(), name = 'student_register'),
   path('sponsor_register/', SponsorSignUpView.as_view(), name = 'sponsor_register'),
   path('staff_register/', StaffSignUpView.as_view(), name = 'staff_register'),
   path('login/', views.login_request, name='login'),
   path('logout/', views.logout, name = 'logout'),
   path('sponsor/', views.sponsor, name='sponsor'),
   path('student/', views.student_table, name='student'),
   path('contact/', views.contact, name='contact'),
   path('home/', views.home,name='home'),
]