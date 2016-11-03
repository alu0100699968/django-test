from django.conf.urls import include, url
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views

from . import views
from . import forms

app_name = 'users'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^list/$', views.ListUsersView.as_view(), name='list'),
    url(r'^(?P<pk>[A-Z]{1}[0-9]{7}|[0-9]{8})/$', views.DetailView.as_view(),
    name='detail'),
    url(r'^(?P<pk>[A-Z]{1}[0-9]{7}|[0-9]{8})/edit$', views.EditView.as_view(),
    name='edit'),
    url(r'^register/$', views.UserRegister.as_view(), name='register'),
    url(r'^account/$', views.profile_redirect, name='account'),
    url(r'^login/$', auth_views.login, {'authentication_form': forms.LoginForm}),
    url('^', include('django.contrib.auth.urls')),
]

'''url(r'^$', RedirectView.as_view(pattern_name='users:login', permanent=False),
name='index'),'''
