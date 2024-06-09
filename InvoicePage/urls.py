from django.urls import path
from . import views

urlpatterns = \
[
    path('', views.index, name='index'),
    path('login', views.loginView, name='loginView'),
    path('register', views.register, name='register'),
    path('makeInvoice/<str:userID>/', views.makeInvoice, name='makeInvoice'),
    path('download_invoice/<str:filename>/', views.download_invoice, name='download_invoice'),
]
