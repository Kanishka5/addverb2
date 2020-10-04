from django.urls import path
from expense import views
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', views.home),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.logoutReq, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard')
]
