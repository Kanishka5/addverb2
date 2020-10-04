from django.urls import path
from expense import views
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', views.home),
    path('signup', views.signup)
]
