from . import views
from django.urls import path, include
from django.conf import settings
urlpatterns = [
   path('', views.dashboard, name='dashboard'),
   path('bio/', views.bio, name='bio'),
   path('index/', views.index, name='index'),
   path('register/', views.register_request, name='register'),
   path('login/', views.login_request, name='login'),
   path('sponsor/', views.sponsor, name='sponsor'),
   # path('accounts/', include('django.contrib.auth.urls')),
]