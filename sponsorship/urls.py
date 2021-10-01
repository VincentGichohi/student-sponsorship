from . import views
from django.urls import path, include
from django.conf import settings
urlpatterns = [
   path('', views.index, name='index'),
   path('dashboard/', views.dashboard, name='dashboard'),
   path('bio/', views.bio, name='bio'),
   path('school/', views.school, name='school'),
   path('recommendation/', views.recommendation, name='recommendation'),
   path('register/', views.register_request, name='register'),
   path('login/', views.login_request, name='login'),
   path('sponsor/', views.sponsor, name='sponsor'),
   path('student/', views.student_table, name='student'),
   path('contact/', views.contact, name='contact')
   # path('accounts/', include('django.contrib.auth.urls')),
]