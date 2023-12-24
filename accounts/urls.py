from django.contrib.auth import views as auth_views
from django.urls import path
from accounts.views import (home, signup, logout_view)

from . import views

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
]