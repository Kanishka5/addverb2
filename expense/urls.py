from django.urls import path
from expense import views
from django.views.generic.base import TemplateView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.logoutReq, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('expense/', views.expenseform, name="expenseform"),
    path('approval/', views.approve, name="approve"),
    path('paymentreq/', views.paymentreq, name="paymentreq")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
