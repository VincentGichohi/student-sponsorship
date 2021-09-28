from . import views
from django.urls import path, include
from django.conf import settings
urlpatterns = [
   path('', views.dashboard, name='dashboard'),
   path('bio/', views.bio, name='bio'),
   path('index/', views.index, name='index'),
   path('accounts/', include('django.contrib.auth.urls')),
]