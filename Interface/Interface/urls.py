"""Interface URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import url
from . import view

urlpatterns = [
    #path('admin/', admin.site.urls),
    url(r'^logon$', view.logon),
    url(r'^login$', view.login),
    url(r'^logout$', view.logout),
    url(r'^record/add$', view.add_record),
    url(r'^record/0/delete$|^record/-?[1-9][0-9]*/delete$', view.delete_record),
    url(r'^record/0/update$|^record/-?[1-9][0-9]*/update$', view.update_record),
    url(r'^record/0$|^record/-?[1-9][0-9]*$', view.get_record),
    url(r'^record/query$', view.query_record)

    

]
