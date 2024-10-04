"""
URL configuration for django_anonymous_form project.

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
from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('analytics', views.AnalyticView.as_view(), name='analytics'),
    path('ajax/filters', views.GetTasksWithFilters.as_view(), name='get-tasks-with-filters'),
    path('ajax/details', views.ModalDetailView.as_view(), name='details-modal'),
    path('blank/<int:pk>', views.BlankDetailView.as_view(), name='blank'),

]
