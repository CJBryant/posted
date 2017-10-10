from django.shortcuts import render, redirect
from django.conf.urls import include
from django.views import generic
from django.contrib.auth import views as auth_views
from registration.backends.simple.views import RegistrationView

class HomePageView(generic.TemplateView):
    template_name = 'home.html'

def page_not_found(request):
    return render(request,'404.html')

class MyRegistrationView(RegistrationView):
    def get_success_url(self, request):
        return '/news/providers/'
