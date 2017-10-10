"""posted URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views
#from registration.backends.hmac.views import RegistrationView
#from registration.backends.simple.views import RegistrationView
from .views import HomePageView, page_not_found, MyRegistrationView
from .forms import LoginForm, MyRegistrationForm

urlpatterns = [
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^accounts/register/$', MyRegistrationView.as_view(form_class=MyRegistrationForm), name='registration_register'),
    url(r'^accounts/login/$', views.login, {'template_name':'login.html', 'authentication_form':LoginForm}, name='login'),
    url(r'^accounts/logout/$', views.logout, {'next_page': '/accounts/login/'}, name='logout'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^news/', include('news.urls'), name='news'),
    url(r'^admin/', admin.site.urls),
    url(r'^', page_not_found, name='page_not_found'),
]
