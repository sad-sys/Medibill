from django.urls import path
from . import views

urlpatterns = \
[
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('makeInvoice', views.makeInvoice, name='makeInvoice'),
    path('download_invoice/<str:filename>/', views.download_invoice, name='download_invoice'),
]
