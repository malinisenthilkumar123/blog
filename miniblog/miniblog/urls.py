"""
URL configuration for miniblog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from blog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('blog/', include('blog.urls')),
    
    # Redirect /catalog/ to the blog homepage
    path('catalog/', RedirectView.as_view(url='/blog/', permanent=True)),
    
    # Authentication URLs
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    
    # For compatibility - redirect to the standard auth views
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login_old'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name='logout_old'),
]
