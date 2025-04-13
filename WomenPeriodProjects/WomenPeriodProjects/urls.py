"""
URL configuration for WomenPeriodProjects project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path,include
from WomenPeriodApp.views import *
from WomenPeriodApp.Apis.Utilidades.Api_utilidades import *
from WomenPeriodApp.Apis.Listados.Api_listados import *
# from WomenPeriodApp.Urls.urls_women_period_app import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',Home.as_view(),name="Home"),
    path('CalendarioView/',CalendarioView.as_view(),name="CalendarioView"),
    path('GenerarMeses/',GenerarMeses().as_view(),name="GenerarMeses"),
    path('GenerarDias/',GenerarDias().as_view(),name="GenerarDias"),
    path('ProcesarCalendario/',ProcesarCalendario,name='ProcesarCalendario'),
    path('CargaReferenciales/',CargaReferenciales().as_view(),name="CargaReferenciales"),

    path('api/',include("WomenPeriodApp.Urls.urls_women_period_app")), 
]

