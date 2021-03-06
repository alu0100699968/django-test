"""django_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import RedirectView
from django_cas import views
import notifications.urls

urlpatterns = [
    url(r'^$', RedirectView.as_view(
        pattern_name='users:index', permanent=False), name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^polls/', include('polls.urls')),
    url(r'^users/', include('users.urls')),
    # CAS
    url(r'^accounts/login/$', views.login, name='cas_login'),
    url(r'^accounts/logout/$', views.logout, name='cas_logout'),
    # Notificaciones
    url('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
]
